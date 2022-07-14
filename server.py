import random
from flask import Flask, render_template
import json

app = Flask(__name__)

keys = []

@app.route('/')
@app.route('/about')
def about():
    return render_template('info.html')

@app.route("/game")
def game():
    return str(len(keys))

@app.route("/ready")
def ready():
    if len(keys)  < 2:
        key = str(random.random())
        keys.append(key)
        if len(keys) == 1:
            return json.dumps({"key": key, "con": 'game', "color": 'red'})
        elif len(keys) == 2:
            return json.dumps({"key": key, "con": 'game', "color": 'yellow'})
    else:
        return "full"

@app.route("/clear")
def clear():
    keys.clear()
    return 'done'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)