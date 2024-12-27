
import pymsteams

class TeamsNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def notify(self, header, content) :
        teams_msg = pymsteams.connectorcard(self.webhook_url)
        teams_msg.title(header)
        teams_msg.text(content)
        teams_msg.send()

