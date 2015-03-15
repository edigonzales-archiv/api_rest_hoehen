#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/api/v1.0/heights', methods=['GET'])
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
