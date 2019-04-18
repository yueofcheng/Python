from flask import Flask, render_template, redirect
import requests
import pymysql
app = Flask(__name__)


@app.route('/')
def index():
    return redirect("name/cucnews")


@app.route('/name/<table>')
@app.route('/name/<table>/<page>')
def select(table, page=1):
    db = pymysql.connect('localhost', 'root', 'password', 'news')
    cursor = db.cursor()
    sql = "select * from %s" % table
    try:
        rscount = cursor.execute(sql)  # 返回记录数
        rs = cursor.fetchall()
    except:
        print("Error")
    db.close()

    page = int(page) - 1
    return render_template("select.html", count=int(rscount / 6) + 1, rs=rs, page=page)


@app.route('/detail/<newid>')
def detail(newid):
    db = pymysql.connect('localhost', 'root', 'chengyiyi422', 'news')
    cursor = db.cursor()
    sql = "select * from cucnews where id = %s" % newid
    try:
        rscount = cursor.execute(sql)  # 返回记录数
        rs = cursor.fetchone()
        #s = rs[5].replace("\r\n", '')
        s = rs[5].split("\r\n")
        new = []
        for r in s:
            if r.isspace():
                print("h")
            else:
                r.strip()
                r = r.replace("\n", '').replace("\t", '')
                new.append(r)
    except:
        print("Error")
    db.close()
    return render_template("detail.html", rs=rs, news=new)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)
