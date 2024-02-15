from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling, 
    Fn,
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
            ip_addresses=ec2.IpAddresses.cidr('10.10.10.0/24'),
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

        # vpc1 subnets.
        self.publicSubnet1 = ec2.CfnSubnet(
            self,
            'publicSubnet1',
            availability_zone='eu-central-1a',
            cidr_block='10.10.10.0/26',
            vpc_id=self.vpc1.vpc_id,
            map_public_ip_on_launch=True,
            tags=[{'key': 'Name', 'value': 'publicSubnet1'}],
        )

        self.privateSubnet1a = ec2.CfnSubnet(
            self,
            'privateSubnet1a',
            availability_zone='eu-central-1a',
            cidr_block='10.10.10.64/26',
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'privateSubnet1a'}],
        )

        self.privateSubnet1b = ec2.CfnSubnet(
            self,
            'privateSubnet1b',
            availability_zone='eu-central-1b',
            cidr_block='10.10.10.128/26',
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'privateSubnet1b'}],
        )
        
        self.privateSubnet1c = ec2.CfnSubnet(
            self,
            'privateSubnet1c',
            availability_zone='eu-central-1c',
            cidr_block='10.10.10.192/26',
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'privateSubnet1c'}]
        )

        # vpc2 subnets.
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
        self.internet_gateway1 = self.attach_internet_gateway1()
        self.internet_gateway2 = self.attach_internet_gateway2()

        self.create_route_tables()
        self.create_Subnet_Route_Table_Associations()
        self.createRoutes()

        # Using existing key pair from AWS Console
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
        self.adminSG.add_ingress_rule( # admin RDP access from home. 
            peer=ec2.Peer.ipv4('86.83.75.135/24'), 
            connection=ec2.Port.tcp(3389), 
            description="AllowRDPtrafficToSpecificIP"
        )
        self.adminSG.add_ingress_rule( # ICMP test purposes
            ec2.Peer.ipv4('10.10.10.40/26'), 
            ec2.Port.icmp_ping(), 
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
        self.webSG.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(), 
            connection=ec2.Port.tcp(80), 
            description='AllowAllHTTPtrafic'
        )
        self.webSG.add_ingress_rule( 
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description='AllowAllHTTPStraffic',
        ) 
        self.webSG.add_ingress_rule( # Internal SSH access admin. 
            peer=ec2.Peer.ipv4('10.20.20.40/26'),
            connection=ec2.Port.tcp(22),
            description='AllowInternalSSHtrafficFromAdminServer',
        )
        self.webSG.add_ingress_rule( # Admin SSH access from home.
            peer=ec2.Peer.ipv4('86.83.75.135/24'),
            connection=ec2.Port.tcp(22),
            description='AllowSSHtrafficFromAdminHome',
        )
        self.webSG.add_ingress_rule( # ICMP test purposes
            peer=ec2.Peer.ipv4('10.20.20.40/26'),
            connection=ec2.Port.icmp_ping(), 
            description='AllowICMPtestServerConnection',
        )

        # Get user data for web server and auto scaling. 
        self.user_data_file = open("project_app_version1/install-httpd.sh", "r").read()
        self.webServer = self.create_web_server()

        # AlbSG, TargetGroup, ALB, ASG and listner.
        self.albSG = ec2.SecurityGroup(
            self,
            'albSG',
            vpc=self.vpc1,
            allow_all_outbound=True,
            description='applicationLoadBalancerVpc1',
            security_group_name='albSG',
        )
        self.albSG.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(), 
            connection=ec2.Port.tcp(80), 
            description='AllowAllHTTPtraffic',
        )
        self.webSG.add_ingress_rule(
            self.albSG, 
            connection=ec2.Port.tcp(80),
            description='AllowTrafficFromALB'
        ) 

        # Application LoadBalancer.
        self.ALB = elbv2.ApplicationLoadBalancer(
            self, 
            "LB",
            security_group=self.albSG,
            vpc=self.vpc1,
            internet_facing=False,
        )

        # Listner.
        self.listner1 = self.ALB.add_listener(
            'publicListner',
            port=80,
            open=True,
        )

        # Target group. 
        self.targetGroup = elbv2.ApplicationTargetGroup(
            self, 
            'TargetGroup', 
            vpc=self.vpc1,
            port=80, 
            protocol=elbv2.ApplicationProtocol.HTTP,
        )

    
        self.asg = autoscaling.AutoScalingGroup(
            self, 
            "ASG",
            vpc=self.vpc1,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023),
            security_group=self.albSG,
            min_capacity=1,
            max_capacity=3,
            desired_capacity=1,
            user_data=ec2.UserData.custom(self.user_data_file),
        )

        
    # Create internet gateway and attach it to vpc1.
    def attach_internet_gateway1(self) -> ec2.CfnInternetGateway:
        internet_gateway1 = ec2.CfnInternetGateway(
            self,
            'IGW1',
            tags=[{'key': 'Name', 'value': 'IGW1'}]
        )
        ec2.CfnVPCGatewayAttachment(
            self,
            "internet_gateway_attachment1",
            vpc_id=self.vpc1.vpc_id,
            internet_gateway_id=internet_gateway1.ref
        )
        return internet_gateway1
    
    # Create internet gateway and attach it to vpc1.
    def attach_internet_gateway2(self) -> ec2.CfnInternetGateway:
        internet_gateway2 = ec2.CfnInternetGateway(
            self,
            'IGW2',
            tags=[{'key': 'Name', 'value': 'IGW2'}]
        )
        ec2.CfnVPCGatewayAttachment(
            self,
            "internet_gateway_attachment2",
            vpc_id=self.vpc2.vpc_id,
            internet_gateway_id=internet_gateway2.ref
        )
        return internet_gateway2
    
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
        self.publicRT1 = ec2.CfnRouteTable(
            self,
            id='publicRT1',
            vpc_id=self.vpc1.vpc_id,
            tags=[{"key": "Name", "value": 'publicRT1'}],
        )
        self.privateRT1 = ec2.CfnRouteTable(
            self,
            id='privateRT1',
            vpc_id=self.vpc1.vpc_id,
            tags=[{"key": "Name", "value": 'privateRT1'}],
        )
        # Route tables vpc2.
        self.publicRT2 = ec2.CfnRouteTable(
            self,
            id='publicRT2',
            vpc_id=self.vpc2.vpc_id,
            tags=[{"key": "Name", "value": 'publicRT2'}],
        )
        self.privateRT2 = ec2.CfnRouteTable(
            self,
            id='privateRT2',
            vpc_id=self.vpc2.vpc_id,
            tags=[{"key": "Name", "value": 'privateRT2'}],
        )

    # Create subnet route table associations vpc1 and vpc2.
    def create_Subnet_Route_Table_Associations(self):
        # vpc1 public and private subnet route table associations.
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'pubRt1<-->pubSub1',
            route_table_id=self.publicRT1.attr_route_table_id,
            subnet_id=self.publicSubnet1.attr_subnet_id,
        )
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'privRt1<-->privSub1a',
            route_table_id=self.privateRT1.attr_route_table_id,
            subnet_id=self.privateSubnet1a.attr_subnet_id,
        )
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'privRt1<-->privSub1b',
            route_table_id=self.privateRT1.attr_route_table_id,
            subnet_id=self.privateSubnet1b.attr_subnet_id,
        )
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'privRt1<-->privSub1c',
            route_table_id=self.privateRT1.attr_route_table_id,
            subnet_id=self.privateSubnet1c.attr_subnet_id,
        )
        # vpc2 public and private subnet route table associations.
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'pubRt2<-->pubSub2',
            route_table_id=self.publicRT2.attr_route_table_id,
            subnet_id=self.publicSubnet2.attr_subnet_id,
        )
        ec2.CfnSubnetRouteTableAssociation(
            self,
            'privRt2<-->privSub2',
            route_table_id=self.privateRT2.attr_route_table_id,
            subnet_id=self.privateSubnet2.attr_subnet_id,
        )

    def createRoutes(self):
        # PublicRT1 to IGW1.
        ec2.CfnRoute(
            self,
            'IGW1-route',
            route_table_id=self.publicRT1.attr_route_table_id,
            destination_cidr_block='0.0.0.0/0',
            gateway_id=self.internet_gateway1.attr_internet_gateway_id,
        )
        # PublicRT2 to IGW2.
        ec2.CfnRoute(
            self,
            'IGW2-route',
            route_table_id=self.publicRT2.attr_route_table_id,
            destination_cidr_block='0.0.0.0/0',
            gateway_id=self.internet_gateway2.attr_internet_gateway_id,
        )
        # PrivateRT1 to NGW.
        ec2.CfnRoute(
            self,
            'NGW-route',
            route_table_id=self.privateRT1.attr_route_table_id,
            destination_cidr_block='0.0.0.0/0',
            nat_gateway_id=self.nat_gateway.attr_nat_gateway_id,
        )
        # PublicRT1 to vpc_peering_connection.
        ec2.CfnRoute(
            self,
            "peeringConnectionRoute1",
            route_table_id=self.publicRT1.attr_route_table_id,
            destination_cidr_block=self.vpc2.vpc_cidr_block,
            vpc_peering_connection_id=self.vpc_peering_connection.attr_id,
        )
        # PublicRT2 to vpc_peering_connection.
        ec2.CfnRoute(
            self,
            "peeringConnectionRoute2",
            route_table_id=self.publicRT2.attr_route_table_id,
            destination_cidr_block=self.vpc1.vpc_cidr_block,
            vpc_peering_connection_id=self.vpc_peering_connection.attr_id,
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
            private_ip_address='10.20.20.40',
            tags=[{'key': 'Name', 'value': 'adminServer'}]
        )    
        return admin_server

    def create_web_server(self) -> ec2.CfnInstance:
        # Get user data file and encode with base64.
        encoded_user_data = Fn.base64(self.user_data_file)
        # Create web server.
        web_server = ec2.CfnInstance(
            self,
            "webServer",
            instance_type='t2.micro', 
            image_id='ami-03cceb19496c25679', # LNX AMI
            subnet_id=self.privateSubnet1c.ref,
            availability_zone=self.privateSubnet1c.attr_availability_zone,
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
            user_data=encoded_user_data,
            private_ip_address='10.10.10.200',
            tags=[{'key': 'Name', 'value': 'webServer'}],
        )
        return web_server
    
        
        
