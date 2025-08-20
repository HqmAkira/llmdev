# VS Codeのデバッグ実行で `from chatbot.graph` でエラーを出さない対策
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from flask import Flask, render_template, request, make_response, session 
from original.graph import get_bot_response, get_messages_list, change_character_response, get_character, memory

# Flaskアプリケーションのセットアップ
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション用の秘密鍵

def get_character_message_from_form(request):
    try:
        return request.form['character_message']
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    # セッションからthread_idを取得、なければ新しく生成してセッションに保存
    if 'thread_id' not in session:
        session['thread_id'] = str(uuid.uuid4())  # ユーザー毎にユニークなIDを生成

    current_character = get_character()
    # GETリクエスト時は初期メッセージ表示
    if request.method == 'GET':
        # メモリをクリア
        memory.storage.clear()
        # 対話履歴を初期化
        response = make_response(render_template('index.html', messages=[], current_character=current_character))
        return response
    

    character_message = get_character_message_from_form(request)
    print(f"Character message: {character_message}")
    if character_message:
        # キャラクター変更の処理
        messages = []
        try:
            messages = get_messages_list(memory, session['thread_id'])
        except:
            messages = []
        new_character = change_character_response(character_message)
        return make_response(render_template('index.html', messages=messages, current_character=new_character))

    # ユーザーからのメッセージを取得
    user_message = request.form['user_message']
    
    # ボットのレスポンスを取得（メモリに保持）
    get_bot_response(user_message, memory, session['thread_id'])

    # メモリからメッセージの取得
    messages = get_messages_list(memory, session['thread_id'])

    print(f"messages: {messages}")

    # レスポンスを返す
    return make_response(render_template('index.html', messages=messages, current_character=current_character))

@app.route('/clear', methods=['POST'])
def clear():
    current_character = get_character()
    # セッションからthread_idを削除
    session.pop('thread_id', None)

    # メモリをクリア
    memory.storage.clear()
    # 対話履歴を初期化
    response = make_response(render_template('index.html', messages=[], current_character=current_character))
    return response

if __name__ == '__main__':
    app.run(debug=True)
