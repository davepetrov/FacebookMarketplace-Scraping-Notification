# FacebookMP-Item-Scraping-Notification

A robust automation script for scraping Facebook Marketplace and notifying users of new listings via WhatsApp. Configurable to support multiple searches, dynamic criteria, and a notification grace period.

---

## Features

- **Dynamic Search Configuration**: Customize item names, keywords, prices, and location filters.
- **Grace Period Management**: Accumulates notifications during specified hours to avoid disturbances.
- **Multi-user Notifications**: Notify multiple users via WhatsApp for each search.
- **Data Persistence**: Efficient data storage using AWS DynamoDB.
- **Real-time Scraping**: Powered by Selenium for live updates.

---

## Requirements

- **Python Version**: 3.12+
- **Dependencies**: Listed in `requirements.txt`.

---

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/FacebookMP-Item-Scraping-Notification.git
cd FacebookMP-Item-Scraping-Notification
```

### Step 2: Install Dependencies
To install the required libraries, run:
```bash
pip install -r requirements.txt
```

[requirements.txt](src/requirements.txt) contains:
```plaintext
pytz
python-dotenv
boto3
twilio
selenium
```

---

## Configuration

### Step 3: Set Up Environment Variables
The script relies on environment variables for configuration. Create a `.env` file and populate it with the following example:

#### General Configuration
```plaintext
TIMEZONE=America/New_York
GRACE_PERIOD_START=0  # Notifications start after 7 AM
GRACE_PERIOD_END=7
DYNAMODB_TABLE_NAME=ExampleTable
```

#### Twilio Configuration
```plaintext
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
MAX_MESSAGE_LENGTH=1000  # Maximum length for each WhatsApp message
```

#### Search Configuration
Each search has unique parameters.

**Search 1**
```plaintext
SEARCH_1_ITEM_NAME=Example Item 1
SEARCH_1_MAX_PRICE_PERCENTAGE=1.1
SEARCH_1_MAX_PRICE=150
SEARCH_1_LOCATION_URL=https://www.facebook.com/marketplace/1234567890/search?query=ExampleItem1
SEARCH_1_KEYWORDS=example,item1
SEARCH_1_USERS=whatsapp:+1234567890,whatsapp:+0987654321
SEARCH_1_CITIES=City1,City2,City3
SEARCH_1_PROVINCE=ON
```

**Search 2**
```plaintext
SEARCH_2_ITEM_NAME=Example Item 2
SEARCH_2_MAX_PRICE_PERCENTAGE=1.2
SEARCH_2_MAX_PRICE=250
SEARCH_2_LOCATION_URL=https://www.facebook.com/marketplace/1234567890/search?query=ExampleItem2
SEARCH_2_KEYWORDS=example,item2
SEARCH_2_USERS=whatsapp:+1111111111,whatsapp:+2222222222
SEARCH_2_CITIES=CityA,CityB,CityC
SEARCH_2_PROVINCE=BC
```

---

## Usage

### Step 4: Run the Script
Start the script by running:
```bash
python main.py
```

### Modifying Searches
To configure additional searches or update existing ones, modify the `.env` file with new parameters.

---

## Deployment

For continuous operation, deploy the script to a cloud platform such as AWS Lambda or run locally.

---

## Important Notes

- **Grace Period**: Notifications are paused between `GRACE_PERIOD_START` and `GRACE_PERIOD_END` in the specified `TIMEZONE`.
- **Message Splitting**: Notifications exceeding `MAX_MESSAGE_LENGTH` (1000 characters) will be automatically split into multiple messages.
- **Valid WhatsApp Numbers**: Ensure all numbers in `SEARCH_X_USERS` follow the `whatsapp:+[country_code][number]` format.

---

## Example Whatsapp message
![image](images/image-1.png)



## Contributing

We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request for review