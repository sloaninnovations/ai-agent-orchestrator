from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/faq')
def faq():
    faq_info = {
        "Question1": "Answer1",
        "Question2": "Answer2",
        "Question3": "Answer3"
    }
    return jsonify(faq_info)

@app.route('/contact')
def contact():
    contact_info = {
        "Email": "example@example.com",
        "Phone": "+123456789",
        "Address": "123, Example Street, Example City, Example Country"
    }
    return jsonify(contact_info)

if __name__ == '__main__':
    app.run(debug=True)