# 要求三：記錄使⽤者狀態
# 延續要求⼆，進⼀步的使⽤ Session 在後端追蹤、記錄使⽤者狀態。關於 Session 的使⽤可
# 以參考 Flask Session 或任何其他文件。

from flask import Flask, request, redirect, url_for, render_template, session

app = Flask(__name__, static_folder="file", static_url_path="/")

app.secret_key = "P@ssw0rd"

@app.route("/")
def index():
    if 'account' in session:
        return render_template("logout.html")
    return render_template("requirement2.html")

@app.route("/member")
def signin():
    if 'account' in session:
        return render_template("logout.html")
    return redirect("/")

@app.route("/error")
def error():
    text = request.args.get("message", None)
    return render_template("error.html", text=text)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/signin", methods=["POST"])
def verification():
    account = request.form["account"]
    password = request.form["password"]
    session["account"] = account
    session["password"] = password
    if account == "test" and password == "test":
        return redirect("/member")
    elif account == "" or password == "":
        text = "請輸入帳號、密碼"
        return redirect(url_for("error", message=text))
    else:
        text = "帳號、或密碼輸入錯誤"
        return redirect(url_for("error", message=text))

app.run(port=3000)