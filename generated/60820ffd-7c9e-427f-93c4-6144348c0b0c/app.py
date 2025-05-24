from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/faq')
def faq():
    faq_info = {
        "Question 1": "Answer 1",
        "Question 2": "Answer 2",
        "Question 3": "Answer 3",
    }
    return jsonify(faq_info)

@app.route('/contact')
def contact():
    contact_info = {
        "Email": "info@example.com",
        "Phone": "+1234567890",
        "Address": "123 Street, City, Country"
    }
    return jsonify(contact_info)

if __name__ == "__main__":
    app.run(debug=True)