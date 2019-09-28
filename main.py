from flask import Flask, render_template, request, redirect
import flask
import pymysql
from db_hanshu import check_user_name, user_reg, check_uname_pwd, WriteInfor, findall, date_str, check_ID, upda_infor, check_sell, save_infor


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

# 查看库存
@LHL.route("/MMBE")
def MMBE():
    is_login = request.cookies.get("is_login")
    if is_login:
        return render_template("MMBE.html")
    else:
        return redirect("/login")

# 库存接口
@LHL.route("/cmmbe")
def cmmbe():
    kc = {}
    data = findall("kucun")
    a = 0
    for x in data:
        # date_str(data):datetime.date类型转换为字符型
        kc[a] = {"ID": x[0], "TradeName": x[1], "ProducData": date_str(x[2]), "RDate": date_str(x[3]), "ShelfLife": x[4], "Pprice": x[5], "Price": x[6], "Inventory": x[7]}
        a += 1
    return flask.jsonify(kc)

# 修改商品信息
@LHL.route("/infor")
def infor():
    is_login = request.cookies.get("is_login")
    if is_login:
        return render_template("infor.html")
    else:
        return redirect("/login")


# 校验是否更新成功
@LHL.route("/check_updata")
def check_updata():
    # ch_up:up, up成功1，失败0
    ID = request.args.get("ID")  # 商品ID
    Price = request.args.get("Price")  # 售价
    TradeName = request.args.get("TradeName")  # 商品名
    RDate = request.args.get("RDate")  # 入库日期
    Pprice = request.args.get("Pprice")  # 进价
    QuantityIn = request.args.get("QuantityIn")  # 库存
    data = (ID, Price, TradeName, RDate, Pprice, QuantityIn)
    print(data)
    up = upda_infor(data)  # 成功返回1 失败返回0
    rsp["ch_up"] = up
    # return render_template("infor.html")
    return flask.jsonify(rsp)

# 校验商品ID是否存在
@LHL.route("/check_ID")
def Check_ID():
    ID = request.args.get("ID")
    ck = check_ID(ID)
    rsp = {"err": ck}
    return flask.jsonify(rsp)

# 出售商品
@LHL.route("/sell")
def sell():
    is_login = request.cookies.get("is_login")
    if is_login:
        return render_template("sell.html")
    else:
        return redirect("/login")

@LHL.route("/Check_sell")
def Check_sell():
    ID = request.args.get("ID")
    rsp = check_sell(ID)
    print(rsp)
    return rsp


@LHL.route("/Save_sell")
def Save_sell():

    ID = request.args.get("ID")                    # ID
    Num = request.args.get("Num")                  # 出售商品数量
    pay = request.args.get("pay")    # 盈利
    kucun = request.args.get("kucun")    # 剩余库存
    data = (Num, pay, kucun, ID)
    print(data)
    r = save_infor(data)
    # 成功1 失败0
    s = {"err": r}
    print(s)
    return s


if __name__ == "__main__":
    # LHL.run(host="0.0.0.0", port=80, debug=True)
    LHL.run(port=80, debug=True)


