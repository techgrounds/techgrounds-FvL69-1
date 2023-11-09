## SECURITY GROUPS:

Statefulness: NACLs are stateless and do not track the state of a connection, while Security Groups are stateful   
and allow traffic based on the response to previous traffic. Default rule: NACLs have a default rule that denies   
all traffic, while Security Groups have a default rule that allows all traffic.  

## KEY-TERMS:

* VPC = Virtual Private Cloud      
* Security Group = Act's as a statefull firewall. Return traffic is allowed, regardless of the rules.  
* Firewall Manager = Simplifies your security group administration and maintenance tasks across multiple accounts and resources. 
* Network ACL = Network Access Control List  

## ASSIGNMENT:

#### Study:  
* Security Groups in AWS  
* Network Access Control Lists in AWS  

## USED RESOURCES:

[security-groups](https://docs.aws.amazon.com/vpc/latest/userguide/security-groups.html)  
  
[infrastructure-security](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html#VPC_Security_Comparison)  

[network-ACL](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html#nacl-basics)  

## DIFFICULTIES:

None.

## RESULT:  

**Comparing ACL's with Security Groups.**  
![ACLvsSecGroup](../00_includes/SCREENSHOTS/AWS/AWS-08_ACLvsSecGR.png)  

**Layers of security.**  
![layers-of-security](../00_includes/SCREENSHOTS/AWS/AWS-08_layers-of-sec.png)  



