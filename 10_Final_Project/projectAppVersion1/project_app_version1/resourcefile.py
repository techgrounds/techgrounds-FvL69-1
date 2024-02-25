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
# Application Load Balancer.
        self.ALB = elbv2.ApplicationLoadBalancer(
            self, 
            "ALB",
            security_group=self.albSG,
            vpc=self.vpc1,
            internet_facing=True,
        ) 

        # HTTP listener.
        self.HTTP_listener = self.ALB.add_listener(
            'HTTP_listener',
            protocol=elbv2.ApplicationProtocol.HTTP,
            port=8080,
            open=True,
        )

        # Add target to listener.
        self.HTTP_listener.add_targets(
            'add_target_asg',
            port=8080,
            targets=[self.asg],
        )

        # Auto scaling group.
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

self,
            'ALB_props',
            pro
            vpc=self.vpc1,
            internet_facing=True,
            security_groups=self.albSG,
            ip_address_type=elbv2.IpAddressType.IPV4,


load_balancer_attributes=(
                # period in seconds before deregistering an unhealthy target instance.
                type='deregistration_delay.timeout_seconds', value=60,
                # Enables HTTP/2 communication between the load balancer and targets.
                type='enable_http2', enabled=True,
                type='idle_timeout.timeout_seconds', value=60,
                # Enables HTTP/2 routing for HTTP and HTTPS listeners.
                type='routing.http2_enabled', enabled=True,
                # Automatically redirects HTTP traffic to HTTPS on port 443.
                type='routing.http_to_https_on_443', enabled=True,
                # Specifies the S3 bucket for storing access logs.
                type='access_logging.target', value='s3://cdk-hnb659fds-assets-829594392737-eu-central-1',
                ),

 self.httpListener = elbv2.CfnListener(
            self,
            'HTTP_Listener',
            default_actions=[ActionPr],
            load_balancer_arn= 'arn:aws:elasticloadbalancing:eu-central-1:829594392737:loadbalancer/app/ApplicationLoadBalancer/012254488e05289a',
            port=80,
        )
         

# HTTP listener.
        self.HTTP_listener = elbv2.CfnListener(
            self,
            'HTTP_Listener',
            default_actions=[],
            load_balancer_arn= 'arn:aws:elasticloadbalancing:eu-central-1:829594392737:loadbalancer/app/ApplicationLoadBalancer/012254488e05289a',
            port=80,
        )

        # HTTPS listener.
        self.HTTPS_listener = elbv2.CfnListener(
            self,
            'HTTP_Listener',
            default_actions=[],
            load_balancer_arn= 'arn:aws:elasticloadbalancing:eu-central-1:829594392737:loadbalancer/app/ApplicationLoadBalancer/012254488e05289a',
            port=443,
        )

        # Auto scaling group.
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
         

# Define the bucket
        self.bucket = s3.Bucket(
            self, 
            "MyBucket",
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            bucket_name="cdk-hnb659fds-assets-829594392737-eu-central-1", # Specify the bucket name
            removal_policy=s3.RemovalPolicy.DESTROY # Set removal policy as needed
        )

        # Define the bucket policy
        self.bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:PutObject"], # Grant permission to write objects to the bucket
            effect=iam.Effect.ALLOW,
            resources=[self.bucket.arn_for_objects("*")], # Grant permission to all objects within the bucket
            principals=[iam.ServicePrincipal("elasticloadbalancing.amazonaws.com")], # Grant permission to Elastic Load Balancing
        ))
        self.lb = elbv2.CfnLoadBalancer(
            self,
            'ALB',
            name='ApplicationLoadBalancer',
            ip_address_type='ipv4',
            load_balancer_attributes = [
                elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='load_balancing.cross_zone.enabled', value='True'),
                elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='access_logs.s3.enabled', value='True'),
                elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='access_logs.s3.bucket', value='s3://cdk-hnb659fds-assets-829594392737-eu-central-1'),
                #elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='access_logs.s3.prefix', value= '<location connection logs in S3 bucket>'),
                # The bucket must exist in the same region as the load balancer and have a bucket policy that grants Elastic Load Balancing permissions to write to the bucket.
                # access_logs.s3.prefix - The prefix for the location in the S3 bucket for the access logs.
                elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='idle_timeout.timeout_seconds', value='50'),
                elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='routing.http2.enabled', value='True'),
                elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='routing.http.drop_invalid_header_fields.enabled', value='True'),
                elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='connection_logs.s3.enabled', value='True'),
                elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='connection_logs.s3.bucket', value='s3://cdk-hnb659fds-assets-829594392737-eu-central-1'),
                #elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(key='connection_logs.s3.prefix', value='<location connection logs in S3 bucket>'),
            ],
            subnets=[
                self.publicSubnet1a.attr_subnet_id,
                self.publicSubnet1b.attr_subnet_id,
                self.publicSubnet1c.attr_subnet_id,
            ],
            security_groups=[self.albSG.security_group_id],
            type='application',
            tags=[{'key': 'Name', 'value': 'ApplicationLoadBalancer'}],
        )

    # Auto scaling group.
        self.asg = autoscaling.AutoScalingGroup(
            self, 
            "ASG",
            vpc=self.vpc1,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023),
            security_group=self.albSG,
            health_check=autoscaling.HealthCheck.elb(  # Use ELB health check
                grace=Duration.seconds(60),  # Wait before unhealthy actions
            ),
            key_name=self.key_pair.key_pair_name,
            min_capacity=1,
            max_capacity=3,
            desired_capacity=1,
            user_data=ec2.UserData.custom(self.user_data_file),
        )

  self.publicSubnet1b = ec2.CfnSubnet(
            self,
            'publicSubnet1b',
            availability_zone='eu-central-1b',
            cidr_block='10.10.10.128/27',
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'publicSubnet1b'}],
        )

        self.privateSubnet1b = ec2.CfnSubnet(
            self,
            'privateSubnet1b',
            availability_zone='eu-central-1b',
            cidr_block='10.10.10.160/27',
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'privateSubnet1b'}],
        )

        self.publicSubnet1c = ec2.CfnSubnet(
            self,
            'publicSubnet1c',
            availability_zone='eu-central-1c',
            cidr_block='10.10.10.192/27',
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'publicSubnet1c'}]
        )
        
        self.privateSubnet1c = ec2.CfnSubnet(
            self,
            'privateSubnet1c',
            availability_zone='eu-central-1c',
            cidr_block='10.10.10.224/27',
            vpc_id=self.vpc1.vpc_id,
            tags=[{'key': 'Name', 'value': 'privateSubnet1c'}]
        )      

# Create ApplicationLoadBalancer.
        self.lb = elbv2.CfnLoadBalancer(
            self,
            'ALB',
            name='ApplicationLoadBalancer',
            ip_address_type='ipv4',
            load_balancer_attributes = [
                elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(
                    key='load_balancing.cross_zone.enabled', 
                    value='True',
                ),
            ],
            subnets=[
                self.publicSubnet1a.attr_subnet_id,
                self.publicSubnet1b.attr_subnet_id,
                self.publicSubnet1c.attr_subnet_id,
            ],
            security_groups=[self.albSG.security_group_id],
            type='application',
            tags=[{'key': 'Name', 'value': 'ApplicationLoadBalancer'}],
        )

        # Create a target group for HTTP traffic on port 443.
        self.HTTPS_TargetGroup = elbv2.CfnTargetGroup(
            self, 
            'HTTPS_TargetGroup',
            health_check_enabled=True,
            health_check_interval_seconds=60,
            health_check_path="/health",
            health_check_port='443',
            health_check_protocol="HTTPS",
            health_check_timeout_seconds=10,
            healthy_threshold_count=5,
            port=443,
            protocol="HTTPS",
            vpc_id=self.vpc1.vpc_id,  
            target_type=self.lb.ref,
        )

        # Add HTTPs target to the target group
        self.HTTPS_TargetGroup.add_property_override("Targets", [
            {
                "Id": self.webServer.ref,  
                "Port": 443,
            }
        ])
        
        # HTTP listener. (redirected to HTTPS)
        self.HTTP_listener = elbv2.CfnListener(
            self,
            'HTTP_Listener',
            default_actions=[
                # Redirect all HTTP requests to HTTPS target group.
                elbv2.CfnListener.ActionProperty(
                    type='redirect',
                    redirect_config=elbv2.CfnListener.RedirectConfigProperty(
                        # Preserve host and path information during redirect
                        host='#{host}',
                        path='/#{path}',
                        # Use 301 (Moved Permanently) status code for SEO benefits
                        status_code='HTTP_301'
                    ),
                    target_group_arn=self.HTTPS_TargetGroup.attr_target_group_arn,
                )
            ],
            load_balancer_arn=self.lb.attr_load_balancer_arn,
            protocol='HTTP',
            port=80,
        )

        # HTTPS listener.
        self.HTTPS_listener = elbv2.CfnListener(
            self,
            'HTTPS_Listener',
            default_actions=[
                elbv2.CfnListener.ActionProperty(
                    type='forward',
                    target_group_arn=self.HTTPS_TargetGroup.attr_target_group_arn,
                )
            ],
            load_balancer_arn=self.lb.attr_load_balancer_arn,  # Reference ALB's ARN,
            protocol='HTTPS',
            port=443,
            certificates=[],
        )

        self.asg = autoscaling.CfnAutoScalingGroup(
            self, 
            "ASG",
            auto_scaling_group_name='ASGprojectApp',
            availability_zones=['eu-central-1a', 'eu-central-1b', 'eu-central-1c'],
            instance_id=self.webServer.ref,
            load_balancer_names=[self.lb.ref],
            vpc_zone_identifier=[
                self.privateSubnet1a.ref,
                self.privateSubnet1b.ref,
                self.privateSubnet1c.ref,
            ],
            health_check_grace_period=60,
            health_check_type='ELB',
            min_size='1',
            max_size='3',
            desired_capacity='1',
            target_group_arns=[self.HTTPS_TargetGroup.attr_target_group_arn],
            tags=[
                {'key': 'Name', 'value': 'ASGprojectApp', 'propagateAtLaunch': True},
            ],
        )

        # ALB security group.
        self.albSG = ec2.SecurityGroup(
            self,
            'albSG',
            vpc=self.vpc1,
            allow_all_outbound=True,
            description='applicationLoadBalancerVpc1',
            security_group_name='albSG',
        )
        self.albSG.add_ingress_rule( # Allow HTTP traffic.
            peer=ec2.Peer.any_ipv4(), 
            connection=ec2.Port.tcp(80), 
            description='AllowAllHTTPtraffic',
        )
        self.albSG.add_ingress_rule( # Allow HTTPS traffic.
            peer=ec2.Peer.any_ipv4(), 
            connection=ec2.Port.tcp(443), 
            description='AllowAllHTTPStraffic',
        )