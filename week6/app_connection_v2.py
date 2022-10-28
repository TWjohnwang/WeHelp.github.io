from flask import Flask, request, redirect, url_for, render_template, session
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool

connection = MySQLConnectionPool(user='root',
                    password='zxc6325551',
                    host='localhost',
                    port='3306',
                    database="website",
                    pool_name = 'signin',
                    pool_size=1)

app = Flask(__name__)

app.secret_key = "P@ssw0rd"

@app.route("/")
def index():
    if 'username' in session:
        return redirect('/member')
    return render_template("index.html")

@app.route("/member")
def signin():
    if 'username' in session:
        member_connection = connection.get_connection()
        with member_connection.cursor() as cursor:
            cursor.execute("SELECT name, content FROM member JOIN message ON member.id = member_id ORDER BY message.time;")
            sql_data = cursor.fetchall()
            member_connection.close()
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
    signup_connection = connection.get_connection()
    with signup_connection.cursor() as cursor:
        select_username = ("SELECT username FROM member WHERE username = %(username)s;")
        cursor.execute(select_username, {'username': username})
        sql_data = cursor.fetchone()
        if not sql_data:
            # 新增會員資料到資料庫
            insert_user = ("INSERT INTO member(name, username, password) "
                        "VALUES(%s, %s, %s)")
            user_data = (name, username, password)
            cursor.execute(insert_user, user_data)
            signup_connection.commit()
            signup_connection.close()
            return redirect("/")
        else:
            text = "帳號已經被註冊"
            connection.close()
            return redirect(url_for("error", message=text))

@app.route("/signin", methods=["POST"])
def verification():
    username = request.form["username"]
    password = request.form["password"]
    signin_connection = connection.get_connection()
    with signin_connection.cursor() as cursor:
        # 從資料庫查詢對應的帳號及密碼
        select_username = ("SELECT username, password, name, id FROM member WHERE username = %(username)s AND password = %(password)s;")
        cursor.execute(select_username, {'username': username, 'password':password})
        sql_data = cursor.fetchone()
        signin_connection.close()
    if sql_data:
        if username == sql_data[0] and password == sql_data[1]:
            session["username"] = username
            session["password"] = password
            session["name"] = sql_data[2]
            session["id"] = sql_data[3]
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
        id = session["id"]
        content = request.form["content"]
        signin_connection = connection.get_connection()
        with signin_connection.cursor() as cursor:
            insert_message = ("INSERT INTO message(member_id, content)"
                            "VALUES(%s, %s)")
            message_data = (id, content)
            cursor.execute(insert_message, message_data)
            signin_connection.commit()
            signin_connection.close()
        return redirect("/member")
    return redirect("/")
    
app.run(port=3000)
