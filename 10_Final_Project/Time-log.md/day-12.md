# Log [date]


## DailyReport (1 sentence)
Windows management server partially created, i've decided to create adminServerSG first.

## Obstacles
SG is done but AdminServer instance vpc_subnet attribute is giving me a headache.
TypeError: type of argument vpc_subnets must be one of (aws_cdk.aws_ec2.SubnetSelection, Dict[str, Any], NoneType)
But this syntax turns out not compatible with vpc_subnet attribute. 

## Solucions
I'm looking for documentation about the subject online and trying chat GPT.

## Learnings 
Creating security groups in CDK, configuring a windows server in CDK.