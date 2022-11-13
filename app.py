# splite3をimportする
from contextlib import redirect_stderr
from pydoc import pager
import sqlite3
from tkinter import E
from turtle import title
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect , session
from datetime import datetime
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)

# Flask では標準で Flask.secret_key を設定すると、sessionを使うことができます。この時、Flask では session の内容を署名付きで Cookie に保存します。
app.secret_key = 'sunabakoza'

@app.route('/')
def index():
    return render_template('/login.html')

@app.route("/login", methods=["GET"])
def login_post():
    if 'session_id' in session:
        return redirect("/top")
    else:
        return render_template("student_login.html")

@app.route("/student_login", methods=["POST"])
def teacher_login_post():
    # ブラウザから送られてきたデータを受け取る
    user_id_stu = request.form.get("user_id_stu")
    password_stu = request.form.get("password_stu")
    conn = sqlite3.connect('rakuren.db')
    c = conn.cursor()
    c.execute("SELECT user_id_stu FROM student WHERE user_id = ? AND password = ?", (user_id_stu, password_stu))
    session_id = c.fetchone()
    conn.close()
    session["user_id_stu"] = session_id
    return redirect("/top")

@app.route("/login", methods=["GET"])
def login_post():
    if 'session_id' in session:
        return redirect("/select")
    else:
        return render_template("teather_login.html")

@app.route("/teacher_login", methods=["POST"])
def teacher_login_post():
    # ブラウザから送られてきたデータを受け取る
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    conn = sqlite3.connect('rakuren.db')
    c = conn.cursor()
    c.execute("SELECT user_id FROM teacher WHERE user_id = ? AND password = ?", (user_id, password))
    session_id = c.fetchone()
    conn.close()
    session["user_id"] = session_id
    return redirect("/select")


# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "GET":
#         #先生のログイン
#         if 'session_id' in session:
#             return redirect("/select")
#         else:
#             return render_template("login.html")
#     else:
#         # ブラウザから送られてきたデータを受け取る
#         user_id = request.form.get("user_id")
#         password = request.form.get("password")
#         user_id_stu = request.form.get("user_id_stu")
#         password_stu = request.form.get("password_stu")

#         # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
#         
#         else:
#             conn = sqlite3.connect('rakuren.db')
#             c = conn.cursor()
#             c.execute("SELECT user_id FROM student WHERE user_id = ? AND password = ?", (user_id_stu, password_stu))
#             print('ログイン')
#             session_id = c.fetchone()
#             conn.close()

#         # session_id が NULL(PythonではNone)じゃなければログイン成功
#         if session_id is None:
#             # ログイン失敗すると、ログイン画面に戻す
#             return render_template("login.html")
#         else:
#             if user_id_stu is None:
#                 session['session_id'] = user_id
#                 return redirect("/select")
#             else:
#                 session['session_id'] = user_id_stu
#                 return redirect("/top")
                
@app.route("/logout")
def logout():
    session.pop('session_id',None)
    # ログアウト後はログインページにリダイレクトさせる
    return redirect("/login")

@app.route('/select')
def select():
    if 'session_id' in session :
        print('session_id')
        return render_template("select.html")
    else:
        return redirect("/login")

@app.route("/select", methods=["GET"])
def select_get():
    if request.method == "GET":
        if 'session_id' in session :     
            return render_template("register_stu.html")
        else:
            return render_template("login.html")
    else:
        return redirect("/select")

# GET  /register => 登録画面を表示
# POST /register => 登録処理をする
@app.route('/register',methods=["GET", "POST"])
def register():
    #  登録ページを表示させる
    if request.method == "GET":
        if 'session_id' in session :
            return redirect ('/login')
        else:
            return render_template("register.html")
    # ここからPOSTの処理
    else:
        user_name = request.form.get("user_name")
        user_id = request.form.get("user_id")   
        password = request.form.get("password")

        conn = sqlite3.connect('rakuren.db')
        c = conn.cursor()
        c.execute("insert into teacher values(null,?,?,?)", (user_name,user_id,password))
        conn.commit()
        conn.close()
        return redirect('/login')


@app.route('/register_stu',methods=["GET", "POST"])
def register_stu():
    #  登録ページを表示させる
    if request.method == "GET":
        if 'session_id' in session :
            teacher_id = "matsui"
            conn = sqlite3.connect('rakuren.db')
            c = conn.cursor()
            c.execute("SELECT user_number,user_id,user_name,password FROM student WHERE teacher_id = ? order by user_number", (teacher_id,))
            user_list = []
            for row in c.fetchall():
                user_list.append({ "user_number": row[0], "user_id": row[1], "user_name": row[2], "password_stu": row[3]})
            c.close()            
            return render_template("register_stu.html", user_list = user_list)
        else:
            return redirect("/login")

    else:
        user_id = request.form.get("user_id")   
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        teacher = 'matsui'

        conn = sqlite3.connect('rakuren.db')
        c = conn.cursor()
        c.execute("INSERT INTO student values(null,?,?,?,?)", (user_id,user_name,teacher,password))
        conn.commit()
        conn.close()
        return redirect ('/register_stu')

@app.route("/del/<int:user_number>")
def del_stu(user_number):

    if "session_id" in session:

        #編集対象のIDを取得
        item_id = request.form.get(user_number)

    #DBに接続
        conn = sqlite3.connect("rakuren.db")

    #DBを操作できるようにする
        c = conn.cursor()

    #SQLを実行してCreateする
        c.execute("DELETE FROM student WHERE user_number = ?" , (user_number,))
    #    task = c.fetchone()

    #DBの変更を保存
        conn.commit()

    #DBに接続を切る
        c.close()
        return redirect("/register_stu")
    
    else:
        return redirect("/login")


@app.route("/add",methods=["GET"])
def add_get():
    if "session_id" in session:
        print("session_id")
        return render_template("add.html")
    else :
        return redirect("/login")
 
@app.route("/add", methods=["POST"])
def add_post():
    if "session_id" in session:
        session_id = session["session_id"][0]
        # フォームから入力されたアイテム名の取得
        time = datetime.now()
        time = time.strftime('%Y/%m/%d %H:%M:%S')
        student_id = "yamada"
        student_name = "山田"
#        condition = request.form.get("user_id")
#        condition_add = request.form.get("user_id")
        condition = "健康"
        condition_add = "元気です"
        learning = request.form.get("learning")
        mochimono = request.form.get("mochimono")
        school_lunch = request.form.get("school_lunch")

        conn = sqlite3.connect("rakuren.db")
        c = conn.cursor()
        # DBにデータを追加する
        c.execute("INSERT INTO contactbook values (null,?,?,?,?,?,?,?,?,?)", (session_id, student_id, student_name,mochimono,condition,condition_add,school_lunch,learning,time))
        conn.commit()
        c.close()
        return redirect("/select")
    else :
        return redirect("/login")

@app.route('/top', methods=["GET"])
def comment():
    if 'session_id' in session :
#        date = datetime.date.today()
        student_id = "yamada"
        conn = sqlite3.connect('rakuren.db')
        c = conn.cursor()
        c.execute("SELECT student_id,student_name,mochimono,condition,condition_add,school_lunch,learning,date FROM contactbook WHERE student_id = ? AND date = (SELECT MAX(date) FROM contactbook)", (student_id,))
        book_list = c.fetchone()
        print("---------")
        print(book_list)
        print("---------")
        c.close()
        return render_template("top.html", book_list = book_list)
    else:
        return redirect("/login")


@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@app.errorhandler(404)
def notfound404(code):
    return "404だよ！！見つからないよ！！！"


# __name__ というのは、自動的に定義される変数で、現在のファイル(モジュール)名が入ります。 ファイルをスクリプトとして直接実行した場合、 __name__ は __main__ になります。
if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run(debug=False)