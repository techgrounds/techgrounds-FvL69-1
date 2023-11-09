## PRICING:

One of the main reasons for moving to the cloud is cost. If done well, public cloud infrastructures can reduce costs significantly   
compared to traditional data centers. This is done by adopting a pay-as-you-go pricing model and economies of scale.  

You pay only for the compute capacity, storage, and outbound data transfer that you use. You never pay for inbound data   
transfer and data transfer between services within the same region.  

*AWS lists four advantages of their pricing model:*  
* Pay-as-you-go  
* Save when you commit  
* Pay less by using more  
* Benefit from massive economies of scale  

When creating a new AWS account, you automatically get a free-tier account for the first 12 months. Some services are free up to a certain limit with a free-tier account.  
Other services are always free. However, those services might be integrated with other services for which you have to pay.  

The Total Cost of Ownership (TCO) is used to measure how much an infrastructure would cost if it were hosted the traditional way.   
This is done by measuring capital expenditures (capex). The cloud pricing model allows you to trade capex for operational (variable)   
expenditure (opex). This can reduce cost by not spending money on capacity you don’t need.  

## KEY-TERMS:

* CAPEX = Capital Expenditure; Money spent on fixed assets e.g. land, buildings and equipment by an organisation or business.
* OPEX = Operational Expenditure; Money spent on ongoing costs such as wages or rent.
* S3 bucket = Simpel Storage Service
* EC2 = Elastic Compute Cloud  

## ASSIGNMENT:

### Study:  
**The four advantages of the AWS pricing model.**  
**AWS free tier for:**  
* S3  
* EC2  
* Always free services    

**Understand the differences between capex and opex.**    

### Exercise:  
* Create an alert that you can use to monitor your own cloud costs.  
* Understand the options that AWS offers to get insights in your cloud costs.  

## USED RESOURCES:

[capex-opex](https://www.google.com/search?client=firefox-b-d&q=capex+and+opex)

[AWS-docs-S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)  

[AWS-docs-EC2](https://docs.aws.amazon.com/ec2/)  

[free-tier-usage](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/tracking-free-tier-usage.html?icmpid=docs_billing_hp-freetier) 

[always-free-services](https://blog.itpro.tv/7-always-free-aws-resources/)  

## DIFFICULTIES:

I had to configure the region setting in my account from global to N.Virginia to be able to get billings under the alarm settings in the  
cloudwatch alarm drop down menu. My region was set to global and the rest was greyed out. I corrected this in the _unified settings_ page.  

## RESULT:  

#### S3 bucket (Simple Storage Service)  
Amazon S3 is an object storage service that stores data as objects within buckets. An object is a file and any metadata   
that describes the file. A bucket is a container for objects.  

To store your data in Amazon S3, you first create a bucket and specify a bucket name and AWS Region. Then, you upload your   
data to that bucket as objects in Amazon S3. Each object has a key (or key name), which is the unique identifier for the object within the bucket.  

#### EC2 (Elastic Compute Cloud)  
Amazon Elastic Compute Cloud (Amazon EC2) provides on-demand, scalable computing capacity   
* You can use EC2 to launch as many or few virtual servers as you need, hence Elastic.  
* EC2 reduces hardware costs so you can develop and deploy applications faster.  

![EC2-instance](../00_includes/SCREENSHOTS/AWS/AWS-02_EC2-example.png)  
Diagram shows a basic architecture of an Amazon EC2 instance deployed within an Amazon Virtual Private Cloud (VPC).   

#### Always free services.  
How many Free Tier – Always Free services are there?    
Currently, there are 35 Always Free services available globally that range from Compute to Database to Mobile, and many more.  
Listing some of them:      
* Amazon DynamoDB is a fast & flexible NoSQL database service for single-digit millisecond performance.  
* AWS Lambda is a compute service that runs your code in response to events and automatically manages the compute resources.  
* Amazon Macie is a fully managed data security and data privacy service that uses machine learning and pattern matching to discover and protect your sensitive data in AWS.  
* Amazon Simple Email Service (SES) is a cost-effective email service in the Cloud that enables developers to send mail from within any application.  
* AWS CloudFormation is a model and provision all your cloud infrastructure resources with code to enable configuration compliance and faster troubleshooting.  

#### Creating an alert  
![creating-cost-alert](../00_includes/SCREENSHOTS/AWS/AWS-02_alert.png)

**E-mail notification from AWS.**
![E-mail_notification](../00_includes/SCREENSHOTS/AWS/AWS-02_E-mail-notification.png)  

#### Understand the options AWS offers to gain insight in cloud costs and usage.  
_**Amazon Managed Grafana**_ is a fully managed, scalable, secure and highly available data visualization service that   
enables customers to instantly query, correlate, and visualize operational metrics, logs, and traces for their   
applications from multiple data sources. Amazon Managed Grafana is open source Grafana compatible and integrated   
with AWS data sources that collect operational data, such as Amazon CloudWatch, Amazon OpenSearch Service, Amazon Athena   
and Amazon Managed Service for Prometheus (AMP). Furthermore, it provides plug-ins to popular open-source databases,   
third-party ISV monitoring tools, as well as other cloud services. With Amazon Managed Grafana you can easily visualize   
information from multiple AWS services, AWS accounts, and Regions in a single Grafana dashboard.  

Other native services are: AWS Cost Explorer, AWS Budgets, and AWS Cost Anomaly Detection.  

#### The differences between capex and opex.  
CAPEX and OPEX (see key-terms)  

The difference is that with CAPEX you have to invest in land to build your data center and you have to buy the servers you need.   
Additional to that you'll require security to safeguard the premissis physically and digitally.  

With OPEX, and this is the trade off AWS offers, you only have to pay for the resources you use.