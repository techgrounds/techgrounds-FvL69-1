'''
VPC2 = 'vpc2'

INTERNET_GATEWAY_2 = 'IGW2'

# route tables vpc2.
PUBLIC_ROUTE_TABLE_2 = 'public-RT-2'
PRIVATE_ROUTE_TABLE_2 = 'private-RT-2'

ROUTE_TABLES_ID_TO_ROUTES_MAP_2 = {
    PUBLIC_ROUTE_TABLE_2: [
        {
            'destination_cidr_block': '0.0.0.0/0',
            'gateway_id': INTERNET_GATEWAY_2,
            'router_type': ec2.RouterType.GATEWAY
        }
    ],
    PRIVATE_ROUTE_TABLE_2: [
        {
            'destination_cidr_block': '0.0.0.0/0',
        }
    ],
}

# subnets vpc2.
PUBLIC_SUBNET_2 = 'public-subnet-1'
PRIVATE_SUBNET_2 = 'private-subnet-1'

SUBNET_CONFIGURATION_2 = {
    PUBLIC_SUBNET_2: {
        'availability_zone': 'eu-central-1a',
        'cidr_block': '10.10.10.0/26',
        'map_public_ip_on_launch': True,
        'route_table_id': PUBLIC_ROUTE_TABLE_2,
    },
    PRIVATE_SUBNET_2: {
        'availability_zone': 'eu-central-1b',
        'cidr_block': '10.10.10.64/26',
        'map_public_ip_on_launch': False,
        'route_table_id': PRIVATE_ROUTE_TABLE_2,
    }
}

#print(kwargs)
                if route['router_type'] == ec2.RouterType.GATEWAY:
                    kwargs['gateway_id'] = self.internet_gateway_1.ref
                if route['router_type'] == ec2.RouterType.NAT_GATEWAY:
                    kwargs['nat_gateway_id'] = self.nat_gateway.ref
                del kwargs['router_type']
'''