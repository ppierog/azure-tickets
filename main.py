import os
from azure_tickets import AzureTickets, TeamsNotifier
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    access_token = os.getenv("AZURE_TOKEN")
    org_url = os.getenv("AZURE_ORG_URL")
    users_string = os.getenv("USERS")
    users = users_string.replace('\n','').split(",")
    teams_webhook = os.getenv("TEAMS_WEBHOOK")
   
    at = AzureTickets(access_token,
                      org_url)
    
    report_header, report_content = at.getContent(users)
    out = report_header + "\n" + report_content
    print(out)
    
    #splited_header = report_header.split("\n")
    #tn = TeamsNotifier(teams_webhook)
    #tn.notify(splited_header[0],out.replace(os.linesep, "<br>"))
    