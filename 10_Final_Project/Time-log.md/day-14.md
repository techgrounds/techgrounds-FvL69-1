# Log [5-02-2024]

## DailyReport (1 sentence)
Tried an ec2.CfnInstance() instead of ec2.Instance() and had to make adjustments to several code constructs but i keep getting errors.

## Obstacles
Everything in my code (NGW, IGW, RTs, Subnets, RT-Subnet-associations, instance-SG, key-pair, VPCs, VPCpeering, routes) is working and deploys except the Windows Admin Server and the routing in vpc2. My instance complains about not having subnets in vpc2. I cannot define the subnet_id attribute for some reason. It gives me a proper headache!

## Solucions
I'm stuck.

## Learnings 
I've spend too long (14 hours today) and already 5 days on trying to get this code working. I'm gonna try a different approach. One without a config file.