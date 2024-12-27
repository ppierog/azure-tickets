# azure-tickets
Python Script to fetch azure tickets for users.
Use AzureDevOps with disabled file system cacheing to enable usage in lambda environment
Use PySteams to notify via teams webhook.

# Create environment
`python -m venv .venv`
`sourcre .venv/bin/activate`
`.venv/bin/pip install -r requirements.txt`

# Prepare .env file for standalone usage
`cp .env_example .env`
Setup token, webhook, users and organization in .env
[How to create Azure DevOps Token](https://learn.microsoft.com/pl-pl/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows "Azure DevOps Token")
[How to create incomming webhook](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet "Teams Webhook")

# Standalone script
`.venv/bin/python main.py -h`

# Create AWS Lambda
`./build_lambda.sh`
[See Lambda Packaging for Python](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html "Lambda Packaging")

# AWS Configuration after deployment
`os.environ['azure_token']`
`os.environ['azure_org_url']`
`os.environ['azure_users']`
`os.environ['teams_webhook']`
azure_users is base64 of user list (see into .env_example for details)
[How to create Azure DevOps Token](https://learn.microsoft.com/pl-pl/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows "Azure DevOps Token")
[How to create incomming webhook](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet "Teams Webhook")
