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

subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='LNX-WebServer',
                    map_public_ip_on_launch=True,
                    subnet_type=ec2.SubnetType.PUBLIC,
            ), ec2.SubnetConfiguration(
                name="WorkStations",
                map_public_ip_on_launch=False,
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            )
            ],

subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='WindowsAdminServer',
                    map_public_ip_on_launch=True,
                    subnet_type=ec2.SubnetType.PUBLIC,
            ), ec2.SubnetConfiguration(
                name="rdsDB",
                map_public_ip_on_launch=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
            ],

# ec2.Instance example
windows_server = ec2.CfnInstance(
                    self,
                    config.ADMIN_SERVER,
                    instance_type=ec2.InstanceType.of(
                        ec2.InstanceClass.BURSTABLE2,
                        ec2.InstanceSize.MICRO),
                    machine_image=ec2.WindowsImage(
                        ec2.WindowsVersion.WINDOWS_SERVER_2022_ENGLISH_FULL_BASE
                    ),
                    vpc=self.vpc2,
                    availability_zone=subnet_config['availability_zone'],
                    vpc_subnets=ec2.SubnetSelection(subnets=[self.subnet_id_to_subnet_map_2[subnet_id]]),
                    associate_public_ip_address=True,
                    key_pair=self.key_pair,
                    security_group=self.adminServerSG,
                    block_devices=[ec2.BlockDevice(
                        device_name='/dev/sda1', # Default root volume.
                        volume=ec2.BlockDeviceVolume.ebs(
                            volume_size=30,
                            encrypted=True,
                            delete_on_termination=True,
                        )
                    )]
                )

# Allow RDP access from a trusted source IP address. (Admins home address IP)
windows_server.connections.allow_from(ec2.Peer.ipv4('86.83.75.135/24'), ec2.Port.tcp(3389))
 instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2,
                ec2.InstanceSize.MICRO),
            machine_image=ec2.WindowsImage(
                ec2.WindowsVersion.WINDOWS_SERVER_2022_ENGLISH_FULL_BASE
            ),
            vpc=self.vpc2,
            availability_zone='eu-central-1a',
            vpc_subnets=ec2.SubnetSelection(config.PUBLIC_SUBNET_2),
            associate_public_ip_address=True,
            key_pair=self.key_pair,
            security_group=self.adminServerSG,
            block_devices=[ec2.BlockDevice(
                device_name='/dev/sda1', # Default root volume.
                volume=ec2.BlockDeviceVolume.ebs(
                    volume_size=30,
                    encrypted=True,
                    delete_on_termination=True,
                )
            )]

    AmazonLinuxImage, AmazonLinuxGeneration, InstanceClass, InstanceSize, InstanceType, WindowsImage, WindowsVersion, UserData
            
'''