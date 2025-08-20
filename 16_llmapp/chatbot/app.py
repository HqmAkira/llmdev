# VS Codeのデバッグ実行で `from chatbot.graph` でエラーを出さない対策
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, make_response 
from chatbot.graph import get_bot_response, get_messages_list, memory

# Flaskアプリケーションのセットアップ
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # GETリクエスト時は初期メッセージ表示
    if request.method == 'GET':
        # メモリをクリア
        memory.storage.clear()
        # 対話履歴を初期化
        response = make_response(render_template('index.html', messages=[]))
        return response

    # ユーザーからのメッセージを取得
    user_message = request.form['user_message']
    
    # ボットのレスポンスを取得（メモリに保持）
    get_bot_response(user_message, memory)

    # メモリからメッセージの取得
    messages = get_messages_list(memory)

    # レスポンスを返す
    return make_response(render_template('index.html', messages=messages))

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template, request, make_response 

# # メッセージを保存するグローバル変数
# messages = []

# # Flaskアプリケーションのセットアップ
# app = Flask(__name__)

# # 応答を作成する関数
# def get_bot_response(user_message):
#     return f"あなたが言ったのは: {user_message}"

# @app.route('/', methods=['GET', 'POST'])
# def index():

#     # GETリクエスト時は初期メッセージ表示
#     if request.method == 'GET':
#         # 対話履歴を初期化
#         response = make_response(render_template('index.html', messages=[]))
#         return response

#     # ユーザーからのメッセージを取得
#     user_message = request.form['user_message']
    
#     # ボットのレスポンスを取得
#     bot_message = get_bot_response(user_message)

#     # 対話履歴に追加
#     messages.append(user_message)
#     messages.append(bot_message)

#     # レスポンスを返す
#     return make_response(render_template('index.html', messages=messages))

# if __name__ == '__main__':
#     app.run(debug=True)