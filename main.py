from flask import Flask, render_template, request
import flask
import pymysql
from db_hanshu import check_user_name, user_reg, check_uname_pwd

LHL = Flask(__name__)

@LHL.route("/")
def home():
    return render_template("home.html")

@LHL.route("/register", methods=["GET","POST"])
def register():   # 注册
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        user_name = request.form.get("user_name")
        user_pwd = request.form.get("user_pwd")
        # 写入数据库
        if user_reg(user_name, user_pwd):
            return render_template("login.html")   # 渲染模板
        else:
            return render_template("register.html")

# 校验用户名是否存在
@LHL.route("/check_uname")
def check_uname():
    user_name = request.args.get("user_name")
    rsp = {}
    CheckCode = check_user_name(user_name)
    # 用户名存在返回1，不存在返回0
    rsp["err"] = CheckCode
    print(rsp)
    return flask.jsonify(rsp)    # 将字典转换为json格式返回

@LHL.route("/login", methods=["GET","POST"])
def login():   # 登录
    if request.method == "GET":
            return render_template("login.html")
    elif request.method == "POST":
        user_name = request.form.get("user_name")
        user_pwd = request.form.get("user_pwd")

        # 登录成功返回0，失败返回1
        if not check_uname_pwd(user_name, user_pwd):
            # 登录成功
            # 返回主页面
            # rsp = redirect("/")
            # # 设置Cookie值，如果登录成功则Cookie值is_login = "1" ,max_age值为Cookie值有效时间
            # rsp.set_cookie("is_login", "1", max_age=60*60)
            return render_template("after_login.html")
        else:
            # 登录失败
            # 显示登录失败页面
            return render_template("login_fail.html")

if __name__ == "__main__":
    LHL.run(host="0.0.0.0", port=80, debug=True)



