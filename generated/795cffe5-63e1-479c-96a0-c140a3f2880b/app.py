from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/faq')
def faq():
    return jsonify({
        "FAQ": "This is the FAQ section. We will update it soon."
    })

@app.route('/contact')
def contact():
    return jsonify({
        "Contact": "You can contact us at contact@example.com"
    })

if __name__ == '__main__':
    app.run(debug=True)