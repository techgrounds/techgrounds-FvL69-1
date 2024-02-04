# Log [01-02-2024]


## DailyReport (1 sentence)
Created vpc peering and routes to route public route tables in both VPCs, attempting to create the Admin Server and routing in vpc2 public subnet according to user-story 4.

## Obstacles
I couldn't add succesfully the routes in the route tables in my config file. I'm still not sure how to code this correctly, there's not much documentation for IaC coding in that respect.

## Solucions
I've created a method in my main file which enables VPC peering and routing to the public route tables in both VPCs. I've asked Google AI Bard for guidance and it worked.

## Learnings 
Using Google Bard or Chat GPT for specific info is a great help.