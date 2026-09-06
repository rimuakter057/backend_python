from fastapi import APIRouter, HTTPException, status

from .. import schemas
from ..legacy_db import conn, cursor

router = APIRouter(tags=["Intro"])


@router.get("/")
def read_data():
    cursor.execute("SELECT * FROM test_table")
    return cursor.fetchall()


@router.post("/add-intro")
def add_intro(data: schemas.Intro):
    cursor.execute(
        "INSERT INTO test_table (name, profession, class, website, duration) VALUES (%s,%s,%s,%s,%s) RETURNING *",
        (data.name, data.profession, data.class_, data.website, data.duration)
    )
    new_row = cursor.fetchone()
    conn.commit()
    return new_row


@router.get("get-intro/{id}")
def get_intro(id: int):
    cursor.execute("SELECT * FROM test_table WHERE id = %s", (id))
    test_table = cursor.fetchone()
    if not test_table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Intro id:{id} not found")
    return {"intro_details": test_table}


@router.get("delete-intro/{id}")
def delete_intro(id: int):
    cursor.execute("DELETE FROM test_table WHERE id = %s RETURNING *", (id))
    new_row = cursor.fetchone()
    conn.commit()
    if not new_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Intro id:{id} not found")


@router.put("/update-intro/{id}")
def update_intro(id: int, data: schemas.Intro):
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
