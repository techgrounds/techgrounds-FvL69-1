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
