import os
from dotenv import load_dotenv
import pytz

load_dotenv()

class Config:
    DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
    GRACE_PERIOD_START = int(os.getenv("GRACE_PERIOD_START", 0))
    GRACE_PERIOD_END = int(os.getenv("GRACE_PERIOD_END", 7))
    MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", 1000))
    CSV_FILE = os.getenv("CSV_FILE", "marketplace_results.csv")
    TIMEZONE = pytz.timezone(os.getenv("TIMEZONE", "America/New_York"))
    
    @staticmethod
    def load_searches():
        searches = []
        search_num = 1
        while True:
            item_name = os.getenv(f"SEARCH_{search_num}_ITEM_NAME")
            if not item_name:
                break
            searches.append({
                "item_name": item_name,
                "max_price_percentage": float(os.getenv(f"SEARCH_{search_num}_MAX_PRICE_PERCENTAGE", 1.2)),
                "max_price": int(os.getenv(f"SEARCH_{search_num}_MAX_PRICE", 100)),
                "cities": os.getenv(f"SEARCH_{search_num}_CITIES"),
                "province": os.getenv(f"SEARCH_{search_num}_PROVINCE"),
                "location_url": os.getenv(f"SEARCH_{search_num}_LOCATION_URL"),
                "keywords": os.getenv(f"SEARCH_{search_num}_KEYWORDS", "").split(","),
                "users": os.getenv(f"SEARCH_{search_num}_USERS", "").split(","),
            })
            search_num += 1
        return searches

    SEARCHES = load_searches()
