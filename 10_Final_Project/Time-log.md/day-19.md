# Log [13-02-2024]

## DailyReport (1 sentence)
Working on instances, adminServer and webserver plus routes and security features.

## Obstacles
1. Made a costly mistake(time lost in days), by putting the route function call before the instance function call. Hence the error noted in day-18 Time-log. 
2. error: adminServer No default subnet for availability zone: 'eu-central-1a'.

## Solutions
1. solved by interchanging function call positions.
2. solved by eliminating 'network_interfaces' attibute from instance config and added subnet_id=self.publicSubnet2.ref to the instance instead.