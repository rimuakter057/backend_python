from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Courses"])


@router.get("/all-courses")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return {"courses": courses}


@router.post("/courses")
def create_course(course: schemas.Course, db: Session = Depends(get_db)):
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


@router.get("/get-course/{id}")
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course id: {id} not found"
        )
    return {"course_details": course}


@router.delete("/delete-course/{id}")
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


@router.get("/coursealchemy")
def course_status(db: Session = Depends(get_db)):
    return {"status": "sqlalchemy ORM working"}
