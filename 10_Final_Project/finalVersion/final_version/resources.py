from aws_cdk import(
    aws_ec2 as ec2,
)
import final_version_stack

class Resources(final_ver):
        
    def __init__() -> None:
        publicSubnet1 = ec2.PublicSubnet(
            self,
            'publicSubnet1',
            availability_zone='eu-central-1a',
            cidr_block='10.10.10.0/26',
            vpc_id=self.vpc1.vpc_id,
            map_public_ip_on_launch=True,
        )

        privateSubnet1 = ec2.PrivateSubnet(
            self,
            'privateSubnet1',
            availability_zone='eu-central-1b',
            cidr_block='10.10.10.64/26',
            vpc_id=self.vpc1.vpc_id,
        )

        publicSubnet2 = ec2.PublicSubnet(
            self,
            'publicSubnet2',
            availability_zone='eu-central-1a',
            cidr_block='10.20.20.0/26',
            vpc_id=self.vpc2.vpc_id,
            map_public_ip_on_launch=True,
        )

        privateSubnet2 = ec2.PrivateSubnet(
            self,
            'privateSubnet2',
            availability_zone='eu-central-1b',
            cidr_block='10.20.20.64/26',
            vpc_id=self.vpc2.vpc_id,
        )
        