import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['telegram_bot']
users_collection = db['users']

# Payment Variables
SUBSCRIPTION_AMOUNT = int(os.getenv("SUBSCRIPTION_AMOUNT", 500))  # Amount in INR
UPI_ID = os.getenv("UPI_ID", "your_upi_id@upi")  # Replace with your actual UPI ID
SUBSCRIPTION_PHOTO = os.getenv("SUBSCRIPTION_PHOTO", "https://example.com/your-photo.jpg")

# Bot Configuration
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("subscription_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Save user data to MongoDB
def save_user(user_id):
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({
            "user_id": user_id,
            "is_active": False
        })

@app.on_message(filters.command("start"))
def start(_, message):
    user_id = message.from_user.id
    save_user(user_id)
    message.reply_text("Welcome to the bot! Use /subscribe to proceed with the subscription.")

@app.on_message(filters.command("subscribe"))
def subscribe(_, message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Pay with Google Pay", url=f"https://pay.google.com/gp/p2p?u={UPI_ID}&amount={SUBSCRIPTION_AMOUNT}"),
                InlineKeyboardButton("Pay with PhonePe", url=f"phonepe://pay?amount={SUBSCRIPTION_AMOUNT}&upiId={UPI_ID}"),
                InlineKeyboardButton("Pay with Paytm", url=f"paytm://pay?amount={SUBSCRIPTION_AMOUNT}&upiId={UPI_ID}")
            ]
        ]
    )
    
    message.reply_photo(photo=SUBSCRIPTION_PHOTO, caption="Click the button to pay:", reply_markup=keyboard)

@app.on_message(filters.command("broadcast") & filters.user(12345678))  # Replace 12345678 with your admin user ID
def broadcast(_, message):
    text = message.text.split(maxsplit=1)[1]  # Get the message to broadcast
    users = users_collection.find({"is_active": True})
    for user in users:
        try:
            app.send_message(user["user_id"], text)
        except Exception as e:
            print(f"Couldn't send message to {user['user_id']}: {e}")

app.run()
