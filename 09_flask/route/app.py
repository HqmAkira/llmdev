from flask import Flask

app = Flask(__name__)

# ルーティングの基本
@app.route('/')
def index():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)