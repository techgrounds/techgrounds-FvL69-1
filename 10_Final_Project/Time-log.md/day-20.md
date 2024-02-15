# Log [13-02-2024]

## DailyReport (1 sentence)
Establish connection between servers, use import existing key-pair

## Obstacles
1. Only one VPC has an IGW so i need to establish network traffic between the VPCs.

## Solutions
* Add ingress rules to servers for appropriate network traffic.
  - Allow ICMP for test purposes. (admin & web server)
  - Allow All SSH for test purposes. (web server)
  - Allow All HTTP for test purposes (web server)
  - Allow All HTTPS for test purposes (web server)
  - Allow RDP with specific IP address. (admin server)

## Learnings 
Configuring SGs and add rules to them.

* Still no connectivity between the two instances.

