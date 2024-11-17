from services.WhatsAppService import WhatsAppService
from services.EmailService import EmailService

class MessageService:
    def __init__(self):
        self.whatsapp_service = WhatsAppService()
        self.email_service = EmailService()
    
    def send_notifications(self, message, users):
        whatsapp_users = [user['value'] for user in users if user['type'] == 'whatsapp']
        email_users = [user['value'] for user in users if user['type'] == 'email']

        if whatsapp_users:
            print("Sending WhatsApp messages...")
            self.whatsapp_service.send_messages(message, whatsapp_users)

        if email_users:
            print("Sending Email messages...")
            self.email_service.send_email("Marketplace Alert", message, email_users)