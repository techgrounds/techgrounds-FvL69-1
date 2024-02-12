# Log [12-02-2024]

## DailyReport (1 sentence)
Working on instances, adminServer and webserver plus routes and security features.

## Obstacles
1. Made a costly mistake(time lost in days), by putting the route function call before the instance function call. Hence the error noted in day-18 Time-log. 
2. error: adminServer No default subnet for availability zone: 'eu-central-1a'.
3. CDK complained about AZ definition.

## Solutions
1. solved by interchanging function call positions.
2. solved by eliminating 'network_interfaces' attibute from instance config and added subnet_id=self.publicSubnet2.ref to the instance instead.
3. Adjusted AZ value in instance: availability_zone=self.publicSubnet1.attr_availability_zone,

## Learnings 
Make sure the function calls are in the right order.
How to find resource id's.
