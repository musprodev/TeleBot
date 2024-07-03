# TeleBot
A powerful Python-based Telegram bot for scraping group members, adding members to groups, and sending mass messages. This bot leverages the Telethon library to interact with Telegram's API.

## Features
- **Scrape Members**: Extract member information from Telegram groups and save it in a CSV file.
- **Add Members**: Add members from a CSV file to another Telegram group.
- **Send Mass Messages**: Send personalized messages to members listed in a CSV file.

# Usage

## Install Dependencies
```
pip install telethon
```
## Clone the repo
```
git clone https://github.com/musprodev/TeleBot
cd TeleBot
```
## Setup the environment

**Get Telegram API ID and Hash:**

- Go to https://my.telegram.org.
- Log in with your phone number and login code.
- Navigate to "API development tools".
- Create a new application and note down `the api_id` and `api_hash`.
- **Run** 
```
python setup.py
``` 
- Follow the prompts to enter your `api_id`, `api_hash`, and phone number.

## Scraping Members:
To scrape members from a group, run the scraper.py script:
- **Run**
```
python scraper.py
```
- Follow the prompts to select a group and specify the output CSV file name

## Adding Members to a Group:
- Ensure you have a CSV file with member details (scraped using `scraper.py`).
- Run the `add2group.py` script
```
python add2group.py members.csv
```
- Follow the prompts to select the target group and add members by user ID or username.

## Sending Mass Messages:
- Ensure you have a CSV file with member details.
- Run the `smsbot.py` script:
```
python smsbot.py members.csv
```
- Follow the prompts to select the messaging mode (by user ID or username) and enter your message.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

### Disclaimer
> Don't use this script on your main account, adviced to use an alt account because of bans and restrictions.
