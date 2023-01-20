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
    #模拟一个笔记数据，
    #result = [{"id":1,"title":"Python运维开发","author":"xiaoli","create_date":"2022-12-4 12:20:000"}]
    result = []
    num=0
    #sample.csv内容：
    #1,Python运维开发,xiaoli,2022-12-4 12:20:00,Python运维开发是一个学习python语言的课程，非常有意思！
    
    with open('sample.csv',"r") as fr:
        for line in fr:    #文件对象可以直接迭代
            #print(line)
            r = line.split(",")
            t={}
            t['id']= r[0];t['title']=r[1];t['author']=r[2];t['update_date']=r[3];
            t['content']=r[4]#;t['zt']=r[5]
            result.append(t)
            num = num+1
            
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

# 用户登出
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')

#关于

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

# 添加笔记
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form) # 实例化ArticleForm表单类
    if request.method == 'POST':
        # 如果用户提交表单，并且表单验证通过
        # 获取表单字段内容
        t={}         
        t["id"]=len(open('sample.csv', 'r').readlines())+1
        t["title"] = form.title.data
        t["author"] =session['username']
        t["update_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        t["content"] = form.content.data
        
        author = session['username']
        
        #1,Python运维开发,xiaoli,2022-12-4 12:20:00,Python运维开发是一个学习python语言的课程，非常有意思！
    
        with open('sample.csv',"a") as fw:
            fw.write(str(t["id"])+","+t["title"]+","+ \
                     t["author"]+","+t["update_date"]+","+ \
                     t["content"]+"\n")
        flash('创建成功', 'success') # 闪存信息
        return redirect(url_for('dashboard'))               # 跳转到控制台
                           
    return render_template('add_article.html', form=form)   # 渲染模板

    
# 编辑笔记
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):   

    article={}    
    with open('sample.csv',"r") as fr:
        for line in fr:    #文件对象可以直接迭代
            #print(line)
            r = line.split(",")
            if r[0] !=id:
                continue
            else:
                #9,ansible学习,zhangsan,2022-12-30 16:52:59,ansible是一个有用技术
                article={}
                article['id']= r[0];article['title']=r[1];article['author']=r[2];article['update_date']=r[3];
                article['content']=r[4]             
                break;
    
    # 检测笔记不存在的情况
    if not article:
        flash('ID错误', 'danger') # 闪存信息
        return redirect(url_for('dashboard'))
    
    # 获取表单
    form = ArticleForm(request.form)
    if request.method == 'GET':
        # 从数据库中获取表单字段的值
        form.title.data = article['title']
        form.content.data = article['content']
        return render_template('edit_article.html', info=form)   # 渲染模板
    
    elif request.method == 'POST':# 如果用户提交表单，并且表单验证通过
        # 获取表单字段内容
        #9,ansible学习,zhangsan,2022-12-30 16:52:59,ansible是一个有用技术
        with open('sample.csv',"r") as fr:
            line_list = fr.readlines()
            for i in range(0,len(line_list)):    #文件对象可以直接迭代
                #print(line)
                r = line_list[i].split(",")
                if r[0] !=id:
                    continue
                else:
                    r[1] = form.title.data
                    r[2] = session['username']
                    r[3] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    r[4] = form.content.data
                    line_list[i] = ",".join(r)
                    break;
        with open('sample.csv',"w") as fw:
            fw.writelines(line_list)
            #fw.write("123")
            
        
        flash('更新成功', 'success') # 闪存信息
        return redirect(url_for('dashboard')) # 跳转到控制台

# 删除笔记
@app.route('/delete_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def delete_article(id):
    # 获取表单字段内容
    #9,ansible学习,zhangsan,2022-12-30 16:52:59,ansible是一个有用技术
    
    with open('sample.csv',"r") as fr:
            line_list = fr.readlines()
            for i in range(0,len(line_list)):    #文件对象可以直接迭代
                #print(line)
                r = line_list[i].split(",") 
                if r[0] !=id:
                    continue
                else:
                    line_list.pop(i)#删除第i行内容  
                    break;
    with open('sample.csv',"w") as fw:
            fw.writelines(line_list)
            #fw.write("123")
    
    flash('删除成功', 'success') # 闪存信息
    return redirect(url_for('dashboard')) # 跳转到控制台



if __name__ == '__main__':#程序入口
    #app.run()#让应用运行在本地服务器上。
    app.secret_key='secret123'
    app.run( host='0.0.0.0',port="5009",debug="True") #允许任意网址访问本站
