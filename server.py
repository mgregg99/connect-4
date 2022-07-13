from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
@app.route('/about')

@app.route("/game")
def game():
    return 'dev'

@app.route("/ready")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)