from mailjet_rest import Client
from config.Config import Config

class EmailService:
    def __init__(self):
        self.client = Client(auth=(Config.EMAIL_API_KEY, Config.EMAIL_SECRET_KEY), version='v3.1')
    
    def send_email(self, subject, message, users):
        for user in users:
            # Escape the \n and replace it with <br> for HTML formatting
            html_message = message.replace("\n", "<br>")
            
            # Create a nicely formatted HTML structure
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0;">
                    <div style="max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #f9f9f9;">
                        <h2 style="color: #333; text-align: center; margin-bottom: 20px;">{subject}</h2>
                        <p style="color: #555; font-size: 16px; white-space: pre-line;">{html_message}</p>
                        <hr style="border: 0; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                        <footer style="text-align: center; font-size: 12px; color: #888;">
                            <p>If you have any questions, feel free to <a href="mailto:{Config.EMAIL_SENDER_EMAIL}" style="color: #007bff; text-decoration: none;">contact us</a>.</p>
                            <p>© David's {Config.EMAIL_SENDER_NAME}, All rights reserved.</p>
                        </footer>
                    </div>
                </body>
            </html>
            """

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
                        "HTMLPart": html_content  # Nicely formatted HTML message
                    }
                ]
            }
            
            # Send the email
            result = self.client.send.create(data=email_data)
            print(f"Email sent to {user}: Status {result.status_code}, Response: {result.json()}")
