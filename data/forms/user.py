from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField, DateField, FieldList
from wtforms.validators import DataRequired

import sqlalchemy


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    email = EmailField('Почта/логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobForm(FlaskForm):
    team_leader = IntegerField('Id руководителя', validators=[DataRequired()])
    job = StringField('Описание', validators=[DataRequired()])

    work_size = IntegerField('Длительность', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])

    is_finished = BooleanField('Закончена ли работа')
    submit = SubmitField('Добавить')