import functools
import json
import time
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

import click
from prettytable import PrettyTable

import noia_sdk as sdk
from noia_sdk.rest import ApiException


class ConfigureNetworkError(Exception):
    pass


class EnvVars:
    NOIA_API_SERVER = "NOIA_API_SERVER"
    NOIA_TOKEN = "NOIA_TOKEN"


class PeerState:
    PRESENT = "present"
    ABSENT = "absent"


class PeerType:
    ENDPOINT = "endpoint"
    TAG = "tag"
    ID = "id"


class ConfigFields:
    ID = "id"
    NAME = "name"
    STATE = "state"
    SERVICES = "services"
    TOPOLOGY = "topology"
    CONNECT_TO = "connect_to"
    CONNECTIONS = "connections"
    PEER_TYPE = "type"
    USE_SDN = "use_sdn"
    IGNORE_NETWORK_TOPOLOGY = "ignore_configured_topology"


@dataclass
class ConnectionServices:
    agent_1: int
    agent_2: int
    agent_1_service_names: list
    agent_2_service_names: list

    @classmethod
    def create(cls, link, endpoints):
        endpoint_1, endpoint_2 = endpoints
        return cls(
            link[0],
            link[1],
            cls._get_services(endpoint_1),
            cls._get_services(endpoint_2),
        )

    @staticmethod
    def _get_services(endpoint):
        service_names = endpoint[1].get(ConfigFields.SERVICES)
        if service_names is None:
            return []
        if isinstance(service_names, str):
            return [service_names]
        if not isinstance(service_names, list) or any(
            not isinstance(name, str) for name in service_names
        ):
            raise ConfigureNetworkError(
                f"Services parameter must be a list of service names for endpoint {endpoint[0]}"
            )
        return service_names

    def get_subnets(self, endpoint_id, agents):
        agent_id = getattr(self, f"agent_{endpoint_id}")
        service_names = getattr(self, f"agent_{endpoint_id}_service_names")
        agent = agents[agent_id]

        return [
            subnet["agent_service_subnet_id"]
            for service in agent["agent_services"]
            for subnet in service["agent_service_subnets"]
            if service["agent_service_name"] in service_names
        ]


ALLOWED_NETWORK_TYPES = (
    sdk.NetworkType.POINT_TO_POINT,
    sdk.NetworkType.GATEWAY,
    sdk.NetworkType.MESH,
)
ALLOWED_NETWORK_TOPOLOGIES = (
    sdk.MetadataNetworkType.P2P,
    sdk.MetadataNetworkType.P2M,
    sdk.MetadataNetworkType.MESH,
)
TAKE_MAX_ITEMS_PER_CALL = 2048
MAX_PAYLOAD_SIZE = 99 * 1024
MAX_QUERY_FIELD_SIZE = 2 * 1024


class WithRetry:
    """Call api method several times in case of an error."""

    def __init__(self, func, retry_count=7, base=15, exponent=1, cap=180, silent=False):
        self.func = func
        self.retry_count = retry_count
        self.base = base
        self.exponent = exponent
        self.cap = cap
        self.silent = silent

    def __call__(self, *args, **kwargs):
        for attempt in range(self.retry_count):
            try:
                return self.func(*args, **kwargs)
            except ApiException as err:
                error = f"API call {self.func.__name__} failed with {err.status} {err.reason}."
                if err.status not in (500, 502, 503, 504, 408, 429):
                    not self.silent and click.secho(error, fg="red", err=True)
                    raise
                # NOTE: This check is specifically for attempting to create connections just after the network was created.
                # In such a case the network ID is returned by the create_network api call, however, it is not yet being seen
                # by subsequent create_connections call if it is made too quickly.
                if err.status == 400 and attempt:
                    raise
                if attempt >= self.retry_count - 1:
                    raise
                delay = min(self.cap, self.base * 2 ** (attempt * self.exponent))
                not self.silent and click.secho(
                    f"{error} Attempt {attempt + 1} out of {self.retry_count}. Waiting for {delay}s to attempt again.",
                    fg="red",
                    err=True,
                )
                time.sleep(delay)


def _default_translator(field):
    def translator(body, data):
        if data is None:
            return body[field]
        else:
            return {
                **body,
                field: data,
            }

    return translator


class BatchedRequest:
    """Executes requests in batches in order to circumvent payload/field size limit.
    Assumes that the batchable parameter is a list/tuple and api call returns a list.

    Translator must be provided for requests that have "body" as a kwarg. The translator
    is a callable that accepts the body as first argument and batch data as the second argument.
    It must return the list if the second argument is None and the payload body otherwise.
    It must not modify the body.

    Example translator:
        def translator(body, data):
            if data is None:
                return body["data"]
            else:
                return {
                    **body,
                    "data": data,
                }
    """

    def __init__(
        self,
        func,
        max_payload_size,
        translator=_default_translator("data"),
        silent=False,
    ):
        self.func = func
        self.max_payload_size = max_payload_size
        self.translator = translator
        self.silent = silent

    def __call__(self, *args, **kwargs):
        if "body" in kwargs:
            return self._call_with_body(*args, **kwargs)
        else:
            return self._call_with_query(*args, **kwargs)

    def _call_with_body(self, *args, **kwargs):
        body = kwargs.pop("body")
        data = self.translator(body, None)
        return self._call(body, data, *args, **kwargs)

    def _call_with_query(self, *args, **kwargs):
        query = args[0]
        args = args[1:]
        return self._call(None, query, *args, **kwargs)

    def _calculate_payload_size(self, data):
        if isinstance(data, list):
            return len(",".join(str(i) for i in data))
        else:
            return len(json.dumps(data))

    def _determine_batch_size(self, body, data, batch_size):
        while batch_size:
            data = data[:batch_size]
            batch = self.translator(body, data) if body is not None else data
            if self._calculate_payload_size(batch) > self.max_payload_size:
                batch_size //= 2
            else:
                return batch_size, batch
        raise ConfigureNetworkError(f"Batch size could not be determined")

    def _generate_batches(self, body, data):
        batch_size = len(data)
        while data:
            batch_size, batch = self._determine_batch_size(body, data, batch_size)
            data = data[batch_size:]
            yield batch

    def _call(self, body, data, *args, **kwargs):
        result = []
        for batch in self._generate_batches(body, data):
            # TODO: What to do with errors in result?
            func = WithRetry(self.func, silent=self.silent)
            if body is None:
                response = func(batch, *args, **kwargs)
            else:
                response = func(body=batch, *args, **kwargs)
            if isinstance(response, dict) and "data" in response:
                result += response["data"]
            else:
                result.append(response)
        # NOTE: Undesirable side effect: will transform non-list responses to {"data": data}
        return {"data": result}


def print_table(items, fields, to_json=False):
    """Prints either a pretty table using fields or a json from items.

    fields is a list of tuples, where the first element of the tuple represents the title of the field
    and the second element may be either an item's field name or a callable.
    Third element is optional and is used to format the field value.
    Also, if the second element is a list/tuple, then the fields will be retrieved recursively.

    NOTE: In such a case formatter function must accept all intermediate objects.

    Args:
        items (list[dict]): A list of items to generate the table for.
        fields (list[tuple]): Field definition.
        to_json (boolean): Outputs a JSON instead of a table if True.
    """

    def get_field(item, field):
        if item is None:
            return "-"
        field_param = field[0]
        field_formatter = (
            field[1] if len(field) == 2 else lambda x: x is None and "-" or x
        )
        if isinstance(field_param, (list, tuple)):
            field_value = item
            for subfield in field_param:
                field_value = get_field(field_value, [subfield])
                if not isinstance(field_value, dict):
                    break
        else:
            field_value = (
                field_param(item)
                if hasattr(field_param, "__call__")
                else item.get(field_param)
            )
        return field_formatter(field_value)

    if not to_json:
        table = PrettyTable()
        table.field_names = [field[0] for field in fields]
        for item in items:
            table.add_row([get_field(item, field[1:]) for field in fields])
        click.echo(str(table))
    else:
        click.echo(json.dumps(items, indent=4))


def find_by_name(items, name, field):
    """Finds an ID of an object with a corresponding name.

    NOTE: This is utterly inefficient for lists of names as it calls itself for each name.
    A faster implementation should be found to support larget `items` sizes.

    Args:
        items (iterable): A collection of objects to search for.
        name (Union[str, List[str]]): Either a single name or a list of names to look up.
        field (str): Field name prefix. "_name" and "_id" will be appended to get e.g. "api_key_id".

    Returns:
        Union[int, list[Union[int, None]], None]: found Ids for the provided names. Or None if not found.
    """
    if isinstance(name, (list, tuple)):
        return [find_by_name(items, nm, field) for nm in name]
    matching_ids = [
        item.get(f"{field}_id") for item in items if name == item.get(f"{field}_name")
    ]
    if len(matching_ids) != 1:
        click.secho(f'Could not find an id by name="{name}"', err=True, fg="red")
        return
    return matching_ids[0]


@functools.lru_cache(maxsize=None)
def resolve_agent_by_name(api, name, silent=False):
    return [
        agent["agent_id"]
        for agent in WithRetry(api.index_agents, silent=silent)(
            filter=f"id|name:{name}", load_relations=False
        )["data"]
    ]


@functools.lru_cache(maxsize=None)
def get_all_agents(api, silent=False):
    all_agents = WithRetry(api.index_agents, silent=silent)(
        take=TAKE_MAX_ITEMS_PER_CALL
    )["data"]
    return {agent["agent_id"]: agent for agent in all_agents}


def resolve_agents(api, agents, silent=False):
    """Resolves endpoint names to ids inplace.

    Args:
        api (PlatformApi): API object to communicate with the platform.
        agents (dict): A dictionary containing endpoints.
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.
    """
    for name, id in agents.items():
        if id is not None:
            continue
        result = resolve_agent_by_name(api, name, silent=silent)
        if len(result) != 1:
            error = f"Could not resolve endpoint name {name}, found: {result}."
            if not silent:
                click.secho(
                    error,
                    err=True,
                    fg="red",
                )
                continue
            else:
                raise ConfigureNetworkError(error)
        agents[name] = result[0]


def get_peer_id(peer_name, peer_config):
    peer_type = peer_config.get(ConfigFields.PEER_TYPE, PeerType.ENDPOINT)
    if peer_type == PeerType.ENDPOINT:
        return peer_config.get(ConfigFields.ID)
    elif peer_type == PeerType.ID:
        try:
            return int(peer_name)
        except ValueError:
            return None
    else:
        return None


def resolve_present_absent(agents, present, absent):
    """Resolves agent connections by objects into agent connections by ids.
    Additionally removes any present connections if they were already added to absent.

    Present connections are the connections that appear as "present" in the config
    and will be added to the network.
    Absent connections are the connections that appear as "absent" in the config and
    will be removed from the existing network.
    Services is a list of service names assigned to the connection's corresponding endpoints.

    Args:
        agents (dict[str, int]): Agent map from name to id.
        present (list): A list of connections that are marked as present in the config.
        absent (list): A list of connections that are marked as absent in the config.

    Returns:
        tuple: Three items that correspond to present/absent connections and a list
            of ConnectionServices objects that correspond to present connections.

            Present/absent connections is a list of lists of two elements, where
            elements are agent ids.
    """
    present_ids = [[agents[src[0]], agents[dst[0]]] for src, dst in present]
    absent_ids = [[agents[src[0]], agents[dst[0]]] for src, dst in absent]
    services = [
        ConnectionServices.create(link, conn)
        for link, conn in zip(present_ids, present)
        if link not in absent_ids and link[::-1] not in absent_ids
    ]
    return (
        [
            link
            for link in present_ids
            if link not in absent_ids and link[::-1] not in absent_ids
        ],
        absent_ids,
        services,
    )


def resolve_p2p_connections(api, connections, silent=False):
    """Resolves configuration connections for Point to Point topology.

    Args:
        api (PlatformApi): API object to communicate with the platform.
        connections (dict): A dictionary containing connections as described in the config file.
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.

    Returns:
        list: A list of two item lists describing endpoint to endpoint connections.
    """
    present = []
    absent = []
    agents = {}

    for src in connections.items():
        dst = src[1].get(ConfigFields.CONNECT_TO)
        if dst is None or len(dst.keys()) == 0:
            continue
        dst = list(dst.items())[0]

        agents[src[0]] = get_peer_id(*src)
        agents[dst[0]] = get_peer_id(*dst)

        if (
            src[1].get(ConfigFields.STATE) == PeerState.ABSENT
            or dst[1].get(ConfigFields.STATE) == PeerState.ABSENT
        ):
            absent.append((src, dst))
        elif (
            src[1].get(ConfigFields.STATE, PeerState.PRESENT) == PeerState.PRESENT
            or dst[1].get(ConfigFields.STATE, PeerState.PRESENT) == PeerState.PRESENT
        ):
            present.append((src, dst))
        else:
            error = f"Invalid state for agents {src[0]} or {dst[0]}"
            if not silent:
                click.secho(error, fg="red", err=True)
            else:
                raise ConfigureNetworkError(error)

    resolve_agents(api, agents, silent=silent)
    if any(id is None for id in agents.keys()):
        return resolve_present_absent({}, [], [])

    return resolve_present_absent(agents, present, absent)


def expand_agents_tags(api, dst_dict, silent=False):
    """Expand tag endpoints into individual endpoints.

    Args:
        api (PlatformApi): API object to communicate with the platform.
        dst_dict ([type]): [description]
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.

    Raises:
        ConfigureNetworkError: In case of any errors

    Returns:
        Union[dict, None]: Dictionary with expanded endpoints where key is the name and value is the config(id, state, type).
    """
    items = {}

    # First expand tags
    for name, dst in dst_dict.items():
        if dst.get(ConfigFields.PEER_TYPE) != PeerType.TAG:
            continue

        agents = WithRetry(api.index_agents)(
            filter=f"tags_names[]:{name}", take=TAKE_MAX_ITEMS_PER_CALL
        )["data"]
        if not agents:
            error = f"Could not find endpoints by the tag {name}"
            if not silent:
                click.secho(error, err=True, fg="red")
                return
            else:
                raise ConfigureNetworkError(error)

        tag_state = dst.get(ConfigFields.STATE, PeerState.PRESENT)
        for agent in agents:
            agent_name = agent["agent_name"]
            if agent_name not in items or (
                tag_state == PeerState.ABSENT
                and items[agent_name][ConfigFields.STATE] == PeerState.PRESENT
            ):
                items[agent_name] = {
                    ConfigFields.ID: agent["agent_id"],
                    ConfigFields.STATE: tag_state,
                    ConfigFields.PEER_TYPE: PeerType.ENDPOINT,
                    ConfigFields.SERVICES: dst.get(ConfigFields.SERVICES),
                }

    # Then override with explicit configs
    for name, dst in dst_dict.items():
        if dst.get(ConfigFields.PEER_TYPE) != PeerType.TAG:
            items[name] = dst
            continue

    return items


def resolve_p2m_connections(api, connections, silent=False):
    """Resolves configuration connections for Point to Multipoint topology. Also, expands tags.

    Args:
        api (PlatformApi): API object to communicate with the platform.
        connections (dict): A dictionary containing connections as described in the config file.
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.

    Returns:
        list: A list of two item lists describing endpoint to endpoint connections.
    """
    present = []
    absent = []
    agents = {}

    for src in connections.items():
        dst_dict = src[1].get(ConfigFields.CONNECT_TO)
        if dst_dict is None or len(dst_dict.keys()) == 0:
            continue
        dst_dict = expand_agents_tags(api, dst_dict)
        if dst_dict is None:
            return resolve_present_absent({}, [], [])

        agents[src[0]] = get_peer_id(*src)
        for dst in dst_dict.items():
            agents[dst[0]] = get_peer_id(*dst)
            if (
                src[1].get(ConfigFields.STATE) == PeerState.ABSENT
                or dst[1].get(ConfigFields.STATE) == PeerState.ABSENT
            ):
                absent.append((src, dst))
            elif (
                src[1].get(ConfigFields.STATE, PeerState.PRESENT) == PeerState.PRESENT
                or dst[1].get(ConfigFields.STATE, PeerState.PRESENT)
                == PeerState.PRESENT
            ):
                present.append((src, dst))
            else:
                error = f"Invalid state for agents {src[0]} or {dst[0]}"
                if not silent:
                    click.secho(error, fg="red", err=True)
                else:
                    raise ConfigureNetworkError(error)

    resolve_agents(api, agents, silent=silent)
    if any(id is None for id in agents.keys()):
        return resolve_present_absent({}, [], [])

    return resolve_present_absent(agents, present, absent)


def resolve_mesh_connections(api, connections, silent=False):
    """Resolves configuration connections for mesh topology. Also, expands tags.

    Args:
        api (PlatformApi): API object to communicate with the platform.
        connections (dict): A dictionary containing connections.
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.

    Returns:
        list: A list of two item lists describing endpoint to endpoint connections.
    """
    present = []
    absent = []

    connections = expand_agents_tags(api, connections)
    if connections is None:
        return resolve_present_absent({}, [], [])

    agents = {
        name: get_peer_id(name, connection) for name, connection in connections.items()
    }

    # NOTE: Assuming connections are bidirectional
    for src, dst in combinations(connections.items(), 2):
        if (
            src[1].get(ConfigFields.STATE) == PeerState.ABSENT
            or dst[1].get(ConfigFields.STATE) == PeerState.ABSENT
        ):
            absent.append((src, dst))
        elif (
            src[1].get(ConfigFields.STATE, PeerState.PRESENT) == PeerState.PRESENT
            or dst[1].get(ConfigFields.STATE, PeerState.PRESENT) == PeerState.PRESENT
        ):
            present.append((src, dst))
        else:
            error = f"Invalid state for agents {src[0]} or {dst[0]}"
            if not silent:
                click.secho(error, fg="red", err=True)
            else:
                raise ConfigureNetworkError(error)

    resolve_agents(api, agents, silent=silent)
    if any(id is None for id in agents.keys()):
        return resolve_present_absent({}, [], [])

    return resolve_present_absent(agents, present, absent)


def configure_connection(api, config, connection, silent=False):
    agents = {
        connection["agent_1"]["agent_id"]: connection["agent_1"],
        connection["agent_2"]["agent_id"]: connection["agent_2"],
    }

    enabled_subnets = set(config.get_subnets(1, agents) + config.get_subnets(2, agents))
    current_subnets = {
        subnet["agent_service_subnet_id"]: subnet["agent_connection_subnet_is_enabled"]
        for subnet in connection["agent_connection_subnets"]
    }

    # First collect all the changes to the original configured subnets
    changes = [
        {
            "agentServiceSubnetId": id,
            "isEnabled": id in enabled_subnets,
        }
        for id, enabled in current_subnets.items()
        if (id in enabled_subnets) != enabled
    ]
    # Then configure any missing subnets
    changes += [
        {
            "agentServiceSubnetId": id,
            "isEnabled": True,
        }
        for id in enabled_subnets
        if id not in current_subnets
    ]

    if not changes:
        return 0

    body = {
        "connectionId": connection["agent_connection_id"],
        "changes": changes,
    }
    BatchedRequest(
        api.update_connection_services,
        max_payload_size=MAX_PAYLOAD_SIZE,
        translator=_default_translator("changes"),
        silent=silent,
    )(body=body)
    return len(changes)


def configure_connections(api, services_config, connections, silent=False):
    ids = [connection["agent_connection_id"] for connection in connections]
    if not ids:
        return 0, 0
    connections_services = BatchedRequest(
        api.get_connection_services,
        max_payload_size=MAX_QUERY_FIELD_SIZE,
        silent=silent,
    )(ids)["data"]

    # Build a map of connections so that it would be quicker to resolve them to subnets
    services_map = {}
    for conn in connections_services:
        services_map[
            frozenset((conn["agent_1"]["agent_id"], conn["agent_2"]["agent_id"]))
        ] = conn

    updated_connections = 0
    updated_subnets = 0
    # Update subnets with connection subnets
    for config in services_config:
        key = frozenset((config.agent_1, config.agent_2))
        if key not in services_map:
            not silent and click.secho(
                f"Warning: Connection from {config.agent_1} to {config.agent_2} was not created.",
                fg="yellow",
                err=True,
            )
            continue

        updated_connections += 1
        updated_subnets += configure_connection(
            api, config, services_map[key], silent=silent
        )

    return updated_connections, updated_subnets


def configure_network_create(api, config, dry_run, silent=False):
    """Configures a new network using provided config.

    Example dictionary:
    {
        "name": "network-name",
        "id": `network-id`,
        "topology": `P2P|P2M|MESH`,
        "use_sdn": `True|False`,
        "state": "present|absent",
        "connections": {
            # Connection for P2P
            "endpoint-name-1": {
                "type": "endpoint|tag|id",
                "id": 1,
                "state": "present|absent",
                "services": ["service1", "service2"],
                "connect_to": {
                    "endpoint-name-2": {
                        "type": "endpoint",
                        "id": 2,
                        "services": ["service3", "service4"],
                    },
                },
            },

            # Connection for P2M
            "source-endpoint": {
                "type": "endpoint",
                "id": 1,
                "state": "present",
                "connect_to": {
                    "destination-1": {
                        "state": "present",
                        "id": 10,
                        "type": "endpoint",
                    },
                    "destination-2": {
                        "state": "present",
                        "id": 11,
                        "type": "endpoint",
                    },
                    "destination-3": {
                        "state": "present",
                        "id": 12,
                        "type": "endpoint",
                    },
                },
            },

            # MESH network - all endpoints interconnected
            "endpoint-1": {
                "type": "endpoint",
                "state": "present",
                "id": 10,
            },
            "endpoint-2": {
                "type": "endpoint",
                "state": "present",
                "id": 11,
            },
            "endpoint-3": {
                "type": "endpoint",
                "state": "present",
                "id": 12,
            },
            "endpoint-4": {
                "type": "endpoint",
                "state": "present",
                "id": 13,
            },
        }
    }

    Args:
        api (PlatformApi): Instance of the platform API
        config (dict): Configuration dictionary
        dry_run (bool): Indicates whether to perform a dry run (without any configuration)
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.

    Returns:
        (bool): True if any changes were made and False otherwise
    """
    topology = config[ConfigFields.TOPOLOGY].upper()
    connections = config.get(ConfigFields.CONNECTIONS, {})

    if topology not in ALLOWED_NETWORK_TOPOLOGIES:
        error = f"Network topology {topology} is not allowed."
        if not silent:
            click.secho(error, err=True, fg="red")
            return False
        else:
            raise ConfigureNetworkError(error)

    if (
        topology == sdk.MetadataNetworkType.P2P
        or topology == sdk.MetadataNetworkType.P2M
    ):
        if not all(
            ConfigFields.CONNECT_TO in connection for connection in connections.values()
        ):
            error = f"All connections must have {ConfigFields.CONNECT_TO} parameter for topology {topology}."
            if not silent:
                click.secho(
                    error,
                    err=True,
                    fg="red",
                )
                return False
            else:
                raise ConfigureNetworkError(error)

    if topology == sdk.MetadataNetworkType.P2P:
        peers, _, services = resolve_p2p_connections(api, connections, silent=silent)
    elif topology == sdk.MetadataNetworkType.P2M:
        peers, _, services = resolve_p2m_connections(api, connections, silent=silent)
    else:
        peers, _, services = resolve_mesh_connections(api, connections, silent=silent)

    if not peers:
        not silent and click.secho(
            f"No valid peers specified for network {config[ConfigFields.NAME]}",
            fg="yellow",
            err=True,
        )
        return False

    try:
        use_sdn = bool(config.get(ConfigFields.USE_SDN, False))
    except ValueError:
        not silent and click.secho(
            "SDN Connections must evaluate to boolean", err=True, fg="red"
        )
        return False

    body = {
        "network_name": config[ConfigFields.NAME],
        "network_type": sdk.NetworkType.POINT_TO_POINT,
        "network_disable_sdn_connections": not use_sdn,
        "network_metadata": {
            "network_created_by": sdk.NetworkGenesisType.CONFIG,
            "network_type": topology,
        },
    }
    if dry_run:
        network_id = 123
        not silent and click.echo(
            f"Would create network {config[ConfigFields.NAME]} as {topology}"
        )
    else:
        result = WithRetry(api.create_network, silent=silent)(body=body)
        network_id = result["data"]["network_id"]
        not silent and click.echo(
            f"Created network {config[ConfigFields.NAME]} with id {network_id}"
        )

    body = {
        "network_id": network_id,
        "agent_ids": peers,
        "network_update_by": sdk.NetworkGenesisType.CONFIG,
    }
    if dry_run:
        not silent and click.echo(
            f"Would create {len(peers)} connections for network {config[ConfigFields.NAME]}"
        )
        return False
    else:
        connections = BatchedRequest(
            api.create_connections,
            translator=_default_translator("agent_ids"),
            max_payload_size=MAX_PAYLOAD_SIZE,
            silent=silent,
        )(body=body)["data"]
        not silent and click.echo(
            f"Created {len(connections)} connections for network {config[ConfigFields.NAME]}"
        )
        updated_connections, updated_subnets = configure_connections(
            api, services, connections, silent=silent
        )
        not silent and click.echo(
            f"Configured {updated_connections} connections and {updated_subnets} subnets for network {config[ConfigFields.NAME]}"
        )
        return True


def configure_network_delete(api, network, dry_run, silent=False):
    """Deletes existing network's connections and the network itself.

    Args:
        api (PlatformApi): Instance of the platform API.
        network (dict): Dictionary containing id and name keys.
        dry_run (bool): Indicates whether to perform a dry run (without any configuration).
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.

    Returns:
        (bool): True if any changes were made and False otherwise
    """
    connections = WithRetry(api.index_connections, silent=silent)(
        filter=f"networks[]:{network['id']}", take=TAKE_MAX_ITEMS_PER_CALL
    )
    for connection in connections["data"]:
        if connection["network_id"] != network["id"]:
            continue
        if dry_run:
            not silent and click.echo(
                f"Would delete connection {connection['agent_connection_id']}..."
            )
        else:
            WithRetry(api.delete_connection, silent=silent)(
                connection["agent_connection_id"]
            )
            not silent and click.echo(
                f"Deleted connection {connection['agent_connection_id']}."
            )

    if dry_run:
        not silent and click.echo(
            f"Would delete network {network['name']} ({network['id']})..."
        )
        return False
    else:
        WithRetry(api.delete_networks, silent=silent)(network["id"])
        not silent and click.echo(f"Deleted network {network['name']}")
        return True


def configure_network_update(api, network, config, dry_run, silent=False):
    """Updates existing network's connection.

    NOTE: Updates only peers. Does not update network type, SDN or agent gateway ID.

    Args:
        api (PlatformApi): Instance of the platform API.
        network (dict): Dictionary containing existing network information.
        config (dict): Configuration dictionary.
        dry_run (bool): Indicates whether to perform a dry run (without any configuration).
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.

    Returns:
        (bool): True if any changes were made and False otherwise
    """
    topology = config[ConfigFields.TOPOLOGY].upper()
    if topology != network[ConfigFields.TOPOLOGY] and not config.get(
        ConfigFields.IGNORE_NETWORK_TOPOLOGY, False
    ):
        error = f"Configured and requested network topologies do not match: {network[ConfigFields.TOPOLOGY]} v.s. {topology}."
        if not silent:
            click.secho(
                error,
                err=True,
                fg="red",
            )
            return False
        else:
            raise ConfigureNetworkError(error)
    elif topology != network[ConfigFields.TOPOLOGY] and config.get(
        ConfigFields.IGNORE_NETWORK_TOPOLOGY, False
    ):
        click.secho(
            (
                f"Configured and requested network topologies do not match: "
                f"{network[ConfigFields.TOPOLOGY]} v.s. {topology}. However, "
                f"{ConfigFields.IGNORE_NETWORK_TOPOLOGY} is set."
            ),
            err=True,
            fg="yellow",
        )
        if network[ConfigFields.TOPOLOGY] != sdk.MetadataNetworkType.P2P:
            click.secho(
                "NOTE: It is more practical to override P2P topologies.",
                err=True,
                fg="yellow",
            )

    connections = WithRetry(api.index_connections, silent=silent)(
        filter=f"networks[]:{network[ConfigFields.ID]}", take=TAKE_MAX_ITEMS_PER_CALL
    )["data"]
    # NOTE: This is required due to the way tests are designed. Tests should be refactored.
    connections = [
        connection
        for connection in connections
        if connection["network_id"] == network[ConfigFields.ID]
    ]
    all_agents = get_all_agents(api, silent)
    resolved_connections = transform_connections(
        all_agents,
        connections,
        network[ConfigFields.TOPOLOGY],
        group_tags=False,
        silent=silent,
    )
    current_connections = {
        frozenset((connection["agent_1_id"], connection["agent_2_id"])): connection
        for connection in connections
    }
    config_connections = config.get(ConfigFields.CONNECTIONS, {})

    if topology == sdk.MetadataNetworkType.P2P:
        present, absent, services = resolve_p2p_connections(
            api, config_connections, silent=silent
        )
    elif topology == sdk.MetadataNetworkType.P2M:
        present, absent, services = resolve_p2m_connections(
            api, config_connections, silent=silent
        )
    else:
        present, absent, services = resolve_mesh_connections(
            api, config_connections, silent=silent
        )
    if network[ConfigFields.TOPOLOGY] == sdk.MetadataNetworkType.P2P:
        current, _, _ = resolve_p2p_connections(
            api, resolved_connections, silent=silent
        )
    elif network[ConfigFields.TOPOLOGY] == sdk.MetadataNetworkType.P2M:
        current, _, _ = resolve_p2m_connections(
            api, resolved_connections, silent=silent
        )
    else:
        current, _, _ = resolve_mesh_connections(
            api, resolved_connections, silent=silent
        )

    present = [frozenset(i) for i in present]
    absent = [frozenset(i) for i in absent]
    current = [frozenset(i) for i in current]

    to_add = [list(link) for link in present if link not in current]
    to_remove = [
        conn["agent_connection_id"]
        for link, conn in current_connections.items()
        if link in absent
    ]

    for item in to_remove:
        if dry_run:
            not silent and click.echo(f"Would remove connection {item}.")
        else:
            WithRetry(api.delete_connection, silent=silent)(item)
            not silent and click.echo(f"Removed connection {item}.")

    added_connections = []
    if dry_run:
        not silent and click.echo(f"Would create {len(to_add)} connections.")
    elif to_add:
        body = {
            "network_id": network["id"],
            "agent_ids": to_add,
            "network_update_by": sdk.NetworkGenesisType.CONFIG,
        }
        added_connections = BatchedRequest(
            api.create_connections,
            translator=_default_translator("agent_ids"),
            max_payload_size=MAX_PAYLOAD_SIZE,
            silent=silent,
        )(body=body, update_type=sdk.UpdateType.APPEND_NEW)["data"]
        not silent and click.echo(
            f"Created {len(to_add)} connections for network {config[ConfigFields.NAME]}"
        )

    connections = [
        connection
        for connection in connections + added_connections
        if connection["agent_connection_id"] not in to_remove
    ]

    if dry_run:
        not silent and click.echo(f"Would configure {len(connections)} connections.")
    else:
        updated_connections, updated_subnets = configure_connections(
            api, services, connections, silent=silent
        )
        not silent and click.echo(
            f"Configured {updated_connections} connections and {updated_subnets} subnets for network {config[ConfigFields.NAME]}"
        )
        return updated_subnets > 0
    return False


def configure_network(api, config, dry_run, silent=False):
    """Configures NOIA Network based on the current state and the requested state.

    Args:
        api (PlatformApi): Instance of the platform API.
        config (dict): Configuration dictionary.
        dry_run (bool): Indicates whether to perform a dry run (without any configuration).
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.

    Returns:
        (bool): True if any changes were made and False otherwise
    """
    if not all(i in config for i in (ConfigFields.NAME, ConfigFields.STATE)):
        error = f"{ConfigFields.NAME} and {ConfigFields.STATE} must be present"
        if not silent:
            click.secho(error, err=True, fg="red")
        else:
            raise ConfigureNetworkError(error)
        return False

    name = config[ConfigFields.NAME]
    id = config.get(ConfigFields.ID)
    state = config[ConfigFields.STATE]
    if state not in (PeerState.PRESENT, PeerState.ABSENT):
        error = f"Invalid network {name} {id if id else ''} state {state}"
        if not silent:
            click.secho(error, fg="red", err=True)
            return False
        else:
            raise ConfigureNetworkError(error)

    not silent and click.secho(
        f"Configuring network {name} {id if id else ''}", fg="green"
    )

    networks = WithRetry(api.index_networks, silent=silent)(
        filter=f"id|name:{name if id is None else id}",
        take=TAKE_MAX_ITEMS_PER_CALL,
    )["data"]
    networks = [
        transform_network(net) for net in networks if net["network_name"] == name
    ]

    if len(networks) == 0 and state == PeerState.PRESENT:
        return configure_network_create(api, config, dry_run, silent=silent)
    elif len(networks) == 1 and state == PeerState.PRESENT:
        return configure_network_update(
            api, networks[0], config, dry_run, silent=silent
        )
    elif len(networks) == 1 and state == PeerState.ABSENT:
        return configure_network_delete(api, networks[0], dry_run, silent=silent)
    elif len(networks) > 1:
        not silent and click.secho(
            f"There are more than one network by the name {name}",
            err=True,
            fg="red",
        )
    return False


def transform_network(network, reference=None):
    """Transforms NetworkObject into internal representation that is used either for export or configuration.

    Args:
        network (NetworkObject): A Network to transform.
        reference (dict): A dictionary describing reference Network configuration.

    Returns:
        dict: Transformed Network representation.
    """
    topology = network.get("network_metadata", {}).get("network_type", "").upper()
    # NOTE: If the network was configured using the SDK or Ansible network_type will always be POINT_TO_POINT and
    # topology information is saved in network_metadata.network_type, however, we still want to support
    # networks created using network_type, thus this conversion.
    if not topology:
        # Topology not set in the metadata, inferring from network type.
        topology = {
            sdk.NetworkType.POINT_TO_POINT: sdk.MetadataNetworkType.P2P,
            sdk.NetworkType.GATEWAY: sdk.MetadataNetworkType.P2M,
            sdk.NetworkType.MESH: sdk.MetadataNetworkType.MESH,
        }[network["network_type"]]
    return {
        ConfigFields.NAME: network["network_name"],
        ConfigFields.ID: network["network_id"],
        ConfigFields.TOPOLOGY: topology,
        ConfigFields.USE_SDN: not network["network_disable_sdn_connections"],
        ConfigFields.STATE: PeerState.PRESENT,
    }


def get_enabled_connection_subnets(connection):
    """Retrieve configured as enabled subnets for given connection.

    Args:
        connection (dict): A connection object that has agent_connection_services injected.

    Returns:
        set: A set of enabled agent service subnet ids
    """
    return {
        subnet["agent_service_subnet_id"]
        for subnet in connection.get("agent_connection_services", {}).get(
            "agent_connection_subnets", []
        )
        if subnet["agent_connection_subnet_is_enabled"]
    }


def transform_connection_agent_services(enabled_subnets, agent_ref, connection):
    """Transforms enabled connection service subnets to a set of service names.

    Args:
        enabled_subnets (iterable): A set of enabled subnets for the given connection.
        agent_ref (str): One of "agent_1" or "agent_2".
        connection (dict): A connection object that has agent_connection_services injected.

    Returns:
        set: A set of enabled agent service names
    """
    return {
        service["agent_service_name"]
        for service in connection.get("agent_connection_services", {})
        .get(agent_ref, {})
        .get("agent_services", [])
        if any(
            subnet["agent_service_subnet_id"] in enabled_subnets
            for subnet in service["agent_service_subnets"]
        )
    }


def transform_connection_services(connection):
    """Retrieve enabled service names for each agent in the connection.

    Args:
        connection (dict): A connection object that has agent_connection_services injected.

    Returns:
        tuple: A tuple consisting of two elements, where the first one corresponds to
            agent_1 and the second one to agent_2.
    """
    enabled_subnets = get_enabled_connection_subnets(connection)
    return (
        transform_connection_agent_services(enabled_subnets, "agent_1", connection),
        transform_connection_agent_services(enabled_subnets, "agent_2", connection),
    )


def transform_p2p_connections(
    all_agents, connections, reference=None, group_tags=False
):
    """Transforms connections assuming One to One topology(Point to Point).

    Args:
        connections (List[AgentConnectionObject]): A list of connections that are assigned to the provided network.
        reference (dict): A dictionary describing reference connections configuration.

    Returns:
        dict: A dictionary with keys as endpoints and values as dicts explaining the endpoint(state, type).
    """
    transformed_connections = {}
    for connection in connections:
        agent_1, agent_2 = connection["agent_1"], connection["agent_2"]
        agent_1_services, agent_2_services = transform_connection_services(connection)
        agent_1_name = agent_1["agent_name"]
        agent_1_type = PeerType.ENDPOINT
        # We must swap A and B agents if we have already made a connection from A->*
        # so that it would be B->A.
        if agent_1["agent_name"] in transformed_connections:
            agent_1, agent_2 = agent_2, agent_1
            agent_1_name = agent_1["agent_name"]
            agent_1_services, agent_2_services = agent_2_services, agent_1_services
        # Fallback to id instead of name if we already have B->*
        if agent_1_name in transformed_connections:
            agent_1_name = agent_1["agent_id"]
            agent_1_type = PeerType.ID
        # Try second agent id instead
        if agent_1_name in transformed_connections:
            agent_1, agent_2 = agent_2, agent_1
            agent_1_services, agent_2_services = agent_2_services, agent_1_services
            agent_1_name = agent_1["agent_id"]
        # Sadly we're out of options here even though it shouldn't happen
        if agent_1_name in transformed_connections:
            click.secho(
                (
                    f"Could not represent connections from {agent_1['agent_name']} to {agent_2['agent_name']} "
                    f"using P2P topology. Consider overriding to P2M or MESH."
                ),
                err=True,
                fg="yellow",
            )
            continue

        transformed_connections[agent_1_name] = {
            ConfigFields.ID: agent_1["agent_id"],
            ConfigFields.PEER_TYPE: agent_1_type,
            ConfigFields.STATE: PeerState.PRESENT,
            ConfigFields.SERVICES: list(agent_1_services),
            ConfigFields.CONNECT_TO: {
                agent_2["agent_name"]: {
                    ConfigFields.ID: agent_2["agent_id"],
                    ConfigFields.PEER_TYPE: PeerType.ENDPOINT,
                    ConfigFields.SERVICES: list(agent_2_services),
                }
            },
        }
    return transformed_connections


def _group_agents_by_tags(agents):
    """A helper method to group agents by tags. Will return a dictionary of tag id as keys and a set of agent ids.

    Args:
        agents (dict): A dictionary containing agents as {agent_id: agent, ...}

    Returns:
        dict: A dictionary containing agents grouped by tags as {tag_name: set(agent_ids)}
    """
    tags = defaultdict(list)
    # Group agents by tags.
    for id, agent in agents.items():
        agent_tags = agent.get("agent_tags", [])
        for tag in agent_tags:
            tags[tag["agent_tag_name"]].append(agent["agent_id"])
        if not agent_tags:
            tags[None].append(agent["agent_id"])

    return {tag: set(agent_ids) for tag, agent_ids in tags.items()}


def group_agents_by_tags(agents, endpoints):
    """Will group endpoints using the same tag and returns the group.

    Args:
        agents (List[AgentConnectionObject]): A list of all agents.
        endpoints (dict): Endpoints configured for a network.

    Returns:
        dict: A dictionary with keys as endpoints and values as dicts explaining the endpoint(state, type).
    """
    tags = _group_agents_by_tags(agents)
    endpoint_tags = _group_agents_by_tags(
        {
            endpoint[ConfigFields.ID]: agents[endpoint[ConfigFields.ID]]
            for endpoint in endpoints.values()
        }
    )
    services = {
        endpoint[ConfigFields.ID]: endpoint.get(ConfigFields.SERVICES, [])
        for endpoint in endpoints.values()
    }

    grouped_endpoints = {}
    # Create a new dictionary with tags
    for tag, endpoints in endpoint_tags.items():
        if tag is None or tags[tag] != endpoints:
            grouped_endpoints.update(
                {
                    agents[endpoint_id]["agent_name"]: {
                        ConfigFields.PEER_TYPE: PeerType.ENDPOINT,
                        ConfigFields.ID: endpoint_id,
                        ConfigFields.STATE: PeerState.PRESENT,
                        ConfigFields.SERVICES: services[endpoint_id],
                    }
                    for endpoint_id in endpoints
                }
            )
        elif tags[tag] == endpoints:
            grouped_endpoints[tag] = {
                ConfigFields.PEER_TYPE: PeerType.TAG,
                ConfigFields.STATE: PeerState.PRESENT,
                ConfigFields.SERVICES: list(
                    set(sum((services[endpoint_id] for endpoint_id in endpoints), []))
                ),
            }

    # Cleanup endpoints that fall into any tags
    result = {
        name: endpoint
        for name, endpoint in grouped_endpoints.items()
        if endpoint[ConfigFields.PEER_TYPE] == PeerType.TAG
        or not any(
            endpoint[ConfigFields.ID] in endpoint_tags[tag]
            for tag, _endpoint in grouped_endpoints.items()
            if _endpoint[ConfigFields.PEER_TYPE] == PeerType.TAG
        )
    }

    return result


def transform_p2m_connections(all_agents, connections, reference=None, group_tags=True):
    """Transforms connections assuming One to many topology(Point to Multipoint). Also, groups agents by tags.

    Args:
        connections (List[AgentConnectionObject]): A list of connections that are assigned to the provided network.
        reference (dict): A dictionary describing reference connections configuration.

    Returns:
        dict: A dictionary with keys as endpoints and values as dicts explaining the endpoint(state, type).
    """
    transformed_connections = {}
    agent_links = defaultdict(dict)
    agents = {}
    services = {}
    # First make agent_id->agent and link->services maps, so that we could
    # find them faster.
    for connection in connections:
        agent_1, agent_2 = connection["agent_1"], connection["agent_2"]
        # We need to map connections in both ways, since it can be either
        # A->Many or Many->A as we get it from the API.
        agents[agent_1["agent_id"]], agents[agent_2["agent_id"]] = agent_1, agent_2
        agent_links[agent_1["agent_id"]][agent_2["agent_id"]] = True
        agent_links[agent_2["agent_id"]][agent_1["agent_id"]] = True
        transformed_services = transform_connection_services(connection)
        services[(agent_1["agent_id"], agent_2["agent_id"])] = transformed_services
        services[(agent_2["agent_id"], agent_1["agent_id"])] = transformed_services[
            ::-1
        ]

    for src, dst in agent_links.items():
        # NOTE: We expect 1 agent to have connections to N other agents, however,
        # sometimes we have N agents that connect to 1 agent, so we have to filter those out.
        dst_first_key = list(dst.keys())[0]
        if (
            len(dst) == 1
            and dst_first_key in agent_links
            and len(agent_links[dst_first_key]) > 1
        ):
            continue
        agent_1 = agents[src]

        connect_to = {
            agent["agent_name"]: {
                ConfigFields.ID: agent["agent_id"],
                ConfigFields.PEER_TYPE: PeerType.ENDPOINT,
                ConfigFields.STATE: PeerState.PRESENT,
                ConfigFields.SERVICES: list(
                    services[(agent_1["agent_id"], agent["agent_id"])][1]
                ),
            }
            for agent in (agents[i] for i in dst.keys())
        }
        agent_services = set()
        for agent in (agents[i] for i in dst.keys()):
            agent_services.update(services[(agent_1["agent_id"], agent["agent_id"])][0])
        # NOTE: This place might be problematic since it will overwrite
        # A->Many if we have OtherMany->A... However, the first if in this loop
        # should filter out these cases.
        transformed_connections[agent_1["agent_name"]] = {
            ConfigFields.ID: agent_1["agent_id"],
            ConfigFields.PEER_TYPE: PeerType.ENDPOINT,
            ConfigFields.STATE: PeerState.PRESENT,
            ConfigFields.SERVICES: list(agent_services),
            ConfigFields.CONNECT_TO: group_agents_by_tags(all_agents, connect_to)
            if group_tags
            else connect_to,
        }
    return transformed_connections


def transform_mesh_connections(
    all_agents, connections, reference=None, group_tags=True
):
    """Transforms connections assuming MESH topology. Also, groups agents by tags.

    NOTE: Even though some connections are missing, this method assumes that every
    endpoint is connected to every other endpoint.

    Args:
        connections (List[AgentConnectionObject]): A list of connections that are assigned to a network.
        reference (dict): A dictionary describing reference connections configuration.

    Returns:
        dict: A dictionary with keys as endpoints and values as dicts explaining the endpoint(state, type).
    """
    transformed_connections = {}
    agents = {}
    services = defaultdict(set)
    for connection in connections:
        agent_1, agent_2 = connection["agent_1"], connection["agent_2"]
        agents[agent_1["agent_id"]], agents[agent_2["agent_id"]] = agent_1, agent_2
        agent_1_services, agent_2_services = transform_connection_services(connection)
        services[agent_1["agent_id"]].update(agent_1_services)
        services[agent_2["agent_id"]].update(agent_2_services)

    # NOTE: Assumes that all peers are interconnected. Will result in all peers being interconnected
    # if we apply the resulting configuration export.
    # Also, it will enable all services for a given endpoint for all connections even if
    # those services are partially enabled to some other endpoints.
    for id, agent in agents.items():
        transformed_connections[agent["agent_name"]] = {
            ConfigFields.ID: id,
            ConfigFields.PEER_TYPE: PeerType.ENDPOINT,
            ConfigFields.STATE: PeerState.PRESENT,
            ConfigFields.SERVICES: list(services[id]),
        }
    return (
        group_agents_by_tags(all_agents, transformed_connections)
        if group_tags
        else transformed_connections
    )


def transform_connections(
    all_agents, connections, topology, reference=None, group_tags=True, silent=False
):
    """Transform Platform's NetworkObject into internal representation that is being used for export and configuration.

    Args:
        connections (List[AgentConnectionObject]): A list of connections that are assigned to the provided network.
        topology (str): Network topology to assume while transforming connections.
        silent (bool, optional): Indicates whether to suppress messages - used with Ansible. Defaults to False.

    Raises:
        ConfigureNetworkError: In case of any errors.

    Returns:
        dict: Returns a dictionary that can be used for network export and/or configuration.
    """
    topology_map = {
        sdk.MetadataNetworkType.P2P: transform_p2p_connections,
        sdk.MetadataNetworkType.P2M: transform_p2m_connections,
        sdk.MetadataNetworkType.MESH: transform_mesh_connections,
    }
    if topology not in topology_map:
        error = f"Network topology {topology} not supported. Skipping."
        if not silent:
            click.secho(error, err=True, fg="yellow")
        else:
            raise ConfigureNetworkError(error)
        return
    return topology_map[topology](
        all_agents, connections, reference=reference, group_tags=group_tags
    )
