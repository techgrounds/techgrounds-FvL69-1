from tkinter import Y
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    )
from constructs import Construct
import project_app.config as config

class ProjectAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Creating vpc1.
        self.vpc1 = ec2.Vpc(
            self,
            config.VPC1,
            ip_addresses=ec2.IpAddresses.cidr('10.10.10.0/25s'),
            availability_zones=['eu-central-1a', 'eu-central-1b'],
            subnet_configuration=[],
            nat_gateways=0,
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )


        # Creating vpc2.
        self.vpc2 = ec2.Vpc(
            self,
            config.VPC2,
            ip_addresses=ec2.IpAddresses.cidr('10.20.20.0/25'),
            availability_zones=['eu-central-1a', 'eu-central-1b'],
            subnet_configuration=[],
            nat_gateways=0,
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )

        # vpc1 attributes and method calls.
        self.subnet_id_to_subnet_map_1 = {}
        self.route_table_id_to_route_table_map_1 = {}

        self.create_subnets_vpc1()
        self.internet_gateway = self.attach_internet_gateway()
        
        self.elastic_ip = ec2.CfnEIP(self, "EIP")
        self.nat_gateway = self.create_nat_gateway()
        self.nat_gateway.add_dependency(self.elastic_ip)
        
        # vpc2 attributes and method calls.
        self.subnet_id_to_subnet_map_2 = {}
        self.route_table_id_to_route_table_map_2 = {}

        self.create_subnets_vpc2()

        # Create AdminServer key-pair.
        self.adminKeyPair = ec2.KeyPair(
            self, 
            "ServerKeyPair",
            key_pair_name='adminServer.kp',
            type=ec2.KeyPairType.RSA,
            format=ec2.KeyPairFormat.PEM
        )

        # Create admin server security group.
        self.adminServerSG = ec2.SecurityGroup (
            self, 
            "AdminServerSG",
            vpc=self.vpc2,
            description="adminServerSecurityGroup",
            allow_all_outbound=True,
            security_group_name='AdminServer'
        )
        # Allow inbound RDP access from a specific IP address.
        self.adminServerSG.add_ingress_rule(ec2.Peer.ipv4('86.83.75.135/24'), ec2.Port.tcp(3389), "AllowRDPAccessFromSpecificIP")
        self.create_admin_server()

        # vpc1 and vpc2.
        self.create_route_tables()
        self.create_subnet_route_tables_associations()

        self.create_routes_vpc1()
        #self.create_routes_vpc2()

        # Create vpc peering.
        self.vpc_peering_connection = ec2.CfnVPCPeeringConnection(
            self,
            config.VPC_PEERING,
            peer_vpc_id=self.vpc2.vpc_id,
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'vpc1_peering_vpc2'}]
        )

        self.routes_to_vpc_peering()

    def routes_to_vpc_peering(self):
        # Create route from public-RT-1 to vpc_peering_connection.
        ec2.CfnRoute(
            self,
            "peeringConnectionRoute1",
            route_table_id=self.route_table_id_to_route_table_map_1[config.PUBLIC_ROUTE_TABLE_1].ref,
            destination_cidr_block='10.20.20.0/26',
            vpc_peering_connection_id=self.vpc_peering_connection.ref
        )
        # Create route from public-RT-2 TO vpc_peering_connection.
        ec2.CfnRoute(
            self,
            "peeringConnectionRoute2",
            route_table_id=self.route_table_id_to_route_table_map_2[config.PUBLIC_ROUTE_TABLE_2].ref,
            destination_cidr_block='10.10.10.0/26',
            vpc_peering_connection_id=self.vpc_peering_connection.ref
        )

    # Create subnets for vpc1.
    def create_subnets_vpc1(self):
        ''' Create subnets for vpc1 '''
        for subnet_id, subnet_config in config.SUBNET_CONFIGURATION_1.items():
            subnet = ec2.CfnSubnet(
                self,
                subnet_id,
                vpc_id=self.vpc1.vpc_id, 
                availability_zone=subnet_config['availability_zone'],
                cidr_block=subnet_config['cidr_block'],
                map_public_ip_on_launch=subnet_config['map_public_ip_on_launch'],
                tags=[{'key': "Name", 'value': subnet_id}]
            )  
            self.subnet_id_to_subnet_map_1[subnet_id] = subnet

    # Create subnets for vpc2.
    def create_subnets_vpc2(self):
        ''' Create subnets for vpc2 '''
        for subnet_id, subnet_config in config.SUBNET_CONFIGURATION_2.items():
            subnet = ec2.CfnSubnet(
                self,
                subnet_id,
                vpc_id=self.vpc2.vpc_id, 
                availability_zone=subnet_config['availability_zone'],
                cidr_block=subnet_config['cidr_block'],
                map_public_ip_on_launch=subnet_config['map_public_ip_on_launch'],
                tags=[{'key': "Name", 'value': subnet_id}]
            )  
            self.subnet_id_to_subnet_map_2[subnet_id] = subnet
        print(self.subnet_id_to_subnet_map_2)

    # Create internet gateway and attach it to vpc1.
    def attach_internet_gateway(self) -> ec2.CfnInternetGateway:
        ''' Create and Attach Internet Gateways vpc1 '''
        internet_gateway = ec2.CfnInternetGateway(
            self,
            config.INTERNET_GATEWAY
        )
        ec2.CfnVPCGatewayAttachment(
            self,
            "internet_gateway_attachment",
            vpc_id=self.vpc1.vpc_id,
            internet_gateway_id=internet_gateway.ref
        )
        return internet_gateway
    
    # Create NAT gateway for public-subnet-1 (vpc1).
    def create_nat_gateway(self) -> ec2.CfnNatGateway:
        ''' Create and Attach NAT Gateway '''
        nat_gateway = ec2.CfnNatGateway(
            self,
            config.NAT_GATEWAY,
            allocation_id=self.elastic_ip.attr_allocation_id,
            subnet_id=self.subnet_id_to_subnet_map_1[config.PUBLIC_SUBNET_1].ref,
        )
        return nat_gateway  
    
    def create_route_tables(self):
        ''' Create Route Tables '''
        # Create route tables for vpc1.
        for route_table_id in config.ROUTE_TABLES_ID_TO_ROUTES_MAP_1:
            self.route_table_id_to_route_table_map_1[route_table_id] = ec2.CfnRouteTable(
                self, 
                route_table_id,
                vpc_id=self.vpc1.vpc_id,
                tags=[{"key": "Name", "value": route_table_id}]
            )
        # Create route tables for vpc2.
        for route_table_id in config.ROUTE_TABLES_ID_TO_ROUTES_MAP_2:
            self.route_table_id_to_route_table_map_2[route_table_id] = ec2.CfnRouteTable(
                self, 
                route_table_id,
                vpc_id=self.vpc2.vpc_id,
                tags=[{"key": "Name", "value": route_table_id}]
            )

    # Create subnet route table association for vpc1 and vpc2. 
    def create_subnet_route_tables_associations(self):
        ''' Associate Subnets With Route Tables '''
        # vpc1.
        for subnetId, subnet_config in config.SUBNET_CONFIGURATION_1.items():
            routeTableId = subnet_config['route_table_id']
            ec2.CfnSubnetRouteTableAssociation(
                self,
                f"{subnetId}<-->{routeTableId}",
                route_table_id=self.route_table_id_to_route_table_map_1[routeTableId].ref, 
                subnet_id=self.subnet_id_to_subnet_map_1[subnetId].ref
            )
        # vpc2.
        for subnetId, subnet_config in config.SUBNET_CONFIGURATION_2.items():
            routeTableId = subnet_config['route_table_id']
            ec2.CfnSubnetRouteTableAssociation(
                self,
                f"{subnetId}<-->{routeTableId}",
                route_table_id=self.route_table_id_to_route_table_map_2[routeTableId].ref, 
                subnet_id=self.subnet_id_to_subnet_map_2[subnetId].ref
            )

    def create_routes_vpc1(self):
        ''' Create routes of the Route Tables '''
        for route_table_id, routes in config.ROUTE_TABLES_ID_TO_ROUTES_MAP_1.items():
            for i in range(len(routes)):
                route = routes[i]
                kwargs = {
                    **route,
                    'route_table_id': self.route_table_id_to_route_table_map_1[route_table_id].ref,
                }
                if route['router_type'] == ec2.RouterType.GATEWAY:
                    kwargs['gateway_id'] = self.internet_gateway.ref
                if route['router_type'] == ec2.RouterType.NAT_GATEWAY:
                    kwargs['nat_gateway_id'] = self.nat_gateway.ref
                del kwargs['router_type']
                ec2.CfnRoute(self, f'{route_table_id}-route-{i}', **kwargs)

    def create_routes_vpc2(self):
        ''' Create Routes of the Route Tables '''
        for route_table_id, routes in config.ROUTE_TABLES_ID_TO_ROUTES_MAP_2.items():
            for i in range(len(routes)):
                route = routes[i]
                kwargs = {
                    **route,
                    'route_table_id': self.route_table_id_to_route_table_map_2[route_table_id].ref,
                }
                ec2.CfnRoute(self, f'{route_table_id}-route-{i}', **kwargs)

    # Create windows server 2022 Base in public subnet vpc2.
    def create_admin_server(self):
        ec2.CfnInstance(
            self,
            'adminServer',
            availability_zone='eu-central-1a',
            image_id='ami-0ced908879ca69797',  
            instance_type='t2.micro',
            subnet_id= self.subnet_id_to_subnet_map_2['public-subnet-2'].ref,
            key_name='adminServer.kp',  
            security_group_ids=['AdminServerSG'],  
            tags=[{'key': 'Name', 'value': 'AdminServer'}], 
            block_device_mappings=[
                {
                    'deviceName': '/dev/sda1',
                    'ebs': {
                        'volumeSize': 30,
                        'encryption': True,
                        'deleteOnTermination': True,
                    },
                },
            ],
        )
        # Allow RDP access from a trusted source IP address. (Admins home address IP)
        #windows_server.connections.allow_from(ec2.Peer.ipv4('86.83.75.135/24'), ec2.Port.tcp(3389))

        # Allow RDP access from a trusted source IP address. (Admins office IP)
        #windows_server.connections.allow_from(ec2.Peer.ipv4('0.0.0.0'), ec2.Port.tcp(3389))


