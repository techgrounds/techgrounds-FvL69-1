# ECS (theoretical assignment)
Amazon Elastic Container Service (Amazon ECS) is a fully managed container orchestration service that helps you easily deploy,   
manage, and scale containerized applications. As a fully managed service, Amazon ECS comes with AWS configuration and operational   
best practices built-in. It's integrated with both AWS and third-party tools, such as Amazon Elastic Container Registry and Docker.   
This integration makes it easier for teams to focus on building the applications, not the environment. You can run and scale your   
container workloads across AWS Regions in the cloud, and on-premises, without the complexity of managing a control plane.  

## Key-terms  
There are three layers in Amazon ECS:    
* Capacity - The infrastructure where your containers run, the capacity options are:  
    - Amazon EC2 instances in the AWS cloud  
    - Serverless (AWS Fargate (Fargate)) in the AWS cloud  
    - On-premises virtual machines (VM) or servers  

* Controller - Deploy and manage your applications that run on the containers  
    - The Amazon ECS scheduler is the software that manages your applications.  

* Provisioning - The tools that you can use to interface with the scheduler to deploy and manage your applications and containers  
    - AWS Management Console  
    - AWS CLI  
    - AWS SDKs  
    - Copilot   
    - AWS CDK  

## Assignment  
#### Gain theoratical knowledge of: Amazon ECS (Elastic Container Service)  

### Used sources  
[AWS-ECS-docs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)  

[ECS-anywhere](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/manage-on-premises-container-applications-by-setting-up-amazon-ecs-anywhere-with-the-aws-cdk.html)  

[google-search](https://www.google.com/search?client=firefox-b-d&q=the+difference+between+Amazon+ECS++and+Kubernetes)  

### Encountered problems  
-  

### Result  
#### What problem does ECS solve?  
Amazon Elastic Container Services (Amazon ECS) is a fully managed container orchestration service that helps organizations easily   
deploy, manage, and scale containerized applications.  

#### Which key terms belong to ECS?  
see Key-terms  

#### How does ECS fits or replace in an on-premises setting?  
##### ECS Anywhere  
You can use ECS Anywhere to deploy native Amazon ECS tasks in an on-premises or customer-managed environment.   
This feature helps reduce costs and mitigate complex local    container orchestration and operations. You can use   
ECS Anywhere to deploy and run container applications in both on-premises and cloud environments. It removes the need for     
your team to learn multiple domains and skill sets, or to manage complex software on their own.    

#### How can i combinate ECS with other services?    
How do I add a service to ECS?
To create a service (Amazon ECS console)

    In the navigation page, choose Clusters.
    On the Clusters page, select the cluster to create the service in.
    From the Services tab, choose Create.
    Under Deployment configuration, specify how your application is deployed

#### What is the difference between ECS and other similar services?    
What is the difference between AWS ECS and EKS?  
ECS is a scalable container orchestration solution for running, stopping, and managing containers in a cluster.   
EKS, on the other hand, assists teams in deploying Kubernetes clusters on AWS without the need to manually install Kubernetes on EC2 instances.  