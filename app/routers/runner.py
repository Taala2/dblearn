import time
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.deps import get_db
from app.models import Exercise, Submission
from app.schemas import RunRequest, RunResult
from app.services.grader import evaluate_sql

router = APIRouter()


@router.post("/{exercise_id}/run", response_model=RunResult)
async def run_sql(
    exercise_id: int,
    payload: RunRequest,
    db: Session = Depends(get_db),
):
    """
    Run and evaluate a SQL query for a specific exercise.
    
    This endpoint executes the submitted SQL query in a sandbox environment,
    compares the result with the expected output, and returns the evaluation result.
    """
    # Get the exercise
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Track execution time
    start_time = time.time()
    
    # Evaluate the submitted SQL
    result = evaluate_sql(exercise.init_sql, exercise.expected_sql, payload.sql)
    
    # Calculate execution time
    execution_time_ms = int((time.time() - start_time) * 1000)
    result.time_ms = execution_time_ms
    
    # Save submission to database
    submission = Submission(
        exercise_id=exercise_id,
        sql_submitted=payload.sql,
        is_correct=result.is_correct,
        result_json=result.result_json,
        time_ms=execution_time_ms,
    )
    db.add(submission)
    db.commit()
    
    return result