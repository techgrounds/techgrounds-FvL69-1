# Log [15-02-2024]

## DailyReport (1 sentence)
Implemented User for web server and autoscaling. Started with ApplicationLoadBalancer and autoscalinggroup build.

## Obstacles
User Data has to be encoded with base64.
Added a 3rd AZ and 2 private subnets to vpc1 to accommodate the ALB with ASG

## Solutions
Encode user_date file with Fn.base64(). Had to import Fn module from aws_ec2.
Asked Google Gemini how to code a ALB and ASG.

## Learnings 