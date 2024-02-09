from aws_cdk import aws_ec2 as ec2

# basic VPC configs
VPC1 = 'vpc1'
VPC2 = 'vpc2'
VPC_PEERING = 'vpc_peering'
ADMIN_SERVER = 'adminServer'

ADMIN_SERVER_SG = 'AdminServerSG'

INTERNET_GATEWAY = 'IGW'
NAT_GATEWAY = 'NGW'
REGION = 'eu-central-1'

# Route tables vpc1.
PUBLIC_ROUTE_TABLE_1 = 'public-RT-1'
PRIVATE_ROUTE_TABLE_1 = 'private-RT-1'

ROUTE_TABLES_ID_TO_ROUTES_MAP_1 = {
    PUBLIC_ROUTE_TABLE_1: [
        {
            'destination_cidr_block': '0.0.0.0/0',
            'gateway_id': INTERNET_GATEWAY,
            'router_type': ec2.RouterType.GATEWAY,
        }
    ],
    PRIVATE_ROUTE_TABLE_1: [
        {
            'destination_cidr_block': '0.0.0.0/0',
            'nat_gateway_id': NAT_GATEWAY,
            'router_type': ec2.RouterType.NAT_GATEWAY,
        }
    ],
}

# Route tables vpc2.
PUBLIC_ROUTE_TABLE_2 = 'public-RT-2'
PRIVATE_ROUTE_TABLE_2 = 'private-RT-2'

ROUTE_TABLES_ID_TO_ROUTES_MAP_2 = {
    PUBLIC_ROUTE_TABLE_2: [
        {
            'destination_cidr_block': '10.10.10.0/26',
            'instance_id': ADMIN_SERVER
        }
    ],
    PRIVATE_ROUTE_TABLE_2: [
        {
            'destination_cidr_block': '10.20.20.0/26',
            'instance_id': ADMIN_SERVER
        }
    ],
}

# Subnets VPC1.
PUBLIC_SUBNET_1 = 'public-subnet-1'
PRIVATE_SUBNET_1 = 'private-subnet-1'

SUBNET_CONFIGURATION_1 = {
    PUBLIC_SUBNET_1: {
        'availability_zone': 'eu-central-1a',
        'cidr_block': '10.10.10.0/26',
        'map_public_ip_on_launch': True,
        'route_table_id': PUBLIC_ROUTE_TABLE_1,
    },
    PRIVATE_SUBNET_1: {
        'availability_zone': 'eu-central-1b',
        'cidr_block': '10.10.10.64/26',
        'map_public_ip_on_launch': False,
        'route_table_id': PRIVATE_ROUTE_TABLE_1,
    },
}

# Subnets VPC2.
PUBLIC_SUBNET_2 = 'public-subnet-2'
PRIVATE_SUBNET_2 = 'private-subnet-2'

SUBNET_CONFIGURATION_2 = {
PUBLIC_SUBNET_2: {
        'availability_zone': 'eu-central-1a',
        'cidr_block': '10.20.20.0/26',
        'map_public_ip_on_launch': True,
        'route_table_id': PUBLIC_ROUTE_TABLE_2,
    },
    PRIVATE_SUBNET_2: {
        'availability_zone': 'eu-central-1b',
        'cidr_block': '10.20.20.64/26',
        'map_public_ip_on_launch': False,
        'route_table_id': PRIVATE_ROUTE_TABLE_2,
    }
}