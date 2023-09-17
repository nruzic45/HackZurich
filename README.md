# HackZurich
A submission for the 2023 HackZurich competition.

Truck optimizer - a Desktop application that optimizes trucking routes in three parts:
1. Euclidian distance minimizer, as well as a correction for the towns on the same route.
2. Inbound optimizer, with built in percentage empty haul analysis that depends on minimzed Outbound and Inbound city routes.
3. Basic frontend implemented using Qt Python. 

The routes, distances and correction were represented with adjacency matricies. Analyticaly, the most effective way to reduce emissions
was to use less trucks per customer.

Future work could include making a online interactive platform, that drivers could use to better coordinate and plan their routes
with an AI assistant.

We are very thankful to HackZurich, for giving us this opportunity. Holcim Maqer for inspiring us to come up with solutions, and to all the other
sponsors who made this possible.


