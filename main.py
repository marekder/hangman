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

engine = db.create_engine('sqlite:///wisielec.db', connect_args={"check_same_thread": False})
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

@app.get("/categories")
def get_categories():
    try:
        query = db.select([categories])
        result = (connection.execute(query)).fetchall()
        if not result:
            return {"status": "failed", "info": "no records"}
        return result
    except Exception as error:
        print(error)
        return {"status": "failed"}

