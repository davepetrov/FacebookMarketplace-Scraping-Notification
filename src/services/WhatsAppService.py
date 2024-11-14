from twilio.rest import Client
from config.Config import Config

class WhatsAppService:
    def __init__(self):
        self.client = Client(Config.ACCOUNT_SID, Config.AUTH_TOKEN)

    def send_messages(self, message, users):
        for user in users:
            print(f"Sending message to {user}")  # Log the user receiving the message
            current_message = ""
            listings = message.strip().split("\n\n")

            for listing in listings:
                if len(current_message) + len(listing) + 2 > Config.MAX_MESSAGE_LENGTH:
                    print(f"Sending message part to {user}")
                    response = self.client.messages.create(body=current_message.strip(), from_=Config.WHATSAPP_NUMBER, to=user)
                    print(f"Response for {user}: {response.status}, SID: {response.sid}")
                    current_message = listing + "\n\n"
                else:
                    current_message += listing + "\n\n"

            if current_message.strip():
                print(f"Sending final message part to {user}")
                response = self.client.messages.create(body=current_message.strip(), from_=Config.WHATSAPP_NUMBER, to=user)
                print(f"Final response for {user}: {response.status}, SID: {response.sid}")
