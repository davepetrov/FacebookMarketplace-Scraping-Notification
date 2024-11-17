from mailjet_rest import Client
from config.Config import Config

class EmailService:
    def __init__(self):
        self.client = Client(auth=(Config.EMAIL_API_KEY, Config.EMAIL_SECRET_KEY), version='v3.1')
    
    def send_email(self, subject, message, users):
        for user in users:
            # Escape the \n and replace it with <br> before using it in the f-string
            html_message = message.replace("\n", "<br>")
            email_data = {
                'Messages': [
                    {
                        "From": {
                            "Email": Config.EMAIL_SENDER_EMAIL,
                            "Name": Config.EMAIL_SENDER_NAME,
                        },
                        "To": [{"Email": user}],
                        "Subject": subject,
                        "TextPart": message,  # Plain text part
                        "HTMLPart": f"<p>{html_message}</p>"  # HTML formatted message
                    }
                ]
            }
            result = self.client.send.create(data=email_data)
            print(f"Email sent to {user}: Status {result.status_code}, Response: {result.json()}")
