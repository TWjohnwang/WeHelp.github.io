# 要求四：Dynamic Routing (Optional)
# 使⽤者可以透過⾸⾴，輸入⼀個正整數，將此正整數透過動態路由 (Flask Dynamic Routing)
# 的技巧，傳遞到後端進⾏平⽅運算，並在⾴⾯中輸出結果。

from flask import Flask, request, redirect, url_for, render_template, session

app = Flask(__name__, static_folder="file", static_url_path="/")

app.secret_key = "P@ssw0rd"

@app.route("/", methods=["GET", "POST"])
def index():
    if 'account' in session:
        return render_template("logout.html")
    elif request.method == "POST":
        # 取得 requirement4.html input name="square" 的 value
        num = request.form["square"] 
    # url_for()函數用於構建指定函數的 URL
    # 把函數名稱作為第一個參數，可以接受任意個關鍵字參數
    # 每個關鍵字參數對應 URL 中的變數，並添加到 URL 中作為查詢參數
    # url_for 是產生「網址路由」，不是執行函數，也不是重新導向！
        return redirect(url_for("calculate", num=num)) 
    return render_template("/requirement4.html")

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

@app.route("/square/<num>", methods=["GET", "POST"])
def calculate(num):
    num = int(num)
    num **= 2
    return render_template("square.html", num=num)

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

# # https://stackoverflow.com/questions/71071835/flask-creating-dynamic-url-based-on-user-input