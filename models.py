# models.py
from peewee import *

db = PostgresqlDatabase('newspace', user='root', password='root',
                        host='localhost', port=5432)

class TodoList(Model):
    id = AutoField()
    task = CharField()

    class Meta:
        database = db

class TodoListCopy(Model):
    id = AutoField()
    task = CharField()

    class Meta:
        database = db