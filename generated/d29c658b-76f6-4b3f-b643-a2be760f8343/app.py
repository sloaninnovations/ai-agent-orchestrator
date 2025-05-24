from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/random')
def random_number():
    return jsonify({'random_number': random.randint(1, 100)})

@app.route('/quote')
def quote():
    quotes = [
        "The greatest glory in living lies not in never falling, but in rising every time we fall. -Nelson Mandela",
        "The way to get started is to quit talking and begin doing. -Walt Disney",
        "Your time is limited, don't waste it living someone else's life. -Steve Jobs",
        "Life is what happens when you're busy making other plans. -John Lennon"
    ]
    return jsonify({'quote': random.choice(quotes)})

if __name__ == '__main__':
    app.run(debug=True)