# Log [21-02-2024]

## DailyReport (1 sentence)
Creating a self signed certificate for HTTPS listener, adjusting peering routes for admin into webserver ssh login. Enableing ALB, listeners, target groups and ASG.

## Obstacles
1.  Adjusting the routes for the peering connection was confusing because of the same names i used for  the default vpc route tables and my custom ones. 
2. The Cfn classes are not compatible with Iinstances and such, all the work on load balancing is for nothing.

## Solutions
1. Gave the route table unique names in every VPC.
2. Tomorrow is presentation day, i had to go back to my code without load balancing.

## Learnings 
1. Use unique names for similar services and resources!!
2. Out of time... made the wrong choice in video to start with in the beginning, after that i wanted to customize as much as possible for learning purposes but it was too far reached for me, my lack of experience with cdk proved to be too much. I learned a lot and it was also fun but i'm very disappointed with my result.
