import base64
import os
from azure_tickets import AzureTickets, TeamsNotifier
 
def lambda_handler(event, context):
    azure_token = os.environ['azure_token']
    azure_org_url = os.environ['azure_org_url']
    azure_users = os.environ['azure_users']
    webhook = os.environ['teams_webhook']
    decoded_users = base64.b64decode(azure_users).decode('utf-8')
    users = decoded_users.split(",")
    azure_tickets = AzureTickets(azure_token, azure_org_url)
    report_header, report_content = azure_tickets.getContent(users)
    
    out = report_header + "\n" + report_content
    htmled_out = out.replace(os.linesep, "<br>")
    #tn = TeamsNotifier(webhook)
    #splited_header = report_header.split("\n")
    #tn.notify(splited_header[0], htmled_out)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8'
        },
        'body': htmled_out
    }
