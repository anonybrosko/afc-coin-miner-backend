from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import threading
import os

from telebot import TeleBot
from telebot.types import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

app = Flask(__name__)
CORS(app)

balance = 0
clicks = 0

@app.route("/")
def index():
    return "AFC Coin Miner backend is running!"

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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
