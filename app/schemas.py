from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LessonBase(BaseModel):
    title: str
    slug: str
    body_md: str
    order: int = 0


class LessonCreate(LessonBase):
    pass


class LessonRead(LessonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LessonList(BaseModel):
    items: List[LessonRead]
    total: int


class ExerciseBase(BaseModel):
    title: str
    description_md: str
    init_sql: str
    expected_sql: str
    order: int = 0


class ExerciseCreate(ExerciseBase):
    lesson_id: int


class ExerciseRead(ExerciseBase):
    id: int
    lesson_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ExerciseList(BaseModel):
    items: List[ExerciseRead]
    total: int


class RunRequest(BaseModel):
    sql: str = Field(..., description="SQL query to execute")


class RunResult(BaseModel):
    is_correct: bool
    result_json: str
    time_ms: int
    rows: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None