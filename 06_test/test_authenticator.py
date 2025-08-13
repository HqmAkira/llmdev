import pytest
from authenticator import Authenticator

# registerのテスト
@pytest.fixture
def authenticator():
    auth = Authenticator()
    auth.register("existed_username", "existed_password")
    yield auth
    auth.users.clear()

# 成功_新規ユーザーの登録テスト
def test_register_success(authenticator):
    username = "new_username"
    password = "new_password"

    authenticator.register(username, password)
    assert username in authenticator.users
    assert authenticator.users[username] == password

# 失敗_既存ユーザーの登録テスト
def test_register_fail_already_exist_user(authenticator):
    username = "existed_username"
    password = "existed_password"

    with pytest.raises(ValueError, match="エラー: ユーザーは既に存在します。"):
        authenticator.register(username, password)


# 成功_ログインテスト
def test_login_success(authenticator):
    username = "existed_username"
    password = "existed_password"

    assert authenticator.login(username, password) == "ログイン成功"

# 失敗_ユーザー名またはパスワードが間違っている場合のログインテスト
@pytest.mark.parametrize("username, password", [
    ("new_username", "new_password"),
    ("new_username", "existed_password"),
    ("existed_username", "new_password"),
])
def test_login_fail_wrong_username_or_password(authenticator, username, password):
    with pytest.raises(ValueError, match="エラー: ユーザー名またはパスワードが正しくありません。"):
        authenticator.login(username, password)