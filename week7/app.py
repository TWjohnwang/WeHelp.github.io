from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for
from flask import session
from mysql.connector.pooling import MySQLConnectionPool

connection = MySQLConnectionPool(user="root",
                    password="",
                    host="localhost",
                    port="3306",
                    database="website",
                    pool_name = "test",
                    pool_size=1)

app = Flask(__name__)

app.secret_key = "P@ssw0rd"

@app.route("/")
def index():
    if "username" in session:
        return redirect("/member")
    return render_template("index.html")

@app.route("/member")
def member():
    if "username" in session:
        try:
            member_connection = connection.get_connection()
            with member_connection.cursor() as cursor:
                select_name = ("SELECT name FROM member WHERE id = %(id)s;")
                cursor.execute(select_name, {"id": session["id"]})
                sql_data = cursor.fetchone()
        except:
            print("Unexpected Error")
        finally:
            member_connection.close()
            return render_template("member.html", text=sql_data[0])
    return redirect("/")

@app.route("/error")
def error():
    text = request.args.get("message", None)
    return render_template("error.html", text=text)

@app.route("/signout")
def signout():
    session.clear()
    return redirect("/")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    try:
        signup_connection = connection.get_connection()
        with signup_connection.cursor() as cursor:
            select_username = ("SELECT username FROM member WHERE username = %(username)s;")
            cursor.execute(select_username, {"username": username})
            sql_data = cursor.fetchone()
            if not sql_data:
                # 新增會員資料到資料庫
                insert_user = ("INSERT INTO member(name, username, password) "
                            "VALUES(%s, %s, %s)")
                user_data = (name, username, password)
                cursor.execute(insert_user, user_data)
                signup_connection.commit()
                return redirect("/")
            else:
                text = "帳號已經被註冊"
                return redirect(url_for("error", message=text))
    except:
        print("Unexpected Error")
    finally:
        signup_connection.close()

@app.route("/signin", methods=["POST"])
def verification():
    username = request.form["username"]
    password = request.form["password"]
    try:
        signin_connection = connection.get_connection()
        with signin_connection.cursor() as cursor:
            # 從資料庫查詢對應的帳號及密碼
            select_username = ("SELECT username, password, name, id FROM member WHERE username = %(username)s AND password = %(password)s;")
            cursor.execute(select_username, {'username': username, 'password':password})
            sql_data = cursor.fetchone()
        if sql_data and username == sql_data[0] and password == sql_data[1]:
            session["username"] = username
            session["password"] = password
            session["name"] = sql_data[2]
            session["id"] = sql_data[3]
            return redirect("/member")
        else:
            if not username or not password:
                text = "請輸入帳號、密碼"
                return redirect(url_for("error", message=text))
            text = "帳號、或密碼輸入錯誤"
            return redirect(url_for("error", message=text))
    except:
        print("Unexpected Error")
    finally:
        signin_connection.close()

@app.route("/api/member/", methods=["GET", "PATCH"])
def api():
    username = request.args.get("username", None)
    if session and request.method == "GET":
        try:
            api_connection = connection.get_connection()
            with api_connection.cursor() as cursor:
                search = ("SELECT id, name, username FROM member WHERE username = %(username)s")
                cursor.execute(search, {"username": username})
                sql_data = cursor.fetchone()
            return jsonify({
                "data": {
                        "id": sql_data[0],
                        "name": sql_data[1],
                        "username": sql_data[2] 
                        }
                    })
        except:
            return jsonify(data=None)
        finally:
            api_connection.close()
    elif session and request.method == "PATCH":
        try:
            api_connection = connection.get_connection()
            with api_connection.cursor() as cursor:
                update = ("UPDATE member SET name = %(name)s WHERE member.id = %(id)s;")
                cursor.execute(update, {"name": request.json["name"], "id": session["id"]})
                api_connection.commit()
            return jsonify(ok=True)
        except:
            return jsonify(error=True)
        finally:
            api_connection.close()
    return jsonify(data=None)

app.run(port=3000)