TODO:
- rate limiting
- switch to session based authentication instead of reusing the same api key for everyone so every project
  is protected regardless  of the project id being leaked or not
- make a health microservice that checks the health of each endpoint and monitors the uptime of the service
- need to add a premium tier for users
    - premium users can have more than 1 api key?
    - premium users can have more than 3 projects
    - premium users can call the validate endpoint more than 100 times per day
    - premiums users can have each api key's metrics + project api key usage metrics
    - make more tiers for enterprise users?
- need to create the endpoints for public usage (this is for AKMS's user project's developer's to use)
    - need to add what goes on free tier and what goes on premium tier
    - endpoint for creating, reading, updating, and deleting an api key
    - validating an api key
