from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.deps import get_db
from app.models import Lesson
from app.schemas import LessonList, LessonRead

router = APIRouter()


@router.get("/", response_model=LessonList)
def get_lessons(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get all lessons with pagination."""
    query = select(Lesson).order_by(Lesson.order).offset(skip).limit(limit)
    lessons = db.exec(query).all()
    total = db.exec(select(Lesson)).all()

    return LessonList(items=lessons, total=len(total))


@router.get("/{lesson_id}", response_model=LessonRead)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Get a specific lesson by ID."""
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/by-slug/{slug}", response_model=LessonRead)
def get_lesson_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get a specific lesson by slug."""
    query = select(Lesson).where(Lesson.slug == slug)
    lesson = db.exec(query).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson