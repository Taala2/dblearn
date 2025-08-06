from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.deps import get_db
from app.models import Exercise
from app.schemas import ExerciseList, ExerciseRead

router = APIRouter()


@router.get("/", response_model=ExerciseList)
def get_exercises(
    lesson_id: int = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get exercises with optional filtering by lesson ID."""
    query = select(Exercise).order_by(Exercise.order)

    if lesson_id is not None:
        query = query.where(Exercise.lesson_id == lesson_id)

    exercises = db.exec(query.offset(skip).limit(limit)).all()
    total_query = select(Exercise)

    if lesson_id is not None:
        total_query = total_query.where(Exercise.lesson_id == lesson_id)

    total = db.exec(total_query).all()

    return ExerciseList(items=exercises, total=len(total))


@router.get("/{exercise_id}", response_model=ExerciseRead)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Get a specific exercise by ID."""
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise