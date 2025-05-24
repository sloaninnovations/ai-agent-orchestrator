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
        "Success is not the key to happiness. Happiness is the key to success.",
        "Don't be afraid to give up the good to go for the great.",
        "I find that the harder I work, the more luck I seem to have.",
        "Success usually comes to those who are too busy to be looking for it."
    ]
    return jsonify({'quote': random.choice(quotes)})

if __name__ == "__main__":
    app.run(debug=True)