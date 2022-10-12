# 要求⼆：建立帳號密碼驗證功能
# 使⽤者可以透過⾸⾴輸入帳號密碼，並且將帳號密碼透過 Form 表單的 POST ⽅法傳送到後
# 端程式進⾏驗證，根據驗證結果，將使⽤者導向到成功、或失敗的⾴⾯。

from flask import Flask, request, redirect, url_for
from flask import render_template

app = Flask(__name__, static_folder="file", static_url_path="/")

@app.route("/")
def index():
    return render_template("requirement2.html")

@app.route("/member")
def signin():
    return render_template("member.html")

@app.route("/error")
def error():
    text = request.args.get("message", None)
    return render_template("error.html", text=text)

@app.route("/signin", methods=["POST"])
def verification():
    account = request.form["account"]
    password = request.form["password"]
    if account == "test" and password == "test":
        return redirect("/member")
    elif account == "" or password == "":
        text = "請輸入帳號、密碼"
        return redirect(url_for("error", message=text))
    else:
        text = "帳號、或密碼輸入錯誤"
        return redirect(url_for("error", message=text))

app.run(port=3000)