from flask import Flask, jsonify
from flask_cors import CORS
import random

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
    return jsonify({"reward": reward, "balance": balance, "clicks": clicks})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
