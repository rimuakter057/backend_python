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


    
class Course(BaseModel):
    name: str
    title: str
    instructor: str
    duration: int
    description: str

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

@app.get("/all-courses")
def get_courses(db: Session =Depends(get_db)):
     courses= db.query(models.Course).all()
     return {"courses": courses}





@app.post("/add-intro")
def add_intro(data:Intro):
    cursor.execute("INSERT INTO test_table (name, profession, class, website, duration) VALUES (%s,%s,%s,%s,%s) RETURNING *", (data.name, data.profession, data.class_, data.website, data.duration))
    new_row = cursor.fetchone()
    conn.commit()
    return new_row

@app.post("/courses")
def create_course(course:Course,db: Session =Depends(get_db)):
 new_course = models.Course(
    name=course.name,
    title=course.title,
    instructor=course.instructor,
    duration=course.duration,
    description=course.description
)
 db.add(new_course)
 db.commit()
 db.refresh(new_course)
 return {"Course": new_course}




@app.get("get-intro/{id}")
def get_intro(id:int):
        cursor.execute("SELECT * FROM test_table WHERE id = %s",(id))
        test_table = cursor.fetchone()
        if not test_table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,

                             detail="Intro id:{id} not found")
        return {"intro_details":test_table}





@app.get("/get-course/{id}")
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course id: {id} not found"
        )
    return {"course_details": course}
     


@app.get("delete-intro/{id}")
def delete_intro(id:int):
           cursor.execute("DELETE FROM test_table WHERE id = %s RETURNING *",(id))
           new_row = cursor.fetchone()       
           conn.commit()
           if not new_row:       
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail="Intro id:{id} not found")



@app.delete("/delete-course/{id}")
def delete_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course id: {id} not found"
        )
    db.delete(course)
    db.commit()
    return {"message": f"Course id: {id} deleted successfully"}
           

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