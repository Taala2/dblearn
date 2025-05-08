from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Lesson(SQLModel, table=True):
    """Database model for lessons."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    slug: str = Field(index=True, unique=True)
    body_md: str
    order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    exercises: List["Exercise"] = Relationship(back_populates="lesson")


class Exercise(SQLModel, table=True):
    """Database model for exercises."""
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: int = Field(foreign_key="lesson.id")
    title: str
    description_md: str
    init_sql: str  # SQL to initialize the exercise environment
    expected_sql: str  # Reference solution for grading
    order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    lesson: Lesson = Relationship(back_populates="exercises")
    submissions: List["Submission"] = Relationship(back_populates="exercise")


class Submission(SQLModel, table=True):
    """Database model for user submissions."""
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id")
    sql_submitted: str
    is_correct: Optional[bool] = None
    result_json: Optional[str] = None
    time_ms: Optional[int] = None
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    exercise: Exercise = Relationship(back_populates="submissions")