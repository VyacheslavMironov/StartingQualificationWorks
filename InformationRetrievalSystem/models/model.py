from sqlalchemy import (
    create_engine, 
    MetaData, 
    Table,
    Column,
    String, 
    Integer, 
    Text,
    JSON,
    ForeignKey
)


# Подключение к серверу PostgreSQL на localhost с помощью psycopg2 DBAPI 
engine = create_engine("postgresql+psycopg2://admin_irs:MyNewPAssword@localhost/irs", echo=True)
conn = engine.connect()
metadata = MetaData()


organizations =     Table('organizations', metadata, 
                        Column('id', Integer(), autoincrement=True, primary_key=True),
                        Column('name', String(45), unique=True)
                    )

user =              Table('user', metadata, 
                        Column('user_id', Integer(), autoincrement=True, primary_key=True),
                        Column('name', String(30)),
                        Column('surname', String(30)),
                        Column('email', String(255), unique=True),
                        Column('password', String(50), nullable=False),
                        Column('organization_id', ForeignKey('organizations.id'))
                    )

type_numbers =      Table('type_numbers', metadata, 
                        Column('id', Integer(), autoincrement=True, primary_key=True),
                        Column('name', String(255)),
                        Column('number_hotel', Integer(), nullable=False),
                        Column('images', JSON(), nullable=True)
                        
                    )

hotel =             Table('hotel', metadata, 
                        Column('hotel_id', Integer(), autoincrement=True, primary_key=True),
                        Column('hotel_name', String(15), unique=True),
                        Column('title', String(255)),
                        Column('images', JSON(), nullable=True),
                        Column('details', Text(), nullable=False),
                        Column('star', Integer()),
                        Column('estimates', Integer()),
                        Column('type_number', ForeignKey('type_numbers.id'))
                        
                    )

application =       Table('applications', metadata, 
                        Column('id', Integer(), autoincrement=True, primary_key=True),
                        Column('user', ForeignKey('user.user_id')),
                        Column('hotel', ForeignKey('hotel.hotel_id')),
                        Column('count_person', Integer(), default=1),
                        Column('count_day', Integer(), default=1),
                        Column('type_number', String(30), unique=True)
                        
                    )
