from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput,
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

        # import existing key pair from AWS Console
        self.key_pair = ec2.KeyPair.from_key_pair_name(
            self, 
            "ExistingKeyPair",
            key_pair_name='projectApp'
        )

        self.adminSG = ec2.SecurityGroup (
            self, 
            "AdminSG",
            vpc=self.vpc2,
            allow_all_outbound=True,
            description="adminServerSecurityGroup",
            security_group_name='AdminSG',
        )   
        self.adminSG.add_ingress_rule( # admin access
            ec2.Peer.ipv4('86.83.75.135/24'), 
            ec2.Port.tcp(3389), 
            "AllowRDPtrafficToSpecificIP"
        )
        self.adminSG.add_ingress_rule( # ICMP test purposes
            ec2.Peer.any_ipv4(), 
            ec2.Port.all_icmp(), 
            'AllowICMPtestServerConnection',
        ) 
        self.adminServer = self.create_admin_server()
        
        self.webSG = ec2.SecurityGroup (
            self, 
            "WebServerSG",
            vpc=self.vpc1,
            allow_all_outbound=True,
            description="webServerSecurityGroup",
            security_group_name='WebServerSG'
        )
        self.webSG.add_ingress_rule( # user request traffic
            ec2.Peer.any_ipv4(), 
            ec2.Port.tcp(80), 
            'AllowHTTPtrafic'
        ) 
        self.webSG.add_ingress_rule( # 
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            'AllowSSHtraffic',
        )
        self.webSG.add_ingress_rule( # ICMP test purposes
            ec2.Peer.any_ipv4(),
            ec2.Port.all_icmp(), 
            'AllowICMPtestServerConnection',
        ) 
        #self.user_data_file = open("project_app_verion1/install-httpd.sh", "r").read()
        self.webServer = self.create_web_sever()

        self.createRoutes()

        # Export the instance private and public IP addresses to the console.
        CfnOutput(
            self,
            'publicIPadminServer',
            value=self.adminServer.attr_public_ip,
            export_name='publicIPadminServer',
        )
        CfnOutput(
            self,
            'privateIPadminServer',
            value=self.adminServer.attr_private_ip,
            export_name='privateIPadminServer',
        )
        CfnOutput(
            self,
            'publicIPwebServer',
            value=self.webServer.attr_public_ip,
            export_name='publicIPwebServer', 
        )
        CfnOutput(
            self,
            'privateIPwebServer',
            value=self.webServer.attr_private_ip,
            export_name='privateIPwebServer', 
        )
        
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
            'privRt1<-->privSub1',
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
            gateway_id=self.internet_gateway.attr_internet_gateway_id,
        )
        # PrivateRT1 to NGW.
        ec2.CfnRoute(
            self,
            'NGW-route',
            route_table_id=self.route_table_id_to_route_table_mapVpc1['privateRT1'].ref,
            destination_cidr_block='0.0.0.0/0',
            nat_gateway_id=self.nat_gateway.attr_nat_gateway_id,
        )
        # PublicRT1 to vpc_peering_connection.
        ec2.CfnRoute(
            self,
            "peeringConnectionRoute1",
            route_table_id=self.route_table_id_to_route_table_mapVpc1['publicRT1'].ref,
            destination_cidr_block=self.vpc2.vpc_cidr_block,
            vpc_peering_connection_id=self.vpc_peering_connection.attr_id,
        )
        # PublicRT2 to vpc_peering_connection.
        ec2.CfnRoute(
            self,
            "peeringConnectionRoute2",
            route_table_id=self.route_table_id_to_route_table_mapVpc2['publicRT2'].ref,
            destination_cidr_block=self.vpc1.vpc_cidr_block,
            vpc_peering_connection_id=self.vpc_peering_connection.attr_id,
        )
        # PublicRT2 to adminServer
        ec2.CfnRoute(
            self,
            'AdminServer-route',
            route_table_id=self.route_table_id_to_route_table_mapVpc2['publicRT2'].ref,
            destination_cidr_block=self.publicSubnet2.cidr_block,
            instance_id=self.adminServer.attr_id,
        )
        # publicRT1 to webServer.
        ec2.CfnRoute(
            self,
            'webServer-route',
            route_table_id=self.route_table_id_to_route_table_mapVpc1['publicRT1'].ref,
            destination_cidr_block=self.publicSubnet1.cidr_block,
            instance_id=self.webServer.attr_id,
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
            key_name=self.key_pair.key_pair_name,
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
            key_name=self.key_pair.key_pair_name,
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
            tags=[{'key': 'Name', 'value': 'webServer'}],
        )
        return web_server
    
        
        
