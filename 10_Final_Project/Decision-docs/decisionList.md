# Decisions list:
* VM disks must be encrypted (EBS encryption in EC2 config)
* Daily backup of webserver with 7 day retention. (RDO: 24 hours, RTO: 1 hour)
* Webserver must be installed in automated manner.
    * AMI: linux 2023 (billed per second) 
* Admin server:
    * AMI: windows 2022 base
    * must have public IP
    * reachable only from trusted locations; (SG inbound config: office IP, admins home IP, RDP protocol)
* Used IP ranges: 10.10.10.0/24 and 10.20.20.0/24 
* All subnets must have a firewall on subnet lvl; NACL on each subnet.
* SSH or RDP connections with Webserver: Only allowed from Admin Server.
* Sugestions on architecture:
    * Using 1 region (Frankfurt) instead of 2 as described in by the assignment provided architecture.
    * 1 VPC (configured with required CIDR block)
    * 2 AZ's with 2 subnets each. (public and private subnet in each AZ)