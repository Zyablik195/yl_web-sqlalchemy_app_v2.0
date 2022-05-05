from flask import Flask
from data import db_session
from data.users import User
from flask import url_for, request, render_template, redirect, abort
from data.jobs import Jobs
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.forms.user import RegisterForm, LoginForm, JobForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_sess = 0
login_manager = LoginManager()
login_manager.init_app(app)

'''
@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id > 0).all()
    for i in jobs:
        if i.is_finished:
            i.is_finished1 = 'Is finished'
        else:
            i.is_finished1 = 'Is not finished'
        user = db_sess.query(User).filter(User.id == i.team_leader).first()
        i.team_leader1 = user.name + user.surname
    return render_template("register.html", jobs=jobs)
'''

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id > 0).all()
    for i in jobs:
        if i.is_finished:
            i.is_finished1 = 'Is finished'
        else:
            i.is_finished1 = 'Is not finished'
        user = db_sess.query(User).filter(User.id == i.team_leader).first()
        i.team_leader1 = user.name + ' ' + user.surname
    return render_template("index.html", jobs=jobs)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.creater == current_user.id
                                          ).first()
        if jobs:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.creater == current_user.id
                                          ).first()
        if jobs:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id).filter(
        (Jobs.creater == current_user.id) | (current_user.id == 1)
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/addjob', methods=['GET', 'POST'])
def add():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(
            team_leader=form.team_leader.data,
            job = form.job.data,
            work_size = form.work_size.data,
            collaborators = form.collaborators.data,
            is_finished = form.is_finished.data,
            creater = current_user.id
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Авторизация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname = form.surname.data,
            age = form.age.data,
            position = form.position.data,
            speciality = form.speciality.data,
            address = form.address.data,
            email = form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

def main():
    global db_sess
    # name = input()
    db_session.global_init("db/blogs.db")
    # db_session.global_init(name)
    db_sess = db_session.create_session()
    app.run(host='127.0.0.1', port=5000)

    """
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.hashed_password = "cap"
    db_sess.add(user)

    user = User()
    user.surname = "Weir"
    user.name = "Andy"
    user.age = 27
    user.position = "support1"
    user.speciality = "geologist"
    user.address = "module_1"
    user.email = "22222@mars.org"
    user.hashed_password = "cap2"
    db_sess.add(user)

    user = User()
    user.surname = "Watny"
    user.name = "Mark"
    user.age = 26
    user.position = "support2"
    user.speciality = "biologist"
    user.address = "module_2"
    user.email = "33333@mars.org"
    user.hashed_password = "cap3"
    db_sess.add(user)

    job = Jobs()
    job.team_leader = 1
    job.job = 'Deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    db_sess.add(job)

    job = Jobs()
    job.team_leader = 2
    job.job = 'Exploration of mineral resources'
    job.work_size = 15
    job.collaborators = '4, 3'
    job.is_finished = False
    db_sess.add(job)

    job = Jobs()
    job.team_leader = 3
    job.job = 'Development of a management system'
    job.work_size = 25
    job.collaborators = '5'
    job.is_finished = False
    db_sess.add(job)
    '''
    for i in range(4):
        user = User()
        user.surname = dick['user.surname'][i]
        user.name = dick['user.name'][i]
        user.age = dick['user.age'][i]
        user.position = dick['user.position'][i]
        user.speciality = dick['user.speciality'][i]
        user.address = dick['user.address'][i]
        user.email = dick['user.email'][i]
        db_sess.add(user)
    '''
    db_sess.commit()
    """

if __name__ == '__main__':
    main()