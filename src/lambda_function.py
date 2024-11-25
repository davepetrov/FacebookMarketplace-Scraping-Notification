import time
from concurrent.futures import ThreadPoolExecutor
from config.Config import Config
from utils.TimeUtils import is_within_grace_period
from services.MarketplaceScraper import MarketplaceScraper 
from services.MessagingService import MessageService  


def lambda_handler(event, context):
    message_service = MessageService()
    accumulated_items = []

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(
                scraper.search_marketplace,
                search["item_name"],
                search["max_price_percentage"],
                search["max_price"],
                search["cities"],
                search["province"],
                search["location_url"],
                search["keywords"]
            )
            for search in Config.SEARCHES
        ]

    for future in futures:
        accumulated_items.extend(future.result())

    if is_within_grace_period():
        # print("Within grace period, no notifications sent.")
        return {"statusCode": 200, "body": "Within grace period, no notifications sent."}

    for search in Config.SEARCHES:
        items_for_search = [item for item in accumulated_items if item[0] == search["item_name"]]
        if items_for_search:
            message = f"New items found for {search['item_name']}\n\n"
            for item in items_for_search:
                message += f"Title: {item[2]}\nPrice: ${item[1]}\nLocation: {item[3]}, {item[4]}\nLink: {item[5]}\n\n"
            message_service.send_notifications(message, search["users"])

    return {"statusCode": 200, "body": "Search and notifications completed."}

if __name__ == "__main__":
    iteration_count = 0
    scraper = MarketplaceScraper()  # Persistent scraper instance with cached links

    while True:
        print("\n" + str(lambda_handler(event=None, context=None)))
        print(f"\nIteration {iteration_count} Complete")
        iteration_count += 1
        time.sleep(250)