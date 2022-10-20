# 要求三：記錄使⽤者狀態
# 延續要求⼆，進⼀步的使⽤ cookie 在後端追蹤、記錄使⽤者狀態。

from flask import Flask, make_response, request, redirect, url_for, render_template
import time

app = Flask(__name__, static_folder="file", static_url_path="/")

@app.route("/")
def index():
    # 判斷 cookie 的 account 及 password 是否為 test
    if request.cookies.get("account") == "test" and request.cookies.get("password") == "test":
        return render_template("logout.html")
    return render_template("requirement2.html")

@app.route("/member")
def signin():
    if  request.cookies.get("account") == "test" and request.cookies.get("password") == "test":
        return render_template("logout.html")
    return redirect("/")

@app.route("/error")
def error():
    text = request.args.get("message", None)
    return render_template("error.html", text=text)

@app.route("/logout")
def logout():
    delete = make_response(redirect("/"))
    delete.set_cookie(key="account", value='', expires=0)
    delete.set_cookie(key="password", value='', expires=0)
    return delete

@app.route("/signin", methods=["POST"])
def verification():
    account = request.form["account"]
    password = request.form["password"]
    if account == "test" and password == "test":
        # 設定後端給前端的 response 
        resp = make_response(redirect("/member"))
        # 在 Response headers 設定 cookie
        resp.set_cookie(key="account", value='test', expires=time.time()+360)
        resp.set_cookie(key="password", value='test', expires=time.time()+360)
        return resp
    elif account == "" or password == "":
        text = "請輸入帳號、密碼"
        return redirect(url_for("error", message=text))
    else:
        text = "帳號、或密碼輸入錯誤"
        return redirect(url_for("error", message=text))

app.run(port=3000)