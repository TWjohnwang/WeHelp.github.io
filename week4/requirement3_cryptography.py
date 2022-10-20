# 要求三：記錄使⽤者狀態
# 延續要求⼆，進⼀步的使⽤ cookie 並且利用第三方套件 cryptography 加密後在後端追蹤、記錄使⽤者狀態。

from flask import Flask, make_response, request, redirect, url_for, render_template
import time
from cryptography.fernet import Fernet
import json

app = Flask(__name__, static_folder="file", static_url_path="/")

# 產生加密金鑰
key = Fernet.generate_key()

@app.route("/")
def index():
    # 判斷 cookie 內有沒有 login
    if "Login" in request.cookies:
        return render_template("logout.html")
    return render_template("requirement2.html")

@app.route("/member")
def signin():
    if check()["account"] == "test" and check()["password"] == "test":
        return render_template("logout.html")
    return redirect("/")
def check():
    cipher_suite = Fernet(key)
    # 解密 cookie
    uncipher_login = (cipher_suite.decrypt(request.cookies.get("Login")))
    # 以 utf-8 解碼
    login = bytes(uncipher_login).decode("utf-8")
    # 以 Json 格式載入 login 字串
    login = json.loads(login)
    return login

@app.route("/error")
def error():
    text = request.args.get("message", None)
    return render_template("error.html", text=text)

@app.route("/logout")
def logout():
    delete = make_response(redirect("/"))
    delete.set_cookie(key="Login", value='', expires=0)
    return delete

@app.route("/signin", methods=["POST"])
def verification():
    account = request.form["account"]
    password = request.form["password"]
    if account == "test" and password == "test":
        cipher_suite = Fernet(key)
        # 將 account 及 password 以符合Json格式的 string 型態儲存
        login_json = f'{{"account":"{account}","password":"{password}"}}'
        # 將帳號及密碼轉換成位元組
        login = bytes(login_json, 'utf-8')
        # 加密帳號及密碼
        ciphered_login = cipher_suite.encrypt(login)
        resp = make_response(redirect("/member"))
        resp.set_cookie(key="Login", value=ciphered_login, expires=time.time()+360)
        return resp
    elif account == "" or password == "":
        text = "請輸入帳號、密碼"
        return redirect(url_for("error", message=text))
    else:
        text = "帳號、或密碼輸入錯誤"
        return redirect(url_for("error", message=text))

app.run(port=3000)