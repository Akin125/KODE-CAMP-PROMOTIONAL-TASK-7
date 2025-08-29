from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..models import Student, StudentCreate, StudentUpdate, StudentRead, Grade, GradeCreate, GradeRead
from ..database import get_session
from ..auth import get_current_user

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=StudentRead)
def create_student(
    student: StudentCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Create a new student (requires authentication)"""
    db_student = Student(**student.dict())
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student


@router.get("/", response_model=List[StudentRead])
def read_students(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all students"""
    students = session.exec(select(Student).offset(skip).limit(limit)).all()
    return students


@router.get("/{student_id}", response_model=StudentRead)
def read_student(
    student_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific student by ID"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentRead)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Update a student (requires authentication)"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_data = student_update.dict(exclude_unset=True)
    for field, value in student_data.items():
        setattr(student, field, value)

    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Delete a student (requires authentication)"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    session.delete(student)
    session.commit()
    return {"message": "Student deleted successfully"}


@router.post("/{student_id}/grades", response_model=GradeRead)
def add_grade(
    student_id: int,
    grade: GradeCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Add a grade to a student (requires authentication)"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    grade_data = grade.dict()
    grade_data["student_id"] = student_id
    db_grade = Grade(**grade_data)
    session.add(db_grade)
    session.commit()
    session.refresh(db_grade)
    return db_grade


@router.get("/{student_id}/grades", response_model=List[GradeRead])
def get_student_grades(
    student_id: int,
    session: Session = Depends(get_session)
):
    """Get all grades for a specific student"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    grades = session.exec(select(Grade).where(Grade.student_id == student_id)).all()
    return grades
