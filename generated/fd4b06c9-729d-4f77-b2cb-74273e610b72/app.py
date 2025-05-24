from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/random', methods=['GET'])
def get_random_number():
    return jsonify({'random_number': random.randint(1, 100)})

@app.route('/quote', methods=['GET'])
def get_quote():
    quotes = [
        "The only way to do great work is to love what you do.",
        "Believe you can and you're halfway there.",
        "Don't watch the clock; do what it does. Keep going.",
        "The future belongs to those who believe in the beauty of their dreams."
    ]
    return jsonify({'quote': random.choice(quotes)})

if __name__ == '__main__':
    app.run(debug=True)