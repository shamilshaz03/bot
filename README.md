# Telegram Subscription Bot with Pyrogram

This bot is a Telegram subscription bot where users can subscribe using Google Pay, PhonePe, or Paytm. The bot also saves users' information to MongoDB.

## Setup

### Step 1: Install Requirements

Install the required Python packages using the following command:

```
pip install -r requirements.txt
```

### Step 2: Set Environment Variables

Set the following environment variables:

- `MONGO_URI`: Your MongoDB connection URI
- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API Hash
- `BOT_TOKEN`: Your Telegram bot token
- `SUBSCRIPTION_AMOUNT`: The subscription amount (default: 500 INR)
- `UPI_ID`: Your UPI ID for payments
- `SUBSCRIPTION_PHOTO`: URL of the subscription image

### Step 3: Run the Bot

Run the bot using:

```
./start.sh
```

### Step 4: Deploy to Koyeb

To deploy on Koyeb:

1. Create a new service and upload this project folder.
2. Set environment variables via the Koyeb dashboard.
3. Set the start command as `./start.sh`.

Now your bot is live on Telegram! Use `/start` to initiate and `/subscribe` to subscribe.
