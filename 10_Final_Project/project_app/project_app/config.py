from aws_cdk import aws_ec2 as ec2

# basic VPC configs
VPC1 = 'vpc1'

INTERNET_GATEWAY_1 = 'IGW1'
NAT_GATEWAY = 'NGW'
REGION = 'eu-central-1'

# route tables vpc1.
PUBLIC_ROUTE_TABLE_1 = 'public-RT-1'
PRIVATE_ROUTE_TABLE_1 = 'private-RT-1'

ROUTE_TABLES_ID_TO_ROUTES_MAP = {
    PUBLIC_ROUTE_TABLE_1: [
        {
            'destination_cidr_block': '0.0.0.0/0',
            'gateway_id': INTERNET_GATEWAY_1,
            'router_type': ec2.RouterType.GATEWAY
        }
    ],
    PRIVATE_ROUTE_TABLE_1: [
        {
            'destination_cidr_block': '0.0.0.0/0',
            'nat_gateway_id': NAT_GATEWAY,
            'router_type': ec2.RouterType.NAT_GATEWAY
        }
    ],
}

# subnets vpc1.
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
    }
}
