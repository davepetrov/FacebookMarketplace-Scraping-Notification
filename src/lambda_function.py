from services.WhatsAppService import WhatsAppService
from services.MarketplaceScraper import MarketplaceScraper
from config.Config import Config
from utils.TimeUtils import is_within_grace_period
from concurrent.futures import ThreadPoolExecutor
import time
import json

def lambda_handler(event, context):
    whatsapp_service = WhatsAppService()
    scraper = MarketplaceScraper()
    # scraper.initialize_browser()
    
    accumulated_items = []
    saved_items = []
    # Run searches in parallel
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
        saved_items.extend(future.result())
    accumulated_items.extend(saved_items)

    # Count accumulated listings
    accumulated_count = len(accumulated_items)
    print(f"Total accumulated listings: {accumulated_count}")

    if is_within_grace_period():
        print("\nWithin grace period. Accumulating new items without sending notifications.")
    else:
        for search in Config.SEARCHES:
            items_for_search = [item for item in accumulated_items if item[0] == search["item_name"]]
            
            if items_for_search:
                message = f"New items found for {search['item_name']}:\n\n"
                for item in items_for_search:
                    message += (f"Listing Title: {item[2]}\nPrice: ${item[1]}\nLocation: {item[3]}, {item[4]}\nLink: {item[5]}\n\n")

                whatsapp_service.send_messages(message, search["users"])
                print(f"Sent WhatsApp notification for {search['item_name']} to users.")
                
                accumulated_items = [item for item in accumulated_items if item not in items_for_search]

        
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Scraping completed successfully'
        })
    }