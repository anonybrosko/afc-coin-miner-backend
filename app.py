from flask import Flask, jsonify
from flask_cors import CORS
import random
import threading

from telebot import telebot
from telebot.types import InLineKeyboardButton, InLineKeyboardMarkup, WebAppInfo

app = Flask(__name__)
CORS(app)

balance = 0
clicks = 0

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

# -----------------
# Telegram Bot
# -----------------
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Go to Mine 🪙",
            web_app=WebAppInfo(url="https://afc-coin-miner.netlify.app/")
        )
    )

    bot.send_message(
        msg.chat.id,
        "Welcome! Click below to mine:",
        reply_markup=keyboard
    )


# Run bot in background thread
def run_bot():
    print("Telegram bot started")
    bot.infinity_polling()


# -----------------
# Start both
# -----------------
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
