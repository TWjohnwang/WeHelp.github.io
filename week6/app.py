from flask import Flask, request, redirect, url_for, render_template, session
import mysql.connector

connection = mysql.connector.connect(user='root', password='zxc6325551',
                                    host='localhost',
                                    port='3306',
                                    database="website")
cursor = connection.cursor()

app = Flask(__name__)

app.secret_key = "P@ssw0rd"

@app.route("/")
def index():
    if 'username' in session:
        cursor.execute("SELECT name, content FROM member JOIN message ON  member.id = member_id ORDER BY message.time;")
        sql_data = cursor.fetchall()
        return render_template("logout.html", text=session["name"], len=len(sql_data), message=[[i[0], i[1]] for i in sql_data])
    return render_template("index.html")

@app.route("/member")
def signin():
    if 'username' in session:
        cursor.execute("SELECT name, content FROM member JOIN message ON  member.id = member_id ORDER BY message.time;")
        sql_data = cursor.fetchall()
        return render_template("logout.html", text=session["name"], len=len(sql_data), message=[[i[0], i[1]] for i in sql_data])
    return redirect("/")

@app.route("/error")
def error():
    text = request.args.get("message", None)
    return render_template("error.html", text=text)

@app.route("/signout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    cursor.execute(f'SELECT username FROM member WHERE username = "{username}";')
    sql_data = cursor.fetchone()
    if not sql_data:
        # 新增會員資料到資料庫
        cursor.execute(f'INSERT INTO member(name, username, password) VALUES("{name}", "{username}", "{password}");')
        connection.commit()
        return redirect("/")
    else:
        text = "帳號已經被註冊"
        return redirect(url_for("error", message=text))

@app.route("/signin", methods=["POST"])
def verification():
    username = request.form["username"]
    password = request.form["password"]
    # 從資料庫查詢對應的帳號及密碼
    cursor.execute(f'SELECT username, password, name FROM member WHERE username = "{username}";')
    sql_data = cursor.fetchone()
    if sql_data:
        if username == sql_data[0] and password == sql_data[1]:
            session["username"] = username
            session["password"] = password
            session["name"] = sql_data[2]
            return redirect("/member")
    else:
        if not username or not password:
            text = "請輸入帳號、密碼"
            return redirect(url_for("error", message=text))
        else:
            text = "帳號、或密碼輸入錯誤"
            return redirect(url_for("error", message=text))
        
@app.route("/message", methods=["POST"])
def message():
    if 'username' in session:
        name = session["username"]
        content = request.form["content"]
        cursor.execute(f'INSERT INTO message(member_id, content) VALUES((SELECT member.id FROM member WHERE member.username = "{name}"), "{content}");')
        connection.commit()
        return redirect("/member")
    return redirect("/")
    
app.run(port=3000)
