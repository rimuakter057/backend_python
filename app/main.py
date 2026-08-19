import psycopg2
import time

from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db, Base


app = FastAPI()

Base.metadata.create_all(bind=engine)

class Intro(BaseModel):
    name: str
    profession: str
    class_: str
    website: str
    duration: int


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="test_first",
            user="postgres",
            password="1234",
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()

        print("Database connection was successful")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/")
def read_data():
    cursor.execute("SELECT * FROM test_table")
    return cursor.fetchall()




@app.post("/add-intro")
def add_intro(data:Intro):
    cursor.execute("INSERT INTO test_table (name, profession, class, website, duration) VALUES (%s,%s,%s,%s,%s) RETURNING *", (data.name, data.profession, data.class_, data.website, data.duration))
    new_row = cursor.fetchone()
    conn.commit()
    return new_row





@app.get("get-intro/{id}")
def get_intro(id:int):
        cursor.execute("SELECT * FROM test_table WHERE id = %s",(id))
        test_table = cursor.fetchone()
        if not test_table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,

                             detail="Intro id:{id} not found")
        return {"intro_details":test_table}

@app.get("delete-intro/{id}")
def delete_intro(id:int):
           cursor.execute("DELETE FROM test_table WHERE id = %s RETURNING *",(id))
           new_row = cursor.fetchone()       
           conn.commit()
           if not new_row:       
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail="Intro id:{id} not found")

@app.get("/coursealchemy")
def course(db: Session = Depends(get_db)):
    return {"status": "sqlalchemy ORM working"}

@app.put("/update-intro/{id}")
def update_intro(id: int, data: Intro):
    cursor.execute(
        "UPDATE test_table SET name = %s, profession = %s, class = %s, website = %s, duration = %s WHERE id = %s RETURNING *",
        (data.name, data.profession, data.class_, data.website, data.duration, id)
    )
    updated_row = cursor.fetchone()
    conn.commit()
    if not updated_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intro id: {id} not found"
        )
    return {"updated_intro": updated_row}