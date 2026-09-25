import asyncio
import os

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Load token from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set. Create a .env file with BOT_TOKEN=your_token")

# RemoteOK API
REMOTEOK_URL = "https://remoteok.com/api"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def search_vacancies(query, count=5):
    """Search vacancies on RemoteOK by keyword."""
    try:
        response = requests.get(REMOTEOK_URL, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            return []
        data = response.json()
    except requests.RequestException:
        return []

    jobs = [j for j in data if isinstance(j, dict) and j.get("position")]
    query_lower = query.lower()
    filtered = [
        j for j in jobs
        if query_lower in j.get("position", "").lower()
        or query_lower in [t.lower() for t in j.get("tags", [])]
    ]
    return filtered[:count]


def format_vacancy(v):
    """Format a single vacancy as an HTML message."""
    name = v.get("position") or "untitled"
    company = v.get("company") or "is not specified"
    location = v.get("location") or "Remote"
    url = v.get("url") or ""

    salary_min = v.get("salary_min")
    salary_max = v.get("salary_max")
    if salary_min and salary_max:
        salary = f"${salary_min}–${salary_max}"
    elif salary_min:
        salary = f"from ${salary_min}"
    elif salary_max:
        salary = f"to ${salary_max}"
    else:
        salary = "is not specified"

    return (
        f"💼 <b>{name}</b>\n"
        f"🏢 {company}\n"
        f"📍 {location}\n"
        f"💰 {salary}\n"
        f"🔗 <a href='{url}'>Open</a>"
    )


# Bot initialization
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Hi! I search for job vacancies on RemoteOK.\n\n"
        "Just send me a keyword — for example, <b>Python</b> or <b>analyst</b>.\n\n"
        "Commands:\n"
        "/start — this message\n"
        "/help — help"
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "How to use:\n"
        "1. Send a keyword (for example, Python)\n"
        "2. I will send you 5 fresh vacancies from RemoteOK\n\n"
        "You can also search by location by adding it to your query: <code>Python New York</code>"
    )


@dp.message()
async def handle_query(message: types.Message):
    query = message.text.strip()

    if not query:
        await message.answer("Please send a keyword to search.")
        return

    await message.answer(f"🔍 Searching for vacancies: «{query}»...")

    # Run sync requests in a separate thread to avoid blocking the bot
    loop = asyncio.get_event_loop()
    vacancies = await loop.run_in_executor(None, search_vacancies, query, 5)

    if not vacancies:
        await message.answer("Nothing found. Try another keyword.")
        return

    for v in vacancies:
        await message.answer(
            format_vacancy(v),
            parse_mode="HTML",
            disable_web_page_preview=False,
        )


async def main():
    print("Bot is running. Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
