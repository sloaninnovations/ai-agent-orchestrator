from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/about')
def about():
    return "About Page"

@app.route('/status')
def status():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(debug=True)