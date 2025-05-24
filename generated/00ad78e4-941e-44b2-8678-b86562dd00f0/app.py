from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/random')
def random_number():
    number = random.randint(1, 100)
    return jsonify(number=number)

@app.route('/quote')
def quote():
    quotes = [
        "The only way to do great work is to love what you do.",
        "Don't count the days, make the days count.",
        "The greatest glory in living lies not in never falling, but in rising every time we fall.",
        "In the end, it's not the years in your life that count. It's the life in your years."
    ]
    quote = random.choice(quotes)
    return jsonify(quote=quote)

if __name__ == "__main__":
    app.run(debug=True)