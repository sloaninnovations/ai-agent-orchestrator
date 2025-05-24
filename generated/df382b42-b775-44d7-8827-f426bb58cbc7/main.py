from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': datetime.now().strftime('%H:%M:%S')}

@app.route('/date')
def get_current_date():
    return {'date': datetime.now().strftime('%Y-%m-%d')}

if __name__ == '__main__':
    app.run(debug=True)