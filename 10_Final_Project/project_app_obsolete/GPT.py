from aws_cdk import core
from aws_cdk import aws_ec2 as ec2

class MyWindowsInstanceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Your custom subnets
        custom_subnet1 = ec2.Subnet(self, "CustomSubnet1", vpc=self.vpc, availability_zone="your-az-1", cidr_block="10.0.1.0/24")
        custom_subnet2 = ec2.Subnet(self, "CustomSubnet2", vpc=self.vpc, availability_zone="your-az-2", cidr_block="10.0.2.0/24")

        # Create a Windows EC2 instance using custom subnets
        windows_instance = ec2.Instance(self, "MyWindowsInstance",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2,
                ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.WindowsImage(
                ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_BASE
            ),
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[custom_subnet1, custom_subnet2]),
            key_name="your-key-pair-name",  # Replace with your key pair name
            security_group=ec2.SecurityGroup.from_security_group_id(self, "MySecurityGroup", "your-security-group-id"),  # Replace with your security group ID
            block_devices=[
                ec2.BlockDevice(
                    device_name='/dev/sda1',  # Default root volume
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=30,
                        encrypted=True,
                        delete_on_termination=True,
                        iops=100 / 3000
                    )
                )
            ]
        )

        # Output the instance ID
        core.CfnOutput(self, "MyWindowsInstanceId",
            value=windows_instance.instance_id,
            description="Windows Server Instance ID"
        )
