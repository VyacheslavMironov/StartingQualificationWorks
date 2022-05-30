# coding: utf-8
from configparser import ConfigParser
from datetime import datetime

from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_cors import CORS, cross_origin
from sqlalchemy import select

from apps.user import UserFasade, updatePassword
from apps.application import Application
from apps.hotels import HotelInfo, UserHistory
from models.model import *


app = Flask('__name__')
# Настройки конфигурации приложения
conf = ConfigParser()
conf.read(filenames='config.ini')
# Создание таблиц
metadata.create_all(engine)
# Настройки сессии
app.secret_key = "123" 
# Настройка заголовка для принятия запроса из вне
cors = CORS(app, resources={r"/*": {"origins": "*"}}, headers='Content-Type')
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        organization_name = request.form.get('organization_name')
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = UserFasade().userSignUp(
            organization_name=organization_name,
            name=name,
            surname=surname,
            email=email,
            password1=password1,
            password2=password2
        )

        if user:
            return redirect(url_for('signin'))
            
    return render_template(template_name_or_list="account/signup.html")


@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserFasade().userSignIn(email=email, password=password)
        if user == True:
            return redirect(url_for('profile'))
    return render_template(template_name_or_list="account/login.html")


@app.route('/signout/', methods=['GET'])
def signout():
    UserFasade().userSignOut()
    return redirect(url_for('index'))


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    return render_template(template_name_or_list="account/profile.html")


@app.route('/profile/update_password', methods=['POST'])
@cross_origin()
def update_password():
    if request.method == "POST":
        data = updatePassword(request.form.get("password_old"), request.form.get("password_new"))
        return (jsonify(data), 200)


@app.route('/', methods=['GET', 'POST'])
def index(city=None, star=None):
    city_lists = list()
    query = select(hotel)
    filter_city = conn.execute(query).fetchall()

    for i in filter_city:
        city_lists.append(i[2])

    if request.method == "POST":
        get_city = request.form.get('city')
        get_star = request.form.get('star')

        data = HotelInfo().filter(get_city,get_star)
    else:
        data = HotelInfo().hotel()

    return render_template(
        template_name_or_list="main/index.html", 
        data=data, city_lists=set(sorted(city_lists, reverse=True)))


@app.route('/show/<int:ids>', methods=['GET', 'POST'])
def show(ids):
    if  request.method == "POST":
        user_id = request.form.get('user_id')
        hotel = request.form.get('hotel')
        count_person = int(request.form.get('count')[2])

        check_in = request.form.get('check-in')
        departure = request.form.get('departure')

        old = datetime.strptime(departure, '%Y-%m-%d')
        new = datetime.strptime(check_in, '%Y-%m-%d')

        count_day = old - new
        count_day = int(str(count_day).split(' ')[0])
        type_number = request.form.get('type_number')
        

        return redirect(url_for(
                            'payment', 
                            user_id=user_id, 
                            hotel=hotel, 
                            count_person=count_person, 
                            count_day=count_day, 
                            type_number=type_number
                        ))

    query = f"SELECT * FROM hotel AS h INNER JOIN type_numbers AS tn ON h.type_number = {ids};"
    detail = conn.execute(query).fetchone()

    return render_template(template_name_or_list="main/show.html", detail=detail)


@app.route('/history/', methods=['GET'])
def history():
    data = UserHistory().info()
    return render_template(template_name_or_list="main/history.html", data=data)


@app.route('/payment?user_id=<int:user_id>&&hotel=<int:hotel>&&count_person=<int:count_person>&&count_day=<int:count_day>&&type_number=<string:type_number>', methods=['GET', 'POST'])
def payment(user_id, hotel, count_person, count_day, type_number):
    name = ''
    if user_id and hotel and count_person and count_day and type_number:
        query = f"SELECT hotel_name FROM hotel WHERE hotel_id={hotel};"
        name = conn.execute(query).fetchone()

        if request.method == "POST":
            data = Application()
            data.add(user_id, hotel, count_person, count_day, type_number)

    return render_template(template_name_or_list="main/payment.html", name=name[0])


app.run(debug = True, host = 'localhost', port = 8080)
