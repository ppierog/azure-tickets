# azure-tickets
Python Script to fetch azure tickets for users.
Use AzureDevOps with disabled file system cacheing to enable usage in lambda environment
Use PySteams to notify via teams webhook.

# Create environment
python -m venv .venv
sourcre .venv/bin/activate
.venv/bin/pip install -r requirements.txt
