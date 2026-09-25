# Telegram Job Bot

A Telegram bot that searches for job vacancies via the RemoteOK API.

## Features
- Takes a keyword from the user
- Searches for vacancies via RemoteOK
- Returns 5 results: title, company, location, salary, link

## How to run
1. Install dependencies: `pip install aiogram requests python-dotenv`
2. Get a token from [@BotFather](https://t.me/BotFather)
3. Create a `.env` file in the project root: `BOT_TOKEN=your_token_here`
4. Run: `python pars_bot.py`

## Example
<img width="697" height="1008" alt="image" src="https://github.com/user-attachments/assets/17ecc118-419f-47da-9dcd-8e09a369eff9" />


## Tech stack
- Python 3.10+
- aiogram 3.x
- requests
