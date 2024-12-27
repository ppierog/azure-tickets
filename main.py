import os
import argparse
from azure_tickets import AzureTickets, TeamsNotifier
from teams_notifier import TeamsNotifier
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    access_token = os.getenv("AZURE_TOKEN")
    org_url = os.getenv("AZURE_ORG_URL")
    users_string = os.getenv("AZURE_USERS")
    users = users_string.replace('\n','').split(",")

    parser = argparse.ArgumentParser(
                    prog='azurre-tickets',
                    description='Get The tickets for azure users',
                    epilog='Enjoy the script! :)')

    parser.add_argument('-n', '--notify', help='notify the report to teams',
                    action='store_true')  # on/off flag

    args = parser.parse_args()

    at = AzureTickets(access_token,
                      org_url)

    report_header, report_content = at.getContent(users)
    out = report_header + "\n" + report_content
    print(out)
    
    if args.notify:
        teams_webhook = os.getenv("TEAMS_WEBHOOK")
        splited_header = report_header.split("\n")
        tn = TeamsNotifier(teams_webhook)
        tn.notify(splited_header[0],out.replace(os.linesep, "<br>"))
