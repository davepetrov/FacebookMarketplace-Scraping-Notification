from decimal import Decimal
import boto3
from botocore.exceptions import ClientError
from config.Config import Config
import time

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(Config.DYNAMODB_TABLE_NAME)

def get_existing_links(links):
    """
    This function performs a batch retrieval of links from DynamoDB to check for duplicates.
    It returns a set of links that already exist in the database.
    """
    try:
        # Prepare the keys for batch get request
        keys = [{"item_link": link} for link in links]
        
        # Perform batch get operation
        response = dynamodb.batch_get_item(
            RequestItems={
                Config.DYNAMODB_TABLE_NAME: {
                    "Keys": keys
                }
            }
        )
        
        # Extract the links of items that exist in the table
        existing_items = response.get("Responses", {}).get(Config.DYNAMODB_TABLE_NAME, [])
        existing_links = {item["item_link"] for item in existing_items}
        
        # print(f"Existing links found: {existing_links}")
        return existing_links

    except ClientError as e:
        print(f"Error fetching batch items: {e}")
        return set()


def save_items(items):
    """
    This function saves a new item to DynamoDB, including city and province.
    """
    for item_name, item_price, item_title, city, province, item_link in items:
        
        try:
            table.put_item(
                Item={
                    "item_link": item_link,
                    "item_name": item_name,
                    "item_price": Decimal(str(item_price)), 
                    "item_title": item_title,
                    "city": city,  
                    "province": province,  
                    "timestamp": int(time.time())
                }
            )
            print(f"Saved new result: {item_title} for ${item_price}. City: {city}, Province: {province}, Link: {item_link}")
            
        except ClientError as e:
            print(f"Error saving item: {e}")