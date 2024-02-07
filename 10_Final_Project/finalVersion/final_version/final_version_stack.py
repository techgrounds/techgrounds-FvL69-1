from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class FinalVersionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define vpc1.
        self.vpc1 = ec2.Vpc(
            self,
            'vpc1',
            max_azs=2,
            create_internet_gateway=False,
            ip_addresses=ec2.IpAddresses.cidr('10.10.10.0/24'),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='public',
                    cidr_mask=26,
                    subnet_type=ec2.SubnetType.PUBLIC,
                    map_public_ip_on_launch=True,
                ),
                ec2.SubnetConfiguration(
                    name='private_egress',
                    cidr_mask=26,
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
            )],
            enable_dns_hostnames=True,
            enable_dns_support=True,
            nat_gateways=0,
        )

        # Define vpc2.
        self.vpc2 = ec2.Vpc(
            self,
            'vpc2',
            max_azs=2,
            create_internet_gateway=False,
            ip_addresses=ec2.IpAddresses.cidr('10.20.20.0/24'),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name='public',
                    cidr_mask=26,
                    subnet_type=ec2.SubnetType.PUBLIC,
                    map_public_ip_on_launch=True,
                ),
                ec2.SubnetConfiguration(
                    name='private_isolated',
                    cidr_mask=26,
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
            )],
            enable_dns_hostnames=True,
            enable_dns_support=True,
            nat_gateways=0,
        )

        self.internet_gateway = self.attach_internet_gateway()

        self.elastic_ip = ec2.CfnEIP(self, "EIP")
        self.nat_gateway = self.create_nat_gateway()
        self.nat_gateway.add_dependency(self.elastic_ip)

        self.route_table_id_to_route_table_map1 = {}
        self.route_table_id_to_route_table_map2 = {}
        self.routeTables = self.createRouteTables()

        # Create vpc peering.
        self.vpc_peering_connection = ec2.CfnVPCPeeringConnection(
            self,
            'VpcPeeringConnection',
            peer_vpc_id=self.vpc2.vpc_id,
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'vpc1_peering_vpc2'}]
        )

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
        #self.AdminServer = self.create_admin_server()

        # Create internet gateway and attach it to vpc1.
    def attach_internet_gateway(self) -> ec2.CfnInternetGateway:
        internet_gateway = ec2.CfnInternetGateway(
            self,
            'IGW'
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
        nat_gateway = ec2.CfnNatGateway(
            self,
            'NGW',
            allocation_id=self.elastic_ip.attr_allocation_id,
            subnet_id=self.vpc1.public_subnets[0].subnet_id,
        )
        return nat_gateway 

    def createRouteTables(self):
        # Route tables vpc1.
        for rt_id in ['publicRT1', 'privateRT1']:
            self.route_table_id_to_route_table_map1[rt_id] = ec2.CfnRouteTable(
                self,
                id=rt_id,
                vpc_id=self.vpc1.vpc_id,
                tags=[{"key": "Name", "value": rt_id}],
            )
        # Route tables vpc2.
        for rt_id in ['publicRT2', 'privateRT2']:
            self.route_table_id_to_route_table_map2[rt_id] = ec2.CfnRouteTable(
                self,
                id=rt_id,
                vpc_id=self.vpc2.vpc_id,
                tags=[{"key": "Name", "value": rt_id}],
            )

    
   




    
    
        
       
