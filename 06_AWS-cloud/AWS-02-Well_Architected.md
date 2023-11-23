# Well-Architected Framework  
The AWS Well-Architected Framework helps you understand the pros and cons of decisions you make while     
building systems on AWS. By using the Framework you will learn architectural best practices for designing   
and operating reliable, secure, efficient, cost-effective, and sustainable systems in the cloud.  

## Key-terms
* Well-Architeded Framework(WAF) = Documents a set of foundational questions that help you understand if a   
  specific architecture aligns well with cloud best practices.  
* WAF tool = Is a service in the cloud that provides a consistent process for you to review and measure your architecture  
  using the WAF. It provides recommendations for making your workloads more reliable, secure, efficient and cost-effective.
* Well-Architected labs = Provides you with a repository of code and documentation to give you hands-on experience implementing  
  best practices.  

## Assignment  
### Study AWS Well-Architected Framework.  

### Used sources    
[AWS-Well-Archtected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)  

[Homepage](https://aws.amazon.com/architecture/well-architected/?ref=wellarchitected-wp&wa-lens-whitepapers.sort-by=item.additionalFields.sortDate&wa-lens-whitepapers.sort-order=desc&wa-guidance-whitepapers.sort-by=item.additionalFields.sortDate&wa-guidance-whitepapers.sort-order=desc)   

[Well-Architected_Labs](https://www.wellarchitectedlabs.com/?ref=wellarchitected-wp)  

[Well-Architected_tool](https://aws.amazon.com/well-architected-tool/?ref=wellarchitected-wp)  

### Experienced problems    
-  

## Result

## Definitions  

### AWS Well-Architected and the Six Pillars Framework Overview  

The AWS Well-Architected Framework describes key concepts, design principles, and architectural best practices for designing and running workloads in the cloud.   
By answering a few foundational questions, learn how well your architecture aligns with cloud best practices and gain guidance for making improvements.  

#### Operational Excellence Pillar  
The ability to support development and run workloads effectively, gain insight into their operations, and to continuously improve   
supporting processes and procedures to deliver business value.    

#### Security Pillar  
The security pillar describes how to take advantage of cloud technologies to protect data, systems, and assets in a way that can improve your security posture.    

#### Reliability Pillar  
The reliability pillar encompasses the ability of a workload to perform its intended function correctly and consistently when it’s expected to.   
This includes the ability to operate and test the workload through its total lifecycle. This paper provides in-depth, best practice guidance   
for implementing reliable workloads on AWS.   

#### Performance Efficiency Pillar  
The ability to use computing resources efficiently to meet system requirements, and to maintain that efficiency as demand changes and technologies evolve.      

#### Cost Optimization Pillar  
The ability to run systems to deliver business value at the lowest price point.    

#### Sustainability Pillar
The ability to continually improve sustainability impacts by reducing energy consumption and increasing efficiency across all components of   
a workload by maximizing the benefits from the provisioned resources and minimizing the total resources required.   


### AWS Well-Architected Lenses  
AWS Well-Architected Lenses extend the guidance offered by AWS Well-Architected to specific industry and technology domains, such as machine learning (ML),   
data analytics, serverless, high performance computing (HPC), IoT, SAP, streaming media, the games industry, hybrid networking, and financial services.   
To fully evaluate workloads, use applicable lenses together with the AWS Well-Architected Framework and its six pillars.  


### AWS Well-Architected Guidance  
Unlike the Framework and Lenses, which are aligned with all six pillars of the Well-Architected Framework, AWS Well-Architected Guidance   
focuses on a specific use case, technology, or implementation scenario.  


### In the AWS Well-Architected Framework, we use these terms:  

    A component is the code, configuration, and AWS Resources that together deliver against a requirement. A component is often the unit   
    of technical ownership, and is decoupled from other components.  

    The term workload is used to identify a set of components that together deliver business value. A workload is usually the level of   
    detail that business and technology leaders communicate about.  

    We think about architecture as being how components work together in a workload. How components communicate and interact is often the focus of architecture diagrams.  

    Milestones mark key changes in your architecture as it evolves throughout the product lifecycle (design, implementation, testing, go live, and in production).  

    Within an organization the technology portfolio is the collection of workloads that are required for the business to operate.  

    The level of effort is categorizing the amount of time, effort, and complexity a task requires for implementation. Each organization needs to consider the size   
    and expertise of the team and the complexity of the workload for additional context to properly categorize the level of effort for the organization.  

        High: The work might take multiple weeks or multiple months. This could be broken out into multiple stories, releases, and tasks.  

        Medium: The work might take multiple days or multiple weeks. This could be broken out into multiple releases and tasks.  

        Low: The work might take multiple hours or multiple days. This could be broken out into multiple tasks.  

When architecting workloads, you make trade-offs between pillars based on your business context. These business decisions can drive your engineering priorities.   
You might   optimize to improve sustainability impact and reduce cost at the expense of reliability in development environments, or, for mission-critical solutions,   
you might optimize reliability with increased costs and sustainability impact. In ecommerce solutions, performance can affect revenue and customer propensity to buy.   
Security and operational excellence are generally not traded-off against the other pillars.   


## On architecture  
Technology architecture teams typically include a set of roles such as: Technical Architect (infrastructure), Solutions Architect (software),    
Data Architect, Networking Architect, and Security Architect.  

At AWS, we prefer to distribute capabilities into teams rather than having a centralized team with that capability. There are risks when you choose  
to distribute decision making authority, for example, verifying that teams are meeting internal standards. We mitigate these risks in two ways.   
First, we have practices (ways of doing things, process, standards, and accepted norms) that focus on allowing each team to have that capability,   
and we put in place experts who verify that teams raise the bar on the standards they need to meet. Second, we implement mechanisms that carry   
out automated checks to verify standards are being met.  

Often these teams use TOGAF or the Zachman Framework as part of an enterprise architecture capability.   

 **“Good intentions never work, you need good mechanisms to make anything happen” — Jeff Bezos.**  

This means replacing a human's best efforts with mechanisms (often automated) that check for compliance with rules or process.   

This establishes a culture across all roles that works back from the customer. Working backward is a fundamental part of our innovation process.   
We start with the customer and what they want, and let that define and guide our efforts.  


## General design principles  
 The Well-Architected Framework identifies a set of general design principles to facilitate good design in the cloud:  

    Stop guessing your capacity needs: If you make a poor capacity decision when deploying a workload, you might end up sitting on expensive idle   
    resources or dealing with the performance implications of limited capacity. With cloud computing, these problems can go away. You can use as   
    much or as little capacity as you need, and scale up and down automatically.  

    Test systems at production scale: In the cloud, you can create a production-scale test environment on demand, complete your testing, and then   
    decommission the resources. Because you only pay for the test environment when it's running, you can simulate your live environment for a   
    fraction of the cost of testing on premises.  

    Automate with architectural experimentation in mind: Automation permits you to create and replicate your workloads at low cost and avoid the   
    expense of manual effort. You can track changes to your automation, audit the impact, and revert to previous parameters when necessary.  

    Consider evolutionary architectures: In a traditional environment, architectural decisions are often implemented as static, onetime events,   
    with a few major versions of a system during its lifetime. As a business and its context continue to evolve, these initial decisions might   
    hinder the system's ability to deliver changing business requirements. In the cloud, the capability to automate and test on demand lowers   
    the risk of impact from design changes. This permits systems to evolve over time so that businesses can take advantage of innovations as a standard practice.  

    Drive architectures using data: In the cloud, you can collect data on how your architectural choices affect the behavior of your workload.   
    This lets you make fact-based decisions on how to improve your workload. Your cloud infrastructure is code, so you can use that data to   
    inform your architecture choices and improvements over time.

    Improve through game days: Test how your architecture and processes perform by regularly scheduling game days to simulate events in production.   
    This will help you understand where improvements can be made and can help develop organizational experience in dealing with events.  


