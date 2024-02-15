network_interfaces=[{
                'associatePublicIpAddress': True,
                'deviceIndex': '0',
                'subnet_id': 'subnetId'
            }],                

self.webServerKeyPair = ec2.KeyPair(
            self, 
            "ServerKeyPairWeb",
            key_pair_name='webServer.kp',
            type=ec2.KeyPairType.RSA,
            format=ec2.KeyPairFormat.PEM
        

# import userdata examples. (source google gemini)
from aws_cdk import aws_ec2 as ec2

# Import existing script from file
user_data_file = open("user_data.sh", "r").read()

# Create an EC2 instance
instance = ec2.Instance(
    self,
    "MyInstance",
    # ... other instance properties
    user_data=ec2.UserData.custom(user_data_file),
)

# Alternatively, use pre-defined functions for basic scripts
instance = ec2.Instance(
    self,
    "MyInstance",
    # ... other instance properties
    user_data=ec2.UserData.for_linux().add_commands("sudo yum update -y"),
)
explanation:
    The user_data property of the ec2.Instance class specifies the user data script.
    ec2.UserData.custom(user_data_file) allows importing user data from a local file.
    ec2.UserData.for_linux().add_commands("sudo yum update -y") creates a basic user data script for updating packages on Linux.


# 2nd example using S3 bucket.
from aws_cdk import aws_ec2 as ec2

# Create a MultipartUserData object
user_data = ec2.MultipartUserData()

# Add commands from a file
commands_file = open("initial_commands.sh", "r").read()
user_data.add_s3_download_command(
    bucket="my-s3-bucket",
    bucket_key="initial_commands.sh",
    local_path="/tmp/initial_commands.sh",
)
user_data.add_commands("chmod +x /tmp/initial_commands.sh && /tmp/initial_commands.sh")

# Add inline commands
user_data.add_commands("sudo apt update -y && sudo apt upgrade -y")

# Create an EC2 instance
instance = ec2.Instance(
    self,
    "MyInstance",
    # ... other instance properties
    user_data=user_data,
)
# Explanation:

    ec2.MultipartUserData allows building complex user data scripts with different parts.
    add_s3_download_command downloads a user data script from S3 at instance launch.
    add_commands adds inline commands directly to the user data script.
    This approach enables modularity and flexibility in user data creation.

Best Practices:

    Keep user data scripts secure and minimize secrets embedded within them.
    Consider using CloudFormation Secrets Manager for sensitive information.
    Test your user data scripts thoroughly before deploying them in production.


# instance routes (non functional)
 # PublicRT2 to adminServer
        ec2.CfnRoute(
            self,
            'AdminServer-route',
            destination_cidr_block=self.publicSubnet2.cidr_block,
            route_table_id=self.publicRT2.attr_route_table_id,
            instance_id=self.adminServer.ref,
        )
        # publicRT1 to webServer.
        ec2.CfnRoute(
            self,
            'webServer-route',
            destination_cidr_block=self.publicSubnet1.cidr_block,
            route_table_id=self.publicRT1.attr_route_table_id,
            instance_id=self.webServer.ref,
        )

    self.testSG = ec2.SecurityGroup (
            self, 
            "testSG",
            vpc=self.vpc2,
            allow_all_outbound=True,
            description="testServerSecurityGroup",
            security_group_name='testSG',
        )   
        self.testSG.add_ingress_rule( # user request traffic
            ec2.Peer.any_ipv4(), 
            ec2.Port.tcp(80), 
            'AllowAllHTTPtrafic'
        )
        self.testSG.add_ingress_rule( # 
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            'AllowAllHTTPStraffic',
        ) 
        self.testSG.add_ingress_rule( # 
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            'AllowAllSSHtraffic',
        )
        self.testSG.add_ingress_rule( # ICMP test purposes
            ec2.Peer.any_ipv4(),
            ec2.Port.all_icmp(), 
            'AllowICMPtestServerConnection',
        )

    self.testServer = self.create_test_server()
    # test server!!!
    def create_test_server(self) -> ec2.CfnInstance:
        test_server = ec2.CfnInstance(
            self,
            "testServer",
            instance_type='t2.micro', 
            image_id='ami-03cceb19496c25679', # LNX AMI
            subnet_id=self.publicSubnet2.ref,
            availability_zone=self.publicSubnet2.attr_availability_zone,
            security_group_ids=[self.testSG.security_group_id],
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
            tags=[{'key': 'Name', 'value': 'testServer'}],
        )
        return test_server
