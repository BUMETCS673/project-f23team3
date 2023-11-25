from flask import Blueprint, Flask, render_template, url_for, request, redirect, session
import firesecure

login_layout = Blueprint('login_api', __name__)


@login_layout.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        # Handle form submission
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        # Actual Registration are handled in local file firesecure.py
        try:
            # firesecure.login_with_email 处理登录逻辑并返回用户对象
            user = firesecure.login_with_email(email, password)
            session['logged_in'] = True  # 设置会话变量标记用户已登录
            return redirect(url_for('main_menu.main_page'))  # 重定向到菜单页面
        except ValueError as err:
            return render_template("login.html", success=False, error=err)
    else:
        # Handle initial GET request to render the registration page
        return render_template("login.html")


# 我直接返回到home不行么？