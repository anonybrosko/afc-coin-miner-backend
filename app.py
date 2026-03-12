from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import threading
import os

from telebot import TeleBot
from telebot.types import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = TeleBot(TOKEN)

app = Flask(__name__)
CORS(app)

balance = 0
clicks = 0

@app.route("/")
def index():
    return "AFC Coin Miner backend is running!"

@app.route(f"/bot/webhook", methods=["POST"])
def webhook():
    json_data = request.get_json()

    if "message" in json_data:
        update = Update.de_json(json_data)
        bot.process_new_updates([update])
    else:
        print("Webhook recieved non-message JSON", json_data)

    return jsonify({"status": "ok"})

@bot.message_handler(commands=['start'])
def start(msg):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Go to Mine 🪙",
            web_app=WebAppInfo(url="https://anonybrosko.github.io/afc-coin-miner-frontend")
        )
    )

    bot.send_message(msg.chat.id, "Welcome! Click below to mine!", reply_markup=keyboard)

@app.route("/mine")
def mine():
    global balance
    global clicks

    reward = random.randint(1, 5)  # 1-5 AFC Coin
    balance += reward
    clicks += 1
 
    return jsonify({
        "reward": reward, 
        "balance": balance, 
        "clicks": clicks
    })

# Start both
# -----------------
if __name__ == "__main__":
    HEROKU_URL = os.environ.get("BACKEND_URL")
    bot.remove_webhook()
    bot.set_webhook(url=f"{HEROKU_URL}/bot/webhook")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
