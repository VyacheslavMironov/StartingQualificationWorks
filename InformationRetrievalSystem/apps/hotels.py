import imp
import sys
from abc import ABC, abstractmethod
from inspect import getargspec
sys.path.append('..')

from flask import session
from sqlalchemy import select

from models.model import conn, hotel, application


class UserHistory(object):
    def __init__(self):
        self.hotel_lists = conn.execute(select(hotel)).fetchall() 
        self.application_lists = conn.execute(select(application)).fetchall()
        self.app = list()
        self.data = list()


    def info(self):
        for app in self.application_lists:
            if app[1] == session['user']['id']:
                self.app.append(app[2])
        
        x = 0
        while len(self.hotel_lists) > x:
            try:
                if self.application_lists[x][2] == self.hotel_lists[x][0]:
                    self.data.append(self.hotel_lists[x])
            except IndexError:
                pass
            x+=1
        return self.data


class Filter:
    def search_star(self, data):
        query = f"SELECT * FROM hotel WHERE star = {int(data)};"
        return conn.execute(query).fetchall()

    def search_city(self, data):
        query = f"SELECT * FROM hotel WHERE title = '{str(data)}';"
        return conn.execute(query).fetchall()

    def search_all(self, data:list):
        query = f"SELECT * FROM hotel WHERE title = '{str(data[0])}' AND star = {int(data[1])};"
        return conn.execute(query).fetchall()


class AbstractObserver(ABC):
    @abstractmethod
    def filter(self, city, star):
        pass


class HotelInfo:

    def filter(self, city=None, star=None):
        if city == None and star:
            obj = Filter().search_star(star)

        elif city and star == None:
            obj = Filter().search_city(city)

        elif city and star:
            obj = Filter().search_all([city, star])
            
        return obj

    
    def hotel(self):
        query = select(hotel)
        return conn.execute(query).fetchall()
