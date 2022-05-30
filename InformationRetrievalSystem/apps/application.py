from abc import ABC, abstractmethod
from sqlalchemy import insert
from models.model import application, conn


class AbstractApplication(ABC):
    @abstractmethod
    def add(self, user_id, hotel, count_person, count_day, type_number):
        pass


class Application(AbstractApplication):
    def add(self, user_id, hotel, count_person, count_day, type_number):
        if user_id and hotel and count_person and count_day and type_number:
            query = insert(application).values(
                user=user_id, 
                hotel=hotel, 
                count_person=count_person, 
                count_day=count_day, 
                type_number=type_number[:29]
            )
            conn.execute(query)
            return True
