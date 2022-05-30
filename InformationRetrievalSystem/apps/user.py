import sys
sys.path.append('..')

from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError, DataError
from flask import session

from models.model import conn, organizations, user


class Validator(object):
    def login(self, email, password):
        if "@" in email and len(password) > 0:
            query = select(user)
            users = conn.execute(query).fetchall()
            for user_item in users:
                if user_item[3] == email:
                    return True
        else:
            return 'Логин или пароль введены не правильно'

    def register(self, name, surname, email, password1, password2):
        if len(name) >= 3 and len(surname) >= 2:
            if "@" in email:
                if password1 == password2:
                    return True

    def new_organization(self, name):
        query = select(organizations).where(organizations.name == name)
        if len(conn.execute(query).fetchall()) == 0:
            return True
        else:
            return False


def updatePassword(new_password, old_password):
    if new_password != old_password:
        print(session['user']['password'])
        print(old_password)
        if session['user']['password'] == old_password:
            query = update(user).values(password=new_password).where('email' == session['user']['email'])
            conn.execute(query)
            session['user']['password'] = new_password
            return {'message': 'Ваш пароль обновлён!', 'status': True}
        else:
            return {'message': 'Вы ввели неверный пароль.', 'status': False}
    else:
        return {'message': 'Пароли не должны совпадать!', 'status': False}


def organization_save(name):
    # Функция добавляет организацию в базу и возвращает id 
    # организации для дальнейшего взаимодействия с таблицей user
    try:
        query = insert(organizations).values(name=name)
        return conn.execute(query).inserted_primary_key[0]
    except IntegrityError:
        return 'Организация уже существует!'


class SignUp:
    def user(self, organization, name, surname, email, password1, password2):
        if Validator().register(name, surname, email, password1, password2) == True:
            query = insert(user).values(
                name=name,
                surname=surname,
                email=email,
                password=password1,
                organization_id=organization
            )
            try:
                return conn.execute(query)
            except DataError:
                return 'Такой пользователь уже существует!'


class SignIn:
    def user(self, email, password):
        query = select(user)
        users = conn.execute(query).fetchall()

        for user_item in users:
            if user_item[3] == email:
                query = organizations.select()
                organization_list = conn.execute(query).fetchall()

                for item in organization_list:
                    if item[0] == user_item[0]:
                        session['user'] = {
                            "id": user_item[0],
                            "name": user_item[1],
                            "surname": user_item[2],
                            "email": user_item[3],
                            "organization": item[1],
                            "password": user_item[4]
                        }
                        return True
                        
                        
class SignOut:
    def user(self):
        return session.clear()
    

class UserFasade:
    def __init__(self):
        self.sign_up = SignUp()
        self.sign_in = SignIn()
        self.sign_out = SignOut()
    
    def userSignUp(self, organization_name, name, surname, email, password1, password2):
        # Валидатор организации
        is_valid_organization = Validator().new_organization(name=organization_name)
        # Добавление организации
        organization_id = organization_save(name=organization_name)
        # Добавление нового пользователя в систему
        return self.sign_up.user(organization_id, name, surname, email, password1, password2)
                    
    def userSignIn(self, email, password):
        is_login = Validator().login(email=email, password=password)
        if is_login == True:
            return self.sign_in.user(email=email, password=password)
        
    def userSignOut(self):
        return self.sign_out.user()
