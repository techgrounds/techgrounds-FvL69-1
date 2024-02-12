from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    #CfnOutput,
)
from constructs import Construct

class ProjectAppVersion1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc1 = ec2.Vpc(
            self,
            'vpc1',
            max_azs=3,
            create_internet_gateway=False,
            ip_addresses=ec2.IpAddresses.cidr('10.10.10.0/25'),
            subnet_configuration=[],
            enable_dns_hostnames=True,
            enable_dns_support=True,
            nat_gateways=0,
        )

        self.vpc2 = ec2.Vpc(
            self,
            'vpc2',
            max_azs=3,
            create_internet_gateway=False,
            ip_addresses=ec2.IpAddresses.cidr('10.20.20.0/25'),
            subnet_configuration=[],
            enable_dns_hostnames=True,
            enable_dns_support=True,
            nat_gateways=0,
        )

        self.vpc_peering_connection = ec2.CfnVPCPeeringConnection(
            self,
            'VpcPeeringConnection',
            peer_vpc_id=self.vpc2.vpc_id,
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'vpc1_peering_vpc2'}]
        )

        self.publicSubnet1 = ec2.CfnSubnet(
            self,
            'publicSubnet1',
            availability_zone='eu-central-1a',
            cidr_block='10.10.10.0/26',
            vpc_id=self.vpc1.vpc_id,
            map_public_ip_on_launch=True,
            tags=[{'key': 'Name', 'value': 'publicSubnet1'}],
        )

        self.privateSubnet1 = ec2.CfnSubnet(
            self,
            'privateSubnet1',
            availability_zone='eu-central-1b',
            cidr_block='10.10.10.64/26',
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'privateSubnet1'}],
        )

        self.publicSubnet2 = ec2.CfnSubnet(
            self,
            'publicSubnet2',
            availability_zone='eu-central-1a',
            cidr_block='10.20.20.0/26',
            vpc_id=self.vpc2.vpc_id,
            map_public_ip_on_launch=True,
            tags=[{'key': 'Name', 'value': 'publicSubnet2'}],
        )

        self.privateSubnet2 = ec2.CfnSubnet(
            self,
            'privateSubnet2',
            availability_zone='eu-central-1b',
            cidr_block='10.20.20.64/26',
            vpc_id=self.vpc2.vpc_id,
            tags=[{'key': 'Name', 'value': 'privateSubnet2'}],
        )

        self.elastic_ip = ec2.CfnEIP(self, "EIP")
        self.nat_gateway = self.create_nat_gateway()
        self.nat_gateway.add_dependency(self.elastic_ip)
        self.internet_gateway = self.attach_internet_gateway()

        self.route_table_id_to_route_table_mapVpc1 = {}
        self.route_table_id_to_route_table_mapVpc2 = {}
        self.create_route_tables()
        self.create_Subnet_Route_Table_Associations()
        
        self.adminKeyPair = ec2.KeyPair(
            self, 
            "ServerKeyPairAdmin",
            key_pair_name='adminServer.kp',
            type=ec2.KeyPairType.RSA,
            format=ec2.KeyPairFormat.PEM
        )
        self.adminSG = ec2.SecurityGroup (
            self, 
            "AdminSG",
            vpc=self.vpc2,
            description="adminServerSecurityGroup",
            security_group_name='AdminSG',
        )
        self.adminSG.add_ingress_rule(ec2.Peer.ipv4('86.83.75.135/24'), ec2.Port.tcp(3389), "AllowRDPtrafficToSpecificIP")
        self.adminServer = self.create_admin_server()
        #CfnOutput(self, "adminServerOutput", value='adminServer')
        
        self.webServerKeyPair = ec2.KeyPair(
            self, 
            "ServerKeyPairWeb",
            key_pair_name='webServer.kp',
            type=ec2.KeyPairType.RSA,
            format=ec2.KeyPairFormat.PEM
        )
        self.webSG = ec2.SecurityGroup (
            self, 
            "WebServerSG",
            vpc=self.vpc1,
            description="webServerSecurityGroup",
            allow_all_outbound=True,
            security_group_name='WebServerSG'
        )
        self.webServer = self.create_web_sever()
        #CfnOutput(self, "webServerOutput", value='webServer')

        self.createRoutes()
        
    # Create internet gateway and attach it to vpc1.
    def attach_internet_gateway(self) -> ec2.CfnInternetGateway:
        internet_gateway = ec2.CfnInternetGateway(
            self,
            'IGW',
            tags=[{'key': 'Name', 'value': 'IGW'}]
        )
        ec2.CfnVPCGatewayAttachment(
            self,
            "internet_gateway_attachment",
            vpc_id=self.vpc1.vpc_id,
            internet_gateway_id=internet_gateway.ref
        )
        return internet_gateway
    
    # Create NAT gateway for publicsubnet1 (vpc1).
    def create_nat_gateway(self) -> ec2.CfnNatGateway:
        nat_gateway = ec2.CfnNatGateway(
            self,
            'NGW',
            allocation_id=self.elastic_ip.attr_allocation_id,
            subnet_id=self.publicSubnet1.ref,
            tags=[{'key': 'Name', 'value': 'NGW'}],
        )
        return nat_gateway 

    # Create route tables for vp1 and vpc2.
    def create_route_tables(self):
        # Route tables vpc1.
        for rt_id in ['publicRT1', 'privateRT1']:
            self.route_table_id_to_route_table_mapVpc1[rt_id] = ec2.CfnRouteTable(
                self,
                id=rt_id,
                vpc_id=self.vpc1.vpc_id,
                tags=[{"key": "Name", "value": rt_id}],
            )
        # Route tables vpc2.
        for rt_id in ['publicRT2', 'privateRT2']:
            self.route_table_id_to_route_table_mapVpc2[rt_id] = ec2.CfnRouteTable(
                self,
                id=rt_id,
                vpc_id=self.vpc2.vpc_id,
                tags=[{"key": "Name", "value": rt_id}],
            )

    # Create route table associations vpc1 and vpc2.
    def create_Subnet_Route_Table_Associations(self):
        # vpc1 public and private associations.
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'pubRt1<-->pubSub1',
            route_table_id=self.route_table_id_to_route_table_mapVpc1['publicRT1'].ref,
            subnet_id=self.publicSubnet1.ref,
        )
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'privRt1<-->pubSub1',
            route_table_id=self.route_table_id_to_route_table_mapVpc1['privateRT1'].ref,
            subnet_id=self.privateSubnet1.ref,
        )

        # vpc2 public and private associations.
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'pubRt2<-->pubSub2',
            route_table_id=self.route_table_id_to_route_table_mapVpc2['publicRT2'].ref,
            subnet_id=self.publicSubnet2.ref,
        )
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'privRt2<-->privSub2',
            route_table_id=self.route_table_id_to_route_table_mapVpc2['privateRT2'].ref,
            subnet_id=self.privateSubnet2.ref,
        )

    def createRoutes(self):
        # PublicRT1 to IGW.
        ec2.CfnRoute(
            self,
            'IGW-route',
            route_table_id=self.route_table_id_to_route_table_mapVpc1['publicRT1'].ref,
            destination_cidr_block='0.0.0.0/0',
            gateway_id=self.internet_gateway.ref,
        )
        # PrivateRT1 to NGW.
        ec2.CfnRoute(
            self,
            'NGW-route',
            route_table_id=self.route_table_id_to_route_table_mapVpc1['privateRT1'].ref,
            destination_cidr_block='0.0.0.0/0',
            nat_gateway_id=self.nat_gateway.ref,
        )
        # PublicRT1 to vpc_peering_connection.
        ec2.CfnRoute(
            self,
            "peeringConnectionRoute1",
            route_table_id=self.route_table_id_to_route_table_mapVpc1['publicRT1'].ref,
            destination_cidr_block='10.20.20.0/24',
            vpc_peering_connection_id=self.vpc_peering_connection.ref
        )
        # PublicRT2 to vpc_peering_connection.
        ec2.CfnRoute(
            self,
            "peeringConnectionRoute2",
            route_table_id=self.route_table_id_to_route_table_mapVpc2['publicRT2'].ref,
            destination_cidr_block='10.10.10.0/24',
            vpc_peering_connection_id=self.vpc_peering_connection.ref
        )
        # PublicRT2 to adminServer
        ec2.CfnRoute(
            self,
            'AdminServer-route',
            route_table_id=self.route_table_id_to_route_table_mapVpc2['publicRT2'].ref,
            destination_cidr_block='10.20.20.0/26',
            instance_id=self.adminServer.ref,
        )
        # publicRT1 to webServer.
        ec2.CfnRoute(
            self,
            'webServer-route',
            route_table_id=self.route_table_id_to_route_table_mapVpc1['publicRT1'].ref,
            destination_cidr_block='10.10.10.0/26',
            instance_id=self.webServer.ref,
        )
    
    def create_admin_server(self) -> ec2.CfnInstance:
        admin_server = ec2.CfnInstance(
            self,
            'adminServer',
            instance_type='t2.micro',
            image_id='ami-0ced908879ca69797', # Windows AMI
            subnet_id=self.publicSubnet2.ref,
            availability_zone=self.publicSubnet2.attr_availability_zone,
            security_group_ids=[self.adminSG.security_group_id],
            key_name='adminServer.kp',
            block_device_mappings=[ec2.CfnInstance.BlockDeviceMappingProperty(
                device_name="/dev/sda1",
                ebs=ec2.CfnInstance.EbsProperty(
                    delete_on_termination=True,
                    encrypted=True,
                    #kms_key_id="kmsKeyId",
                    volume_size=30,
                ),
            )],
            tags=[{'key': 'Name', 'value': 'adminServer'}]
        )    
        return admin_server
    
    def create_web_sever(self) -> ec2.CfnInstance:
        web_server = ec2.CfnInstance(
            self,
            "webServer",
            instance_type='t2.micro', 
            image_id='ami-03cceb19496c25679', # LNX AMI
            subnet_id=self.publicSubnet1.ref,
            availability_zone=self.publicSubnet1.attr_availability_zone,
            security_group_ids=[self.webSG.security_group_id],
            key_name='webServer.kp',
            
            block_device_mappings=[ec2.CfnInstance.BlockDeviceMappingProperty(
                device_name="/dev/xvda",
                ebs=ec2.CfnInstance.EbsProperty(
                    delete_on_termination=True,
                    encrypted=True,
                    #kms_key_id="kmsKeyId",
                    volume_size=30,
                    volume_type='gp3',
                ),
            )],
            tags=[{'key': 'Name', 'value': 'webServer'}]
        )
        return web_server
        
