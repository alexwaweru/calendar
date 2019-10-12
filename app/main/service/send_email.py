import requests


def send_email(sender_email, recipients_emails, subject, body):
    
    with open("resources/api_credentials.yml", 'r') as ymlfile:
        api_cfg = yaml.load(ymlfile, yaml.FullLoader)
        apikey = api_cfg["mailgun"]["apikey"]
        url = api_cfg["mailgun"]["url"]
        
        return requests.post(url, auth = ("api", apikey), data = { "from": sender_email,
                            "to": recipients_emails, "subject": subject, 
                            "textOrHtmlMessage": body}
                            )
    