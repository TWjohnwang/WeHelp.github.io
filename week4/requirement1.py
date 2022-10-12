# 要求⼀：建立⾸⾴
# 執⾏寫好的 Python 程式，啟動 Flask 伺服器，並建立網站的⾸⾴如下。

from flask import Flask
from flask import render_template

app = Flask(__name__, static_folder="file", static_url_path="/")

@app.route("/")
def index():
    return render_template("requirement1.html")

app.run(port=3000)