# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, redirect, url_for
from data import db_session
from data.clas import User
from data.clas import Reviews
from data.clas import RegisterForm
from data.clas import LoginForm
from data.clas import ReviewsForm
from data.clas import Tovar
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/base.sqlite")


@app.route("/")
@app.route('/index')
def index(): 
    session = db_session.create_session()
    component = session.query(Tovar) 
    return render_template("tovars.html", component=component)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)



@app.route('/component',  methods=['GET', 'POST'])
def component():
    if request.method == 'GET':
        session = db_session.create_session()
        proz = session.query(Tovar).filter(Tovar.types == 'Процессор')
        mat = session.query(Tovar).filter(Tovar.types == 'Материнская плата')
        video = session.query(Tovar).filter(Tovar.types == 'Видеокарта')
        pam = session.query(Tovar).filter(Tovar.types == 'Оперативная память')
        block = session.query(Tovar).filter(Tovar.types == 'Блок питания')
        korp = session.query(Tovar).filter(Tovar.types == 'Корпус')
        oxl = session.query(Tovar).filter(Tovar.types == 'Охлаждение')
        ssd = session.query(Tovar).filter(Tovar.types == 'SSD')
        disk = session.query(Tovar).filter(Tovar.types == 'Жесткий диск')
        return render_template('Content.html', proz=proz, mat=mat, video=video, 
                               pam=pam, block=block, korp=korp, oxl=oxl, ssd=ssd,
                               disk=disk)
    elif request.method == 'POST':
        session = db_session.create_session()
        component = Reviews()
        component.title = request.form['title']
        component.content = request.form['about']
        component.types = request.form['class']
        component.user_id = current_user.id
        session.add(component)
        session.commit()
        return redirect('/index')  
    

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        session = db_session.create_session()
        component = session.query(Reviews).filter(Reviews.user_id == current_user.id)    
        return render_template('profile.html', component=component)        
    elif request.method == 'POST':
        return redirect('/logout')



@app.route('/product')
def product():
    session = db_session.create_session()
    component = session.query(Tovar)
    return render_template('tovars.html', component=component)


@app.route('/product/<types>')
def product_typ(types):
    session = db_session.create_session()
    component = session.query(Tovar).filter(Tovar.types == types)
    return render_template('tovars.html', component=component)


@app.route('/product/<types>/<manufacturer>')
def product_typ_man(types, manufacturer):
    session = db_session.create_session()
    component = session.query(Tovar).filter(Tovar.types == types, 
                                            Tovar.manufacturer == manufacturer)
    return render_template('tovars.html', component=component)


@app.route('/tovar/<name>', methods=['GET', 'POST'])
def tovars(name):
    if request.method == 'GET':
        session = db_session.create_session()
        component = session.query(Tovar).filter(Tovar.name == name)
        return render_template('see.html', component=component)
    elif request.method == 'POST':
        session = db_session.create_session()
        component = Reviews()
        component.name = name
        component.plus = request.form['plus']
        component.minus = request.form['minus']
        component.content = request.form['about']
        component.estimation = request.form['class']
        component.user_id = current_user.id
        session.add(component)
        session.commit()
        return redirect('/index') 


def main():
    app.run(port=8070, host='127.0.0.1')


if __name__ == '__main__':
    main()