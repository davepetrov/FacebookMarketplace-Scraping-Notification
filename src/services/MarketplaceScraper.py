from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.DatabaseUtils import save_results, get_existing_links
from config.DriverConfig import DriverConfig

import time


class MarketplaceScraper:
    def __init__(self):
        # Cache for links seen across iterations
        self.seen_links = set()

    def _is_location_allowed(self, city, province, cities_search, province_search):
        """
        Check if the extracted location matches any of the desired cities and provinces.
        """
        return (city in cities_search) and (province in province_search)

    def search_marketplace(self, item_name, max_price_percentage, max_price, cities_search, province_search, location_url, keywords):
        driver_config = DriverConfig()
        driver = driver_config.driver

        # Open the marketplace URL
        driver.get(location_url)
        time.sleep(5)

        # Close login modal if present
        try:
            close_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Close' and @role='button']"))
            )
            close_button.click()
            print("Login modal closed.")
        except Exception as e:
            print("Login modal close button could not be interacted with:", e)

        # Scrape marketplace items
        new_items = []
        try:
            items = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@role='link' and contains(@href, '/marketplace/item/')]"))
            )
            print(f"Found {len(items)} items to inspect for {item_name}.")

            # Gather all item links from the page
            item_links = {item.get_attribute("href") for item in items}
            # Filter out links already seen locally
            unseen_links = item_links - self.seen_links

            print(f"New links to process: {len(unseen_links)}")
            if unseen_links:
                # Check against the database only if there are unseen links
                existing_links = get_existing_links(unseen_links)
                print(f"Existing links from the database: {len(existing_links)}")
            else:
                existing_links = set()

            # Process items
            for idx, item in enumerate(items):
                try:
                    item_link = item.get_attribute("href")

                    # Skip already seen or existing links
                    if item_link in self.seen_links or item_link in existing_links:
                        print(f"[X] Skipping already processed item '{item_link}'.\n")
                        continue

                    self.seen_links.add(item_link)  # Cache the link

                    # Extract price, title, and other details
                    price_element = item.find_element(By.XPATH, ".//span[contains(text(), '$') or contains(text(), 'Free')]")
                    title_element = item.find_element(By.XPATH, ".//span[string-length(normalize-space()) > 5 and contains(@style, '-webkit-box-orient: vertical;')]")
                    price_text = price_element.text.replace("$", "").replace(",", "").strip()

                    if "free" in price_text.lower():
                        print(f"[X] Item '{title_element.text}' is labeled as 'Free' and will be ignored.\n")
                        continue
                    else:
                        price_text = price_text[2::]

                    item_price = float(price_text) if price_text.isdigit() else None
                    item_title = title_element.text.lower()

                    # Extract location
                    try:
                        location_element = item.find_element(By.XPATH, f".//following-sibling::div//span[contains(text(), ', {province_search}')]")
                        item_location = location_element.text.strip()
                        city, province = map(str.strip, item_location.split(",", 1))
                    except Exception:
                        print(f"[X] Location not found for item '{item_title}' or city not in {province_search}. Skipping.\n")
                        continue

                    print(f"Extracted details - Title: {item_title}, Price: {item_price}, City: {city}, Province: {province}, Link: {item_link}")

                    # Check if the location matches the search criteria
                    if not self._is_location_allowed(city, province, cities_search, province_search):
                        print(f"[X] Item '{item_title}' is in '{item_location}', which does not match the search criteria.\n")
                        continue

                    # Check price and keywords
                    price_threshold = max_price * max_price_percentage
                    if item_price is not None and item_price <= price_threshold:
                        keyword_matches = sum(1 for word in keywords if word in item_title)
                        if keyword_matches >= 2:
                            print(f"Item '{item_title}' matches criteria. Adding to new items.\n")
                            new_items.append((item_name, item_price, item_title, city, province, item_link))
                        else:
                            print("[X] Item doesn't match keyword criteria.\n")
                    else:
                        print("[X] Item doesn't match price criteria.\n")

                except Exception as inner_e:
                    print(f"Error processing item {idx + 1}: {inner_e}\n")

        except Exception as e:
            print(f"Could not load items for inspection for {item_name}: {e}\n")
        finally:
            driver.quit()

        # Return only the new listings
        return new_items
