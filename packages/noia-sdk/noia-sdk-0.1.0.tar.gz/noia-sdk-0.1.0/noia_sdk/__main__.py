#!/usr/bin/env python
import functools
import os
from datetime import datetime, timedelta

import click
import yaml

import noia_sdk as sdk
from noia_sdk.rest import ApiException
from noia_sdk.utils import *


def noia_api(func):
    """Helper decorator that injects ApiClient instance into the arguments"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        API_URL = os.environ.get(EnvVars.NOIA_API_SERVER)
        API_KEY = os.environ.get(EnvVars.NOIA_TOKEN)

        if API_URL is None:
            click.secho(
                f"{EnvVars.NOIA_API_SERVER} environment variable is missing.",
                err=True,
                fg="red",
            )
            raise SystemExit(1)

        config = sdk.Configuration()
        config.host = API_URL
        config.api_key["Authorization"] = API_KEY
        api = sdk.ApiClient(config)

        try:
            return func(*args, api=api, **kwargs)
        except ApiException as err:
            click.secho("API error occured", err=True, fg="red")
            click.secho(f"Reason: {str(err)}", err=True, fg="red")
        finally:
            del api
        raise SystemExit(2)

    return wrapper


def noia_platform(func):
    """Helper decorator that injects PlatformApi instance into the arguments"""

    @functools.wraps(func)
    def wrapper(*args, api=None, **kwargs):
        if os.environ.get(EnvVars.NOIA_TOKEN) is None:
            click.secho(
                f"{EnvVars.NOIA_TOKEN} environment variable is missing.",
                err=True,
                fg="yellow",
            )
        try:
            api = sdk.PlatformApi(api)
            return func(*args, platform=api, **kwargs)
        except:
            raise
        finally:
            del api

    return noia_api(wrapper)


def collect_endpoint_services(services):
    services = ", ".join({service["agent_service_name"] for service in services})
    return services if services else "-"


def collect_connection_services(services):
    service_map = {}
    state_map = {
        sdk.AgentConnectionStatus.PENDING: "~",
        sdk.AgentConnectionStatus.WARNING: "*",
        sdk.AgentConnectionStatus.ERROR: "!",
        sdk.AgentConnectionStatus.CONNECTED: "^",
        sdk.AgentConnectionStatus.OFFLINE: "#",
    }
    for service in (
        services["agent_1"]["agent_services"] + services["agent_2"]["agent_services"]
    ):
        for subnet in service["agent_service_subnets"]:
            service_map[subnet["agent_service_subnet_id"]] = service[
                "agent_service_name"
            ]
    services = {
        f"{service_map[subnet['agent_service_subnet_id']]}{state_map.get(subnet['agent_connection_subnet_status'], '?')}"
        for subnet in services["agent_connection_subnets"]
        if subnet["agent_connection_subnet_is_enabled"]
    }
    return ", ".join(services) if services else "-"


@click.group()
def apis():
    """NOIA Networks cli tool"""


@apis.command()
@click.argument("username", nargs=1)
@click.argument("password", nargs=1, default=None, required=False)
@noia_api
def login(username, password, api):
    """Login with username and password.

    Will retrieve access token and print it to stdout. You can provide the password as a second parameter
    or type it when prompted if the password is not provided.

    \b
    Example:
        noiactl login MyUser@example.com MyPassword

        \b
        noiactl login MyUser@example.com
        Password: <type your password here>
    """
    if not password:
        password = click.prompt("Password", default=None, hide_input=True)

    if password is None:
        return

    payload = {"user_email": username, "user_password": password, "additionalProp1": {}}
    api = sdk.AuthApi(api)
    try:
        token = api.local(body=payload)
        click.echo(token["refresh_token"])
    except ApiException as err:
        click.secho("Login was not successful", err=True, fg="red")
        click.secho(f"Reason: {str(err)}", err=True, fg="red")
        raise SystemExit(1)


@apis.command()
@click.option(
    "--show-secret", "-s", is_flag=True, default=False, help="Shows API secrets"
)
@click.option("--skip", default=0, type=int, help="Skip N API keys")
@click.option("--take", default=128, type=int, help="Take N API keys")
@click.option(
    "--json",
    "-j",
    is_flag=True,
    default=False,
    help="Outputs a JSON instead of a table",
)
@noia_platform
def get_api_keys(show_secret, skip, take, json, platform):
    """List all API keys.

    API keys are being used by the endpoint agent to connect to the NOIA platform.

    By default this command will retrieve up to 128 API keys. You can use --take parameter to get more keys.
    """
    keys = platform.index_api_key(skip=skip, take=take)["data"]

    fields = [
        ("Organization ID", "api_key_id"),
        ("User ID", "user_id"),
        ("Key ID", "api_key_id"),
        ("Key Name", "api_key_name"),
        ("Is Suspended", "api_key_is_suspended", lambda x: x and "Yes" or "No"),
        ("Status", "api_key_status", lambda x: x and "Ok" or "Err"),
        ("Secret", "api_key_secret", lambda x: show_secret and x or "-"),
        ("Created At", "api_key_created_at"),
        ("Updated At", "api_key_updated_at"),
        ("Expires At", "api_key_valid_until"),
    ]
    print_table(keys, fields, to_json=json)


@apis.command()
@click.argument("name")
@click.argument(
    "expires",
    type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]),
    default=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
)
@click.option("--suspended", "-s", is_flag=True, help="Create a suspended API key")
@noia_platform
def create_api_key(name, suspended, expires, platform):
    """Create a API key."""
    body = {
        "api_key_name": name,
        "api_key_is_suspended": suspended,
        "api_key_valid_until": expires,
    }
    result = platform.create_api_key(body=body)
    click.echo(result["data"]["api_key_id"])


@apis.command()
@click.option("--name", default=None, type=str)
@click.option("--id", default=None, type=int)
@noia_platform
def delete_api_key(name, id, platform):
    """Delete API key either by name or by id. If there are multiple names - please use id."""
    if name is None and id is None:
        click.secho("Either API key name or id must be specified.", err=True, fg="red")
        raise SystemExit(1)

    if id is None:
        keys = platform.index_api_key()["data"]
        id = find_by_name(keys, name, "api_key")
        if id is None:
            raise SystemExit(1)

    platform.delete_api_key(id)


@apis.command()
@click.option("--name", default=None, type=str, help="Filter endpoints by name")
@click.option("--id", default=None, type=int, help="Filter endpoints by IDs")
@click.option(
    "--network", default=None, type=str, help="Filter endpoints by network name"
)
@click.option("--tag", default=None, type=str, help="Filter endpoints by tag")
@click.option("--skip", default=0, type=int, help="Skip N endpoints")
@click.option("--take", default=42, type=int, help="Take N endpoints")
@click.option(
    "--show-services",
    is_flag=True,
    default=False,
    help="Retrieves services that are configured for each endpoint",
)
@click.option(
    "--online", is_flag=True, default=False, help="List only online endpoints"
)
@click.option(
    "--offline", is_flag=True, default=False, help="List only offline endpoints"
)
@click.option(
    "--json",
    "-j",
    is_flag=True,
    default=False,
    help="Outputs a JSON instead of a table",
)
@noia_platform
def get_endpoints(
    name, id, tag, network, skip, take, show_services, online, offline, json, platform
):
    """List all endpoints.

    By default this command will retrieve up to 42 endpoints. You can use --take parameter to get more endpoints.
    """
    filters = []
    if name:
        filters.append(f"id|name:{name}")
    elif id:
        filters.append(f"ids[]:{id}")
    if tag:
        filters.append(f"tags_names[]:{tag}")
    if network:
        filters.append(f"networks_names[]:{network}")
    agents = platform.index_agents(
        filter=",".join(filters) if filters else None, skip=skip, take=take
    )["data"]

    if online or offline:
        filtered_agents = []
        is_online = online and not offline
        while agents and len(filtered_agents) < take:
            filtered_agents += [
                agent for agent in agents if agent["agent_is_online"] == is_online
            ]
            if len(filtered_agents) < take:
                skip += take
                agents = platform.index_agents(
                    filter=",".join(filters) if filters else None, skip=skip, take=take
                )["data"]
        agents = filtered_agents

    fields = [
        ("Agent ID", "agent_id"),
        ("Name", "agent_name"),
        ("Public IP", "agent_public_ipv4"),
        ("Provider", ("agent_provider", "agent_provider_name")),
        ("Location", "agent_location_city"),
        ("Online", "agent_is_online"),
        (
            "Tags",
            "agent_tags",
            lambda x: x and ", ".join(i["agent_tag_name"] for i in x) or "-",
        ),
    ]

    if show_services:
        ids = [agent["agent_id"] for agent in agents]
        agents_services = BatchedRequest(
            platform.get_agent_services_with_subnets,
            max_payload_size=MAX_QUERY_FIELD_SIZE,
        )(ids)["data"]
        agent_services = defaultdict(list)
        for agent in agents_services:
            agent_services[agent["agent_id"]].append(agent)
        agents = [
            {
                **agent,
                "agent_services": agent_services.get(agent["agent_id"], []),
            }
            for agent in agents
        ]
        fields.append(("Services", "agent_services", collect_endpoint_services))

    print_table(agents, fields, to_json=json)


@apis.command()
@click.option(
    "--json",
    "-j",
    is_flag=True,
    default=False,
    help="Outputs a JSON instead of a table",
)
@noia_platform
def get_topology(json, platform):
    """Retrieves networks topology."""
    topology = platform.topology_networks()["data"]

    fields = [
        ("Network name", "network_name"),
        ("Network type", "network_type"),
        ("Network ID", "network_id"),
        ("Gateway ID", "agent_gateway_id"),
        ("N# of endpoints", "network_agents_count"),
        ("N# of connections", "network_agent_connections_count"),
    ]
    print_table(topology, fields, to_json=json)


@apis.command()
@click.option(
    "--network", default=None, type=str, help="Filter connections by network name or ID"
)
@click.option("--id", default=None, type=int, help="Filter endpoints by ID")
@click.option("--skip", default=0, type=int, help="Skip N connections")
@click.option("--take", default=42, type=int, help="Take N connections")
@click.option(
    "--show-services",
    is_flag=True,
    default=False,
    help="Retrieves services that are configured for each endpoint",
)
@click.option(
    "--json",
    "-j",
    is_flag=True,
    default=False,
    help="Outputs a JSON instead of a table",
)
@noia_platform
def get_connections(network, id, skip, take, show_services, json, platform):
    """Retrieves network connections.

    Connection service status is added to the end of the service name with the following possible symbols:

    \b
    ^ - Connection is online.
    ! - There was an error establishing the connection
    # - Connection is offline
    * - Connection is in warning state
    ~ - Connection is being established
    ? - Unknown state

    By default this command will retrieve up to 42 connections. You can use --take parameter to get more connections.
    """
    filters = []
    if network:
        try:
            filters.append(f"networks[]:{int(network)}")
        except ValueError:
            networks = platform.index_networks(filter=f"id|name:{network}")["data"]
            filters.append(
                f"networks[]:{','.join(str(net['network_id']) for net in networks)}"
            )

    if id:
        filters.append(f"id|name:{id}")
    connections = platform.index_connections(
        filter=",".join(filters) if filters else None,
        skip=skip,
        take=take,
    )["data"]
    fields = [
        ("ID", "agent_connection_id"),
        ("Endpoint 1", ("agent_1", "agent_name")),
        ("IP 1", ("agent_1", "agent_public_ipv4")),
        ("Endpoint 2", ("agent_2", "agent_name")),
        ("IP 2", ("agent_2", "agent_public_ipv4")),
        ("Status", "agent_connection_status"),
        ("Network name", "network_name"),
        ("Network type", "network_type"),
        ("Network ID", "network_id"),
        ("Gateway ID", "agent_gateway_id"),
        ("Created At", "agent_connection_created_at"),
        ("Modified At", "agent_connection_modified_at"),
        ("SDN Policy ID", "agent_sdn_policy_id"),
        ("Link Tag", "agent_connection_link_tag"),
        ("Last Handshake", "agent_connection_last_handshake"),
        ("TX total", "agent_connection_tx_bytes_total"),
        ("RX total", "agent_connection_rx_bytes_total"),
        ("Latency", "agent_connection_latency_ms"),
        ("Packet Loss", "agent_connection_packet_loss"),
    ]

    if show_services:
        ids = [connection["agent_connection_id"] for connection in connections]
        connections_services = BatchedRequest(
            platform.get_connection_services, max_payload_size=MAX_QUERY_FIELD_SIZE
        )(ids)["data"]
        connection_services = {
            connection["agent_connection_id"]: connection
            for connection in connections_services
        }
        connections = [
            {
                **connection,
                "agent_connection_services": connection_services[
                    connection["agent_connection_id"]
                ],
            }
            for connection in connections
        ]
        fields.append(
            ("Services", "agent_connection_services", collect_connection_services)
        )

    print_table(connections, fields, to_json=json)


@apis.command()
@click.argument("network")
@click.argument("agents", nargs=-1)
@click.option(
    "--use-names",
    is_flag=True,
    default=False,
    help="Use network and agent's names instead of ids. Will not work with name duplicates.",
)
@click.option(
    "--json",
    "-j",
    is_flag=True,
    default=False,
    help="Outputs a JSON instead of a table",
)
@noia_platform
def create_connections(network, agents, use_names, json, platform):
    """Create connections between endpoints. Number of endpoints must be even.

    \b
    Arguments:
        network - either a network name or ID
        agents - a list of endpoint ids or names separated by spaces

    In order to use endpoint names instead of ids provide --use-names option.

    Example:

        noiactl create-connections MyNetworkName 1 2 3 4 5 6 7 8

        This command will create 4 connections from Endpoint 1 to Endpoint 2 like this:

        \b
        Endpoint 1 ID | Endpoint 2 ID
        1             | 2
        3             | 4
        5             | 6
        7             | 8
    """

    networks = platform.index_networks(filter=f"id|name:{network}")["data"]
    if len(networks) != 1:
        click.secho(f"Could not find the network {network}", err=True, fg="red")
        raise SystemExit(1)

    network = networks[0]["network_id"]
    network_type = networks[0]["network_type"]
    if use_names:
        all_agents = platform.index_agents(take=TAKE_MAX_ITEMS_PER_CALL)["data"]
        agents = find_by_name(all_agents, agents, "agent")
        if any(i is None for i in agents):
            raise SystemExit(1)
    else:
        try:
            agents = [int(i) for i in agents]
        except ValueError:
            click.secho("Invalid agent id", err=True, fg="red")
            raise SystemExit(1)

    if network_type == sdk.NetworkType.POINT_TO_POINT:
        if len(agents) == 0 or len(agents) % 2 != 0:
            click.secho("Number of agents must be even.", err=True, fg="red")
            raise SystemExit(1)
        agents = list(zip(agents[:-1:2], agents[1::2]))

    body = {
        "network_id": network,
        "agent_ids": agents,
        "network_update_by": sdk.NetworkGenesisType.SDK,
    }
    connections = platform.create_connections(body=body)["data"]

    fields = [
        ("Connection ID", "agent_connection_id"),
        ("Endpoint 1 ID", "agent_1_id"),
        ("Endpoint 1 WG", "agent_wg_1_id"),
        ("Endpoint 2 ID", "agent_2_id"),
        ("Endpoint 2 WG", "agent_wg_2_id"),
        ("Network ID", "network_id"),
    ]
    print_table(connections, fields, to_json=json)


@apis.command()
@click.argument("id", type=int)
@noia_platform
def delete_connection(id, platform):
    """Delete a connection."""
    platform.delete_connection(id)


@apis.command()
@click.option("--network", default=None, type=str, help="Filter networks by name/ID")
@click.option(
    "--show-secret", "-s", is_flag=True, default=False, help="Shows Network secrets"
)
@click.option("--skip", default=0, type=int, help="Skip N networks")
@click.option("--take", default=42, type=int, help="Take N networks")
@click.option(
    "--json",
    "-j",
    is_flag=True,
    default=False,
    help="Outputs a JSON instead of a table",
)
@noia_platform
def get_networks(network, show_secret, skip, take, json, platform):
    """List all networks.

    By default this command will retrieve up to 42 networks. You can use --take parameter to get more networks.
    """
    networks = platform.index_networks(
        filter=f"id|name:{network}" if network else None,
        skip=skip,
        take=take,
    )["data"]

    fields = [
        ("Organization ID", "organization_id"),
        ("User ID", "user_id"),
        ("Agent Gateway ID", "agent_gateway_id"),
        ("Network ID", "network_id"),
        ("Network Name", "network_name"),
        ("Network Type", "network_type"),
        ("Network Topology", ("network_metadata", "network_type")),
        ("Network Secret", "network_key", lambda x: show_secret and x or "-"),
        (
            "SDN Connections",
            "network_disable_sdn_connections",
            lambda x: x and "Disabled" or "Enabled",
        ),
        ("Created At", "network_created_at"),
        ("Updated At", "network_updated_at"),
        ("Created By", ("network_metadata", "network_created_by")),
        ("Updated By", ("network_metadata", "network_updated_by")),
    ]
    print_table(networks, fields, to_json=json)


@apis.command()
@click.argument("name")
@click.option(
    "--network-type",
    default=sdk.NetworkType.POINT_TO_POINT,
    help="Low level network type.",
    hidden=True,
)
@click.option(
    "--gateway-id",
    default=0,
    type=int,
    help="Endpoint ID to use as gateway for GATEWAY network type.",
    hidden=True,
)
@click.option(
    "--topology",
    default=sdk.MetadataNetworkType.P2P,
    help="Specifies Network Topology that is used by configure-networks or Ansible playbooks.",
)
@click.option(
    "--disable-sdn-connections",
    is_flag=True,
    default=True,
    help="Disable SDN connections. Default is disable.",
    hidden=True,
)
@noia_platform
def create_network(
    name, network_type, topology, gateway_id, disable_sdn_connections, platform
):
    """Create a network.

    Possible network topologies are P2P, P2M, MESH. The network topology is mainly used for
    Network as Code usage scenarious.

    \b
    P2P - used to configure the network using endpoint pairs.
    P2M - used to configure the network when one endpoint connects to many endpoints.
    MESH - used to configure the network where every endpoint is connected to every other endpoint.

    \b
    Examples:
        # Create a network with P2P topology
        noiactl create-network MyNetworkName

    \b
        # Create a network with MESH topology
        noiactl create-network MyNetworkName --topology MESH

    """
    if network_type not in ALLOWED_NETWORK_TYPES:
        click.secho(f"Network type {network_type} is not allowed.", err=True, fg="red")
        raise SystemExit(1)

    topology = topology.upper() if topology else topology
    if topology is not None and topology not in ALLOWED_NETWORK_TOPOLOGIES:
        click.secho(f"Network topology {topology} is not allowed.", err=True, fg="red")
        raise SystemExit(1)

    body = {
        "network_name": name,
        "network_type": network_type,
        "agent_gateway_id": gateway_id,
        "network_disable_sdn_connections": disable_sdn_connections,
        "network_metadata": {
            "network_created_by": sdk.NetworkGenesisType.SDK,
            "network_type": topology,
        },
    }
    result = platform.create_network(body=body)
    click.echo(result["data"]["network_id"])


@apis.command()
@click.argument("network")
@noia_platform
def delete_network(network, platform):
    """Delete a network."""
    networks = platform.index_networks(filter=f"id|name:{network}")["data"]

    if len(networks) > 1:
        click.echo(f"Found {len(networks)} networks by name {network}.")
    elif not networks:
        click.secho(
            f"Could not find a network by id/name {network}.", err=True, fg="red"
        )
        raise SystemExit(1)

    for net in networks:
        platform.delete_networks(net["network_id"])


@apis.command()
@click.argument("config")
@click.option(
    "--network",
    default=None,
    type=str,
    help="Filter configuration file networks by name",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Perform a dry run without configuring anything.",
)
@click.option(
    "--json",
    "-j",
    "from_json",
    is_flag=True,
    default=False,
    help="Imports configuration from JSON instead of YAML",
)
@noia_platform
def configure_networks(config, network, dry_run, from_json, platform):
    """Configure networks using a configuration YAML/JSON file.

    \b
    Example YAML file:
        name: test-network
        state: present
        topology: P2M
        connections:
            gateway-endpoint:
                state: present
                type: endpoint
                services:
                - postgres
                - redis
                connect_to:
                    endpoint-1:
                        type: endpoint
                        services:
                        - app
                    endpoint2:
                        state: present
                        type: endpoint
                        services:
                        - app
    """
    with open(config, "rb") as cfg_file:
        if from_json:
            config = json.load(cfg_file)
            config = config if isinstance(config, list) else [config]
        else:
            config = list(yaml.safe_load_all(cfg_file))

    for index, net in enumerate(config):
        if any(i not in net for i in ("name", "topology", "state")):
            click.secho(
                f"Skipping {index} entry as no name, topology or state found.",
                fg="yellow",
            )
            continue
        if (network and network in net["name"]) or not network:
            configure_network(platform, net, dry_run)

    click.secho("Done", fg="green")


@apis.command()
@click.option("--network", default=None, type=str, help="Filter networks by name or ID")
@click.option("--skip", default=0, type=int, help="Skip N networks")
@click.option("--take", default=42, type=int, help="Take N networks")
@click.option("--topology", default=None, type=str, help="Override network topology")
@click.option(
    "--json",
    "-j",
    "to_json",
    is_flag=True,
    default=False,
    help="Outputs a JSON instead of YAML",
)
@noia_platform
def export_networks(network, skip, take, topology, to_json, platform):
    """Exports existing networks to configuration YAML/JSON file.

    If the network was created via UI or manually with complex topology in order
    to get full export, you might want to override the topology.

    If exact topology export is required - use P2P topology.

    By default this command will retrieve up to 42 networks. You can use --take parameter to get more networks.
    """
    if topology:
        topology = topology.upper()
        if topology not in ALLOWED_NETWORK_TOPOLOGIES:
            click.secho(
                f"Network topology {topology} not supported. Skipping.",
                err=True,
                fg="red",
            )
            return

    networks = [
        transform_network(net)
        for net in platform.index_networks(
            filter=f"id|name:{network}" if network else None,
            skip=skip,
            take=take,
        )["data"]
    ]
    if not networks:
        return

    all_agents = WithRetry(platform.index_agents)(take=TAKE_MAX_ITEMS_PER_CALL)["data"]
    all_agents = {agent["agent_id"]: agent for agent in all_agents}

    for net in networks:
        connections_filter = f"networks[]:{net['id']}"
        connections = WithRetry(platform.index_connections)(
            filter=connections_filter, take=TAKE_MAX_ITEMS_PER_CALL
        )["data"]
        ids = [connection["agent_connection_id"] for connection in connections]
        if ids:
            connections_services = BatchedRequest(
                platform.get_connection_services, max_payload_size=MAX_QUERY_FIELD_SIZE
            )(ids)["data"]
            connection_services = {
                connection["agent_connection_id"]: connection
                for connection in connections_services
            }
        net_connections = [
            {
                **connection,
                "agent_connection_services": connection_services.get(
                    connection["agent_connection_id"], {}
                ),
            }
            for connection in connections
            if connection["network_id"] == net["id"]
        ]
        transformed_connections = transform_connections(
            all_agents,
            net_connections,
            topology if topology else net[ConfigFields.TOPOLOGY],
        )
        if transformed_connections:
            net[ConfigFields.CONNECTIONS] = transformed_connections
        if topology:
            net["topology"] = topology
        del net["use_sdn"]

    if to_json:
        click.echo(json.dumps(networks, indent=4))
    else:
        click.echo(yaml.dump_all(networks))


def main():
    apis(prog_name="noiactl")


if __name__ == "__main__":
    main()
