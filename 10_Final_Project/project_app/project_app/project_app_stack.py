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
            # 'IpAddresses' configures the IP range and size of the entire VPC.
            ip_addresses=ec2.IpAddresses.cidr('10.10.10.0/25'),
            max_azs=2,
            subnet_configuration=[],
            nat_gateways=0,
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )

        self.subnet_id_to_subnet_map = {}
        self.route_table_id_to_route_table_map = {}

        self.create_subnets_vpc1()
        self.elastic_ip = ec2.CfnEIP(self, "EIP")
        self.internet_gateway = self.attach_internet_gateway()
        self.nat_gateway = self.create_nat_gateway()
        self.nat_gateway.add_dependency(self.elastic_ip)

        self.create_route_tables()
        self.create_subnet_route_tables_association()
        self.create_routes()


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
            self.subnet_id_to_subnet_map[subnet_id] = subnet

    # Create internet gateway and attach it to vpc1.
    def attach_internet_gateway(self) -> ec2.CfnInternetGateway:
        ''' Create and Attach Internet Gateway '''
        internet_gateway = ec2.CfnInternetGateway(
            self,
            config.INTERNET_GATEWAY_1
        )
        ec2.CfnVPCGatewayAttachment(
            self,
            "internet_gateway_attachment",
            vpc_id=self.vpc1.vpc_id,
            internet_gateway_id=internet_gateway.ref
        )

        return internet_gateway

    # Create NAT gateway for public-subnet-1.
    def create_nat_gateway(self) -> ec2.CfnNatGateway:
        ''' Create and Attach NAT Gateway '''
        nat_gateway = ec2.CfnNatGateway(
            self,
            config.NAT_GATEWAY,
            allocation_id=self.elastic_ip.attr_allocation_id,
            subnet_id=self.subnet_id_to_subnet_map[config.PUBLIC_SUBNET_1].ref,
        )

        return nat_gateway  

    # Create route tables for vpc1.
    def create_route_tables(self):
        ''' Create Route Tables '''
        for route_table_id in config.ROUTE_TABLES_ID_TO_ROUTES_MAP:
            self.route_table_id_to_route_table_map[route_table_id] = ec2.CfnRouteTable(
                self, 
                route_table_id,
                vpc_id=self.vpc1.vpc_id,
                tags=[{"key": "Name", "value": route_table_id}]
            )

    def create_subnet_route_tables_association(self):
        ''' Associate Subnets With Route Tables '''
        for subnetId, subnet_config in config.SUBNET_CONFIGURATION_1.items():
            routeTableId = subnet_config['route_table_id']
            ec2.CfnSubnetRouteTableAssociation(
                self,
                f"{subnetId}<-->{routeTableId}",
                route_table_id=self.route_table_id_to_route_table_map[routeTableId].ref, 
                subnet_id=self.subnet_id_to_subnet_map[subnetId].ref
            )
    
    def create_routes(self):
        ''' Create routes of the Route Tables '''
        for route_table_id, routes in config.ROUTE_TABLES_ID_TO_ROUTES_MAP.items():
            for i in range(len(routes)):
                route = routes[i]
                kwargs = {
                    **route,
                    'route_table_id': self.route_table_id_to_route_table_map[route_table_id].ref,
                }
                if route['router_type'] == ec2.RouterType.GATEWAY:
                    kwargs['gateway_id'] = self.internet_gateway.ref
                if route['router_type'] == ec2.RouterType.NAT_GATEWAY:
                    kwargs['nat_gateway_id'] = self.nat_gateway.ref
                del kwargs['router_type']
                ec2.CfnRoute(self, f'{route_table_id}-route-{i}', **kwargs)
