
from datetime import date, datetime, timedelta
import pymsteams
import os
from azure.devops.connection import Connection
from azure.devops.v7_1.work_item_tracking import Wiql
from msrest.authentication import BasicAuthentication
import hashlib

class AzureTickets:

    def __init__(self, personal_access_token, organization_url):
        self.personal_access_token = personal_access_token
        self.organization_url = organization_url
        self.credentials = BasicAuthentication('', personal_access_token)
        self.connection = Connection(base_url=organization_url, creds= self.credentials)
        self.client = self.connection.clients.get_work_item_tracking_client()
    
    def getInitials(self, name):
        splited = name.split()
        hashed = splited[0] + splited[1]
        return splited[0][0] + splited[1][0] + " " + hashlib.md5(hashed.encode()).hexdigest()

    def getContent(self, users):
        today = date.today()
        prev_moth = today - timedelta(days=14)
        # The day 28 exists in every month. 4 days later, it's always next month
        curr_month = prev_moth.replace(day=28) + timedelta(days=4)
        last_day_of_prev_month = curr_month - timedelta(days=curr_month.day)
        first_day_of_prev_month = last_day_of_prev_month.replace(day=1)
        
        authors_initials_list = [self.getInitials(user) for user in users]
        authors_initials_list.sort()

        authors_initials = "\n".join(authors_initials_list)
        report_header = f"Azure Report: {first_day_of_prev_month}-{today}\n{authors_initials}\n"
        report_content = ""
        def _generateCombinedOr(users):
            combined = ""
            for user in users:
                combined += f" OR [System.AssignedTo] = '{user}'"
            return combined[4:]

        combinedOrCloause = _generateCombinedOr(users)
        wiql = Wiql(
            query=f"""
            select [System.Id], [System.AssignedTo]
            from WorkItems
            where
                    ({combinedOrCloause})
                    AND [System.State] = 'closed'
                    AND [Closed Date] >= '{first_day_of_prev_month}'
                    AND [Closed Date] <= '{today}'
            order by [Closed Date] desc"""

        )
        result = self.client.query_by_wiql(wiql)

        item_ids = [str(item.id) for item in result.work_items]
        items =  self.client.get_work_items(item_ids)

        items.sort(key=lambda item: item.fields['System.AssignedTo']['displayName'])

        author=''
        parsed_initials_authors = []
        for item in items:
            if author!=self.getInitials(item.fields['System.AssignedTo']['displayName']):
                author=self.getInitials(item.fields['System.AssignedTo']['displayName'])
                report_content += os.linesep
                report_content += f"{author}"
                report_content += os.linesep
                report_content += os.linesep
                parsed_initials_authors.append(author)

            #work_item = self.client.get_work_item(int(item.id))
            report_content += f"[{item.id}] {item.fields['System.Title']}"
            report_content += os.linesep

        report_content += os.linesep
        report_content += os.linesep
        not_parsed_authors_initials = set(authors_initials_list) - set(parsed_initials_authors)
        report_content+= "Missing Reports:\n"
        report_content+= "\n".join(not_parsed_authors_initials)
        report_content += os.linesep
        report_content += os.linesep

        return report_header, report_content

class TeamsNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def notify(self, header, content) :
        teams_msg = pymsteams.connectorcard(self.webhook_url)
        teams_msg.title(header)
        teams_msg.text(content)
        teams_msg.send()

