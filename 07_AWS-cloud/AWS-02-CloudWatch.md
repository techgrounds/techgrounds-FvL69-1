# CloudWatch (practical assignment).  
What is Amazon CloudWatch?  

Amazon CloudWatch monitors your Amazon Web Services (AWS) resources and the applications you run on AWS in real time.   
You can use CloudWatch to collect and track metrics, which are variables you can measure for your resources and applications.  

The CloudWatch home page automatically displays metrics about every AWS service you use. You can additionally create custom   
dashboards to display metrics about your custom applications, and display custom collections of metrics that you choose.  

You can create alarms that watch metrics and send notifications or automatically make changes to the resources you are monitoring   
when a threshold is breached. For example, you can monitor the CPU usage and disk reads and writes of your Amazon EC2 instances   
and then use that data to determine whether you should launch additional instances to handle increased load. You can also use   
this data to stop under-used instances to save money.  

With CloudWatch, you gain system-wide visibility into resource utilization, application performance, and operational health.  

## Key-terms  
The following terminology and concepts are central to your understanding and use of Amazon CloudWatch:

    Namespaces: A namespace is a container for CloudWatch metrics. Naming convention: AWS/service

    Metrics: Metrics are the fundamental concept in CloudWatch. A metric represents a time-ordered set of data points that are published to CloudWatch.   
             Think of a metric as a variable to monitor, and the data points as representing the values of that variable over time.   

    Time stamps: Each metric data point must be associated with a time stamp. The time stamp can be up to two weeks in the past and up to two hours into the future.   

    Dimensions: A dimension is a name/value pair that is part of the identity of a metric. You can assign up to 30 dimensions to a metric.  

    Resolution: Each metric is one of the following: Standard resolution, with data having a one-minute granularity or  
                High resolution, with data at a granularity of one second

    Statistics: Statistics are metric data aggregations over specified periods of time.  

    Percentiles: A percentile indicates the relative standing of a value in a dataset. For example, the 95th percentile means that 95 percent   
                 of the data is lower than this value and 5 percent of the data is higher than this value. Percentiles help you get a better   
                 understanding of the distribution of your metric data.  

    Alarms: You can use an alarm to automatically initiate actions on your behalf.  

## Assignment  
### CloudWatch in practice.  

### Used sources  
[WhatIsCloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)  

### Encountered problems  
-  

### Result  
Amazon CloudWatch is basically a metrics repository. An AWS service—such as Amazon EC2—puts metrics into the repository,   
and you retrieve statistics based on those metrics. If you put your own custom metrics into the repository, you can retrieve   
statistics on these metrics as well.  

![CloudWatch-pic](CW-Overview.png)  

### Amazon CloudWatch can be accessed via API, command-line interface, AWS SDKs, and the AWS Management Console.  
