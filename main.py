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

engine = db.create_engine('sqlite:///hangman.db', connect_args={"check_same_thread": False})
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

# Getting all categories


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

# Getting all words

@app.get("/words")
def get_words():
    try:
        query = db.select([words])
        result = (connection.execute(query)).fetchall()
        if not result: # if result = []
            return {"status": "failed", "info": "no records"}
        return result
    except Exception as error:
        print(error)
        return {"status": "failed"}



# Getting particular category


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

# Adding categories


@app.post("/categories")
async def add_category(request: Request):
    try:
        added_category = json.loads(await request.body())
        added_name = added_category["name"]
        added_description = added_category["description"]
        query = db.insert(categories).values(name=added_name, description=added_description)
        connection.execute(query)
        print(added_category["name"], added_category["description"])
        return {"status": "done"}
    except Exception as error:
        print(error)
        return {"status": "failed"}

# Adding words

@app.post("/words")
async def add_word(request: Request):
    try:
        added_word = json.loads(await request.body())
        added_category_id = added_word["category_id"]
        query = db.select([categories]).where(categories.columns.id == added_category_id)
        result = connection.execute(query).fetchall()
        if not result:
            return {"status": "failed", "info": "category does not exist"}
        added_word = added_word["word"]
        query = db.insert(words).values(category_id=added_category_id, word=added_word)
        connection.execute(query)
        print(added_word)
        return {"status": "done"}
    except Exception as error:
        print(error)
        return {"status": "failed"}

# Getting random word


@app.get("/words/random")
def get_word_random():
    try:
        query = db.select([words])
        result = (connection.execute(query)).fetchall()
        random_index = random.randrange(0, len(result))
        random_word = dict(result[random_index])
        query = db.select([categories]).where(categories.columns.id == random_word["category_id"])
        result = (connection.execute(query)).fetchone()
        random_word["Category"] = {"name": result["name"], "description": result["description"]}
        return random_word
    except Exception as error:
        print(error)
        return {"status": "failed"}











#
# @app.get("/categories/{id}/word/")
# def get_specific_word(categories_id: int):
#     query = db.select([categories, words])
#     query = query.select_from(categories.join(words, categories.columns.id == words.columns.category_id))
#     result = (connection.execute(query)).fetchall()
#     print(result)
