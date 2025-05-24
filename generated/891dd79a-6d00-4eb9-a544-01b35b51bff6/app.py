from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/random')
def random_number():
    return jsonify(number=random.randint(1, 100))

@app.route('/quote')
def quote():
    return jsonify(quote="The only way to do great work is to love what you do. - Steve Jobs")

if __name__ == '__main__':
    app.run(debug=True)