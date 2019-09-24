from flask import Flask, render_template, request, redirect
import flask
import pymysql
from db_hanshu import check_user_name, user_reg, check_uname_pwd, WriteInfor

LHL = Flask(__name__)

@LHL.route("/")
def home():
    is_login = request.cookies.get("is_login")
    return render_template("home.html", is_login=is_login)

# 注册
@LHL.route("/register", methods=["GET","POST"])
def register():
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
    return flask.jsonify(rsp)    # 将字典转换为json格式返回

# 登录
@LHL.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
            return render_template("login.html")
    elif request.method == "POST":
        user_name = request.form.get("user_name")
        user_pwd = request.form.get("user_pwd")

        # 登录成功返回0，失败返回1
        if not check_uname_pwd(user_name, user_pwd):
            # 登录成功
            # 返回主页面
            rsp = redirect("/")
            # 设置Cookie值，如果登录成功则Cookie值is_login = "1" ,max_age值为Cookie值有效时间
            rsp.set_cookie("is_login", "1", max_age=24*60*60)
            return rsp
            # return render_template("after_login.html")
        else:
            # 登录失败
            # 显示登录失败页面
            return render_template("login_fail.html")

@LHL.route("/after_login", methods=["GET","POST"])
def after_login():
    # 获取cookie值
    is_login = request.cookies.get("is_login")
    print(is_login)
    if is_login:
        if request.method == "GET":
            return render_template("after_login.html")
        elif request.method == "POST":
            # ID = request.form.get("ID")                    # 商品ID
            TradeName = request.form.get("TradeName")     # 商品名
            ProducData = request.form.get("ProducData")   # 生产日期
            RDate = request.form.get("RDate")             # 入库日期
            ShelfLife = request.form.get("ShelfLife")     # 保质期
            Pprice = request.form.get("Pprice")           # 进价
            QuantityIn = request.form.get("QuantityIn")   # 进货数量
            data = (TradeName, ProducData, RDate, ShelfLife, Pprice, QuantityIn)
            # rsp = {}
            if WriteInfor(data):
                rsp["err"] = 1
            else:
                rsp["err"] = 0
            return render_template("after_login.html")
    else:
        # 跳转到登录界面
        return redirect("/login")
rsp = {}
@LHL.route("/check_cunchu")
def check_cunchu():
    return flask.jsonify(rsp)

if __name__ == "__main__":
    LHL.run(host="0.0.0.0", port=80, debug=True)



