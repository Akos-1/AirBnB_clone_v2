#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv


class DBStorage:
    """This class connects to the MySQL database and manages the ORM"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        session = self.__session
        classes = ['User', 'State', 'City', 'Amenity', 'Place', 'Review']
        if cls is not None:
            classes = [cls]
        objects = {}
        for clas in classes:
            query = session.query(eval(clas))
            for instance in query.all():
                key = '{}.{}'.format(clas, instance.id)
                objects[key] = instance
        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and create the current database session"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Call remove() method on the private
        session attribute (self.__session)"""
        self.__session.close()
