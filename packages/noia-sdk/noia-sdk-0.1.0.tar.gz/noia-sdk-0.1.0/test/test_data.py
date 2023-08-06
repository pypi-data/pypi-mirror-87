import functools

TEST_YAML = """---
# Create connection between IoT devices and IoT load balancer
name: edge_to_lb
state: present
use_sdn: true
# Connect devices only through SDN, skip public internet
use_public: false
# SDN connection count - how many failover paths to create
sdn_path_count: 3
# Latency threshold, %
latency_threshold: 10
# Packet loss threshold, %
pl_threshold: 1
topology: p2m
connections:
  de-aws-lb01:
    type: endpoint
# Allow IoT devices to access 2 services: haproxy load balancer and MQTT broker
    services: 
      - haproxy
      - mqtt
    connect_to:
      iot_device:
# Connect all endpoints tagged as iot_device
        type: tag
# Allow ssh connection from lb to devices
        services: ssh
"""

INDEX_NETWORKS = {
    "data": [
        {
            "network_name": "skip",
            "network_id": 321,
            "network_type": "POINT_TO_POINT",
            "network_disable_sdn_connections": False,
            "network_metadata": {
                "network_type": "P2P",
            },
        },
        {
            "network_name": "test",
            "network_id": 123,
            "network_type": "POINT_TO_POINT",
            "network_disable_sdn_connections": False,
            "network_metadata": {
                "network_type": "MESH",
            },
        },
        {
            "network_name": "test",
            "network_id": 456,
            "network_type": "MESH",
            "network_disable_sdn_connections": False,
        },
    ]
}
P2P_CONNECTIONS = [
    {
        "agent_connection_id": 1,
        "network_id": 321,
        "agent_1": {
            "agent_id": 1,
            "agent_name": "de-hetzner-db01",
        },
        "agent_2": {
            "agent_id": 2,
            "agent_name": "de-aws-be01",
        },
    },
    {
        "agent_connection_id": 2,
        "network_id": 321,
        "agent_1": {
            "agent_id": 3,
            "agent_name": "de-aws-lb01",
        },
        "agent_2": {
            "agent_id": 4,
            "agent_name": "kr-aws-dns01",
        },
    },
]
P2M_CONNECTIONS = [
    {
        "agent_connection_id": 3,
        "network_id": 321,
        "agent_1": {
            "agent_id": 1,
            "agent_name": "auto gen 1",
        },
        "agent_2": {
            "agent_id": 4,
            "agent_name": "auto gen 4",
        },
    },
    {
        "agent_connection_id": 4,
        "network_id": 321,
        "agent_1": {
            "agent_id": 1,
            "agent_name": "auto gen 1",
        },
        "agent_2": {
            "agent_id": 5,
            "agent_name": "auto gen 5",
        },
    },
    {
        "agent_connection_id": 5,
        "network_id": 321,
        "agent_1": {
            "agent_id": 1,
            "agent_name": "auto gen 1",
        },
        "agent_2": {
            "agent_id": 6,
            "agent_name": "auto gen 6",
        },
    },
]
MESH_CONNECTIONS = [
    {
        "agent_connection_id": 6,
        "network_id": 321,
        "agent_1": {
            "agent_id": 13,
            "agent_name": "iot_mqtt",
        },
        "agent_2": {
            "agent_id": 10,
            "agent_name": "iot_device1",
        },
    },
    {
        "agent_connection_id": 7,
        "network_id": 321,
        "agent_1": {
            "agent_id": 13,
            "agent_name": "iot_mqtt",
        },
        "agent_2": {
            "agent_id": 11,
            "agent_name": "iot_device2",
        },
    },
    {
        "agent_connection_id": 8,
        "network_id": 321,
        "agent_1": {
            "agent_id": 13,
            "agent_name": "iot_mqtt",
        },
        "agent_2": {
            "agent_id": 10,
            "agent_name": "iot_device2",
        },
    },
    {
        "agent_connection_id": 9,
        "network_id": 321,
        "agent_1": {
            "agent_id": 13,
            "agent_name": "iot_mqtt",
        },
        "agent_2": {
            "agent_id": 12,
            "agent_name": "iot_device3",
        },
    },
    {
        "agent_connection_id": 10,
        "network_id": 321,
        "agent_1": {
            "agent_id": 10,
            "agent_name": "iot_device1",
        },
        "agent_2": {
            "agent_id": 12,
            "agent_name": "iot_device3",
        },
    },
]
CREATED_CONNECTIONS = [
    {
        "agent_connection_id": 10,
        "network_id": 321,
        "agent_1": {
            "agent_id": 13,
            "agent_name": "iot_mqtt",
        },
        "agent_2": {
            "agent_id": 10,
            "agent_name": "iot_device1",
        },
    },
    {
        "agent_connection_id": 7,
        "network_id": 321,
        "agent_1": {
            "agent_id": 13,
            "agent_name": "iot_mqtt",
        },
        "agent_2": {
            "agent_id": 11,
            "agent_name": "iot_device2",
        },
    },
    {
        "agent_connection_id": 8,
        "network_id": 321,
        "agent_1": {
            "agent_id": 13,
            "agent_name": "iot_mqtt",
        },
        "agent_2": {
            "agent_id": 10,
            "agent_name": "iot_device2",
        },
    },
]


def create_agent_subnets(id, name, subnets=24):
    if not isinstance(subnets, (list, tuple)):
        subnets = (subnets,)
    return {
        "agent_service_id": id,
        "agent_service_name": name,
        "agent_service_type": "DOCKER",
        "agent_service_is_active": True,
        "agent_service_subnets": [
            {
                "agent_service_subnet_id": subnet,
                "agent_service_subnet_ip": f"172.18.0.{subnet}",
                "agent_service_subnet_is_active": True,
            }
            for subnet in subnets
        ],
    }


def create_agent_connection_subnets(subnets, enabled_flags):
    return [
        {
            "agent_connection_subnet_id": id,
            "agent_service_subnet_id": subnet,
            "agent_connection_subnet_status": "ERROR",
            "agent_connection_subnet_is_enabled": enabled,
            "agent_connection_subnet_error": "Some message",
        }
        for id, (subnet, enabled) in enumerate(zip(subnets, enabled_flags))
    ]


AGENT_CONNECTION_SUBNETS_1 = [
    {
        "agent_connection_subnet_id": 14,
        "agent_service_subnet_id": 21,
        "agent_connection_subnet_status": "ERROR",
        "agent_connection_subnet_is_enabled": True,
        "agent_connection_subnet_error": "Agent '9' service ip: 172.18.0.5 intersects network CIDRS: 172.18.0.0/16",
    },
    {
        "agent_connection_subnet_id": 31,
        "agent_service_subnet_id": 22,
        "agent_connection_subnet_status": "PENDING",
        "agent_connection_subnet_is_enabled": False,
        "agent_connection_subnet_error": "Agent '22' service ip: 172.17.0.2 intersects network CIDRS: 172.17.0.0/16",
    },
    {
        "agent_connection_subnet_id": 40,
        "agent_service_subnet_id": 23,
        "agent_connection_subnet_status": "ERROR",
        "agent_connection_subnet_is_enabled": True,
        "agent_connection_subnet_error": "Agent '22' service ip: 172.19.0.3 intersects network CIDRS: 172.19.0.0/16",
    },
    {
        "agent_connection_subnet_id": 39,
        "agent_service_subnet_id": 24,
        "agent_connection_subnet_status": "ERROR",
        "agent_connection_subnet_is_enabled": True,
        "agent_connection_subnet_error": "Agent '22' service ip: 172.18.0.5 intersects network CIDRS: 172.18.0.0/16",
    },
    {
        "agent_connection_subnet_id": 38,
        "agent_service_subnet_id": 25,
        "agent_connection_subnet_status": "ERROR",
        "agent_connection_subnet_is_enabled": True,
        "agent_connection_subnet_error": "Agent '22' service ip: 172.18.0.5 intersects network CIDRS: 172.18.0.0/16",
    },
]
AGENT_CONNECTION_SUBNETS_2 = [
    {
        "agent_connection_subnet_id": 14,
        "agent_service_subnet_id": 21,
        "agent_connection_subnet_status": "ERROR",
        "agent_connection_subnet_is_enabled": False,
        "agent_connection_subnet_error": "Agent '9' service ip: 172.18.0.5 intersects network CIDRS: 172.18.0.0/16",
    },
    {
        "agent_connection_subnet_id": 31,
        "agent_service_subnet_id": 22,
        "agent_connection_subnet_status": "PENDING",
        "agent_connection_subnet_is_enabled": False,
        "agent_connection_subnet_error": "Agent '22' service ip: 172.17.0.2 intersects network CIDRS: 172.17.0.0/16",
    },
    {
        "agent_connection_subnet_id": 40,
        "agent_service_subnet_id": 23,
        "agent_connection_subnet_status": "ERROR",
        "agent_connection_subnet_is_enabled": True,
        "agent_connection_subnet_error": "Agent '22' service ip: 172.19.0.3 intersects network CIDRS: 172.19.0.0/16",
    },
    {
        "agent_connection_subnet_id": 39,
        "agent_service_subnet_id": 24,
        "agent_connection_subnet_status": "ERROR",
        "agent_connection_subnet_is_enabled": True,
        "agent_connection_subnet_error": "Agent '22' service ip: 172.18.0.5 intersects network CIDRS: 172.18.0.0/16",
    },
    {
        "agent_connection_subnet_id": 38,
        "agent_service_subnet_id": 25,
        "agent_connection_subnet_status": "ERROR",
        "agent_connection_subnet_is_enabled": False,
        "agent_connection_subnet_error": "Agent '22' service ip: 172.18.0.5 intersects network CIDRS: 172.18.0.0/16",
    },
]
CONNECTION_SERVICES = {
    "agent_connection_id": 169,
    "agent_connection_subnets": [],
    "agent_1": {
        "agent_id": 9,
        "agent_services": [
            {
                "agent_service_id": 16,
                "agent_service_name": "nats-streaming",
                "agent_service_type": "DOCKER",
                "agent_service_is_active": True,
                "agent_service_subnets": [
                    {
                        "agent_service_subnet_id": 21,
                        "agent_service_subnet_ip": "172.18.0.11",
                        "agent_service_subnet_is_active": True,
                    },
                    {
                        "agent_service_subnet_id": 22,
                        "agent_service_subnet_ip": "172.17.0.3",
                        "agent_service_subnet_is_active": True,
                    },
                ],
            },
            {
                "agent_service_id": 21,
                "agent_service_name": "sdn-bi",
                "agent_service_type": "DOCKER",
                "agent_service_is_active": True,
                "agent_service_subnets": [
                    {
                        "agent_service_subnet_id": 23,
                        "agent_service_subnet_ip": "172.18.0.5",
                        "agent_service_subnet_is_active": True,
                    }
                ],
            },
            {
                "agent_service_id": 123,
                "agent_service_name": "missing-subnet",
                "agent_service_type": "DOCKER",
                "agent_service_is_active": True,
                "agent_service_subnets": [
                    {
                        "agent_service_subnet_id": 123,
                        "agent_service_subnet_ip": "172.18.0.5",
                        "agent_service_subnet_is_active": True,
                    }
                ],
            },
        ],
    },
    "agent_2": {
        "agent_id": 22,
        "agent_services": [
            {
                "agent_service_id": 13,
                "agent_service_name": "sdn-pgadmin",
                "agent_service_type": "DOCKER",
                "agent_service_is_active": True,
                "agent_service_subnets": [
                    {
                        "agent_service_subnet_id": 24,
                        "agent_service_subnet_ip": "172.18.0.10",
                        "agent_service_subnet_is_active": True,
                    }
                ],
            },
            {
                "agent_service_id": 18,
                "agent_service_name": "streaming",
                "agent_service_type": "DOCKER",
                "agent_service_is_active": True,
                "agent_service_subnets": [
                    {
                        "agent_service_subnet_id": 25,
                        "agent_service_subnet_ip": "172.17.0.3",
                        "agent_service_subnet_is_active": True,
                    },
                ],
            },
        ],
    },
}
P2P_CONNECTIONS_SERVICES = [
    {
        **CONNECTION_SERVICES,
        "agent_connection_id": 1,
        "agent_connection_subnets": AGENT_CONNECTION_SUBNETS_1,
    },
    {
        **CONNECTION_SERVICES,
        "agent_connection_id": 2,
        "agent_connection_subnets": AGENT_CONNECTION_SUBNETS_2,
    },
]
CONFIG_CONNECTIONS = {
    "agent 0": {
        "services": ["a", "b"],
    },
    "agent 1": {
        "services": ["b", "c"],
    },
    "agent 2": {
        "services": ["d", "e"],
    },
    "agent 3": {
        "services": ["f", "g"],
    },
    "agent 4": {
        "services": ["h", "i"],
    },
}
INDEX_CONNECTIONS_EX = {"data": []}
INDEX_AGENTS_EX = {"data": []}


class EqualSets:
    def __init__(self, data):
        self.data = set(data)

    def __eq__(self, ref):
        return set(ref) == self.data


def parametrize(param_list):
    """Decorates a test case to run it as a set of subtests."""

    def decorator(f):
        @functools.wraps(f)
        def wrapped(self, *args):
            for param in param_list:
                with self.subTest(name=str(param)):
                    f(self, *args, *param)

        return wrapped

    return decorator


def index_agents_stub(*args, **kwargs):
    if "filter" not in kwargs:
        return {
            "data": [
                {
                    "agent_name": f"auto gen {i}",
                    "agent_id": i,
                    "agent_tags": [],
                }
                for i in range(256)
            ]
        }
    elif "tags_names[]" in kwargs["filter"]:
        return {
            "data": [
                {
                    "agent_name": f"filter - {kwargs['filter']} {i}",
                    "agent_id": 10 * len(kwargs["filter"]) + i,
                }
                for i in range(3)
            ]
        }
    for i in range(10):
        if f"agent{i}" in kwargs["filter"]:
            return {"data": [{"agent_name": f"agent{i}", "agent_id": i}]}
    return {"data": []}


def connection_services_stub(_, ids):
    return {
        "data": [
            {
                **CONNECTION_SERVICES,
                "agent_connection_id": id,
                "agent_connection_subnets": AGENT_CONNECTION_SUBNETS_2
                if id % 2
                else AGENT_CONNECTION_SUBNETS_1,
            }
            for id in ids
        ]
    }
