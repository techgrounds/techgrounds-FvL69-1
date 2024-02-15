# Log [14-02-2024]

## DailyReport (1 sentence)
Understanding flow of network traffic because i can't get traffic flowing from vpc1 to vpc2.

## Obstacles
1. Windows instance is not reachable through the IGW in vpc1.
2. Windows instance (admin server) firewall blocks ICMP packets from Linux instance (web server) regardless of the ingress rule that i've set on it's security group to allow all ICMP traffic. So loggin into my admin server in vpc2 is not possible through vpc1.
3. I've tried to configure the settings of my admin server to be reachable on the network for other devices but without success.

## Solutions
1. I've added an IGW to vpc2. 
    - I can access the admin server now through RDP.
    - I can ssh from the admin server into the web server via vpc peering using the private IP from my web server.
2. windows instance is quite slow so i left the firewall settings for now
3. SSH login from admin into web server works fine.


## Learnings 
1. Using an IGW for each VPC works better and is of no additional cost
2. I don't have to create specific routes for my instances. Route table subnet associations, security group and ACL rules dictate the flow of traffic in a network.