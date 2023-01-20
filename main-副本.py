from flask import Flask
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import time
from forms import ArticleForm

app = Flask(__name__)#创建一个该类的实例，第一个参数是应用模块或者包的名称

@app.route('/')#告诉Flask 什么样的URL能触发函数
def hello_world():
    return 'Hello World!'

from functools import wraps
# 如果用户已经登录
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:     # 判断用户是否登录
            return f(*args, **kwargs)  # 如果登录，继续执行被装饰的函数
        else:                          # 如果没有登录，提示无权访问
            flash('无权访问，请先登录', 'danger')
            return redirect(url_for('login'))
    return wrap


# 控制台
@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
        result = [{"id":1,"title":"Python运维开发","author":"xiaoli","create_date":"2022-12-4 12:20:000"}]
        if result: # 如果笔记存在，赋值给articles变量
            return render_template('dashboard.html', articles=result)
        else:      # 如果笔记不存在，提示暂无笔记
            msg = '暂无笔记信息'
            return render_template('dashboard.html', msg=msg)

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "logged_in" in session:  # 如果已经登录，则直接跳转到控制台
        return redirect(url_for("dashboard"))

    if request.method == 'POST': # 如果提交表单
        # 从表单中获取字段
        username = request.form['username']
        password_candidate = request.form['password']
        if username=="zhangsan" and password_candidate =="123456" : # 如果查到记录
            # 写入session
            session['logged_in'] = True
            session['username'] = username
            flash('登录成功！', 'success') # 闪存信息
            return redirect(url_for('dashboard')) # 跳转到控制台
        else:  # 如果密码错误
            error = '用户名和密码不匹配'
            return render_template('login.html', error=error) # 跳转到登录页，并提示错误信息

    return render_template('login.html')


# 添加笔记
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form) # 实例化ArticleForm表单类
    if request.method == 'POST':
        # 如果用户提交表单，并且表单验证通过
        # 获取表单字段内容
        title = form.title.data
        content = form.content.data

        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(title,content,create_date)
        flash('创建成功','success')
        result = [{"id":2,"title":"Python运维开发","author":"xiaoli","create_date":"2022-12-4 12:20:000"}]

        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)   # 渲染模板
    



if __name__ == '__main__':#程序入口
    #app.run()#让应用运行在本地服务器上。
    app.secret_key='secret123'
    app.run( host='0.0.0.0',port="5006",debug="True") #允许任意网址访问本站
