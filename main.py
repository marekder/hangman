from fastapi import Request, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import sqlalchemy as db
import random

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = db.create_engine('sqlite:///hangman_.db', connect_args={"check_same_thread": False})
connection = engine.connect()
metadata = db.MetaData()

categories = db.Table('Categories', metadata,
                db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
                db.Column('name', db.String(60), nullable=False),
                db.Column('description', db.String(100), nullable=False),
                )

words = db.Table('Words', metadata,
                 db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
                 db.Column('category_id', db.Integer(), nullable=False),
                 db.Column('word', db.String(60), nullable=False),
                 )


metadata.create_all(engine)

print("Klucze tabeli Categories:", categories.columns.keys(), '\n')
print("Klucze tabeli Words:", words.columns.keys(), '\n')

# dodaję dane do tabeli Categories

# query = db.insert(categories).values(id=1, name='Przyroda', description="Kategoria przyroda")
# connection.execute(query)
# select_users_query = db.select([categories])
# select_results = connection.execute(select_users_query)
# print("\n", select_results.fetchall())

# Pobranie wszystkich kategorii


@app.get("/categories")
def get_categories():
    try:
        query = db.select([categories])
        result = (connection.execute(query)).fetchall()
        if not result: # if result = []
            return {"status": "failed", "info": "no records"}
        return result
    except Exception as error:
        print(error)
        return {"status": "failed"}

# Pobranie jednej kategorii


@app.get("/categories/{id}")
def get_category_by_id(id: int):
    try:
        query = db.select([categories]).where(categories.columns.id == id)
        result = (connection.execute(query)).fetchone()
        print(type(result))
        if not result: # if result is None
            return {"status": "failed", "info": "no category with this id"}
        return result
    except Exception as error:
        print(error)
        return {"status": "failed"}


















# @app.get("/words/random")
# def get_words_random():
#     try:
#         query = db.select([words])
#         result = (connection.execute(query)).fetchall()
#         if not result:
#             return {"status": "failed", "info": "no records"}
#         return result
#     except Exception as error:
#         print(error)
#         return {"status": "failed"}
#
# @app.get("/categories/{id}/word/")
# def get_specific_word(categories_id: int):
#     query = db.select([categories, words])
#     query = query.select_from(categories.join(words, categories.columns.id == words.columns.category_id))
#     result = (connection.execute(query)).fetchall()
#     print(result)
