import argparse
import glob
import json
import os
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import frontmatter
from slugify import slugify
from sqlmodel import Session, select

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine
from app.models import Exercise, Lesson


def extract_lesson_metadata(content: str) -> Dict:
    """Extract metadata from lesson Markdown file with frontmatter."""
    post = frontmatter.loads(content)
    metadata = post.metadata
    
    # Set defaults for required fields
    if "title" not in metadata:
        # Try to extract title from first heading
        title_match = re.search(r'^# (.+)', post.content, re.MULTILINE)
        metadata["title"] = title_match.group(1) if title_match else "Untitled Lesson"
    
    if "slug" not in metadata:
        metadata["slug"] = slugify(metadata["title"])
    
    if "order" not in metadata:
        metadata["order"] = 0
    
    return {
        "title": metadata["title"],
        "slug": metadata["slug"],
        "order": metadata["order"],
        "body_md": post.content,
    }


def extract_exercise_metadata(content: str) -> Dict:
    """Extract exercise data from YAML file."""
    data = yaml.safe_load(content)
    
    # Ensure required fields~
    required_fields = ["title", "description_md", "init_sql", "expected_sql"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Exercise YAML missing required field: {field}")
    
    # Set defaults
    if "order" not in data:
        data["order"] = 0
    
    # Ensure lesson_id is present or can be inferred
    if "lesson_id" not in data and "lesson_slug" not in data:
        raise ValueError("Exercise must have either lesson_id or lesson_slug")
    
    return data


def load_lesson(session: Session, file_path: str) -> Lesson:
    """Load a lesson from a Markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    lesson_data = extract_lesson_metadata(content)
    print(f"Loading lesson: {lesson_data['title']}")
    
    # Check if lesson exists by slug
    query = select(Lesson).where(Lesson.slug == lesson_data["slug"])
    existing_lesson = session.exec(query).first()
    
    if existing_lesson:
        # Update existing lesson
        for key, value in lesson_data.items():
            setattr(existing_lesson, key, value)
        existing_lesson.updated_at = datetime.utcnow()
        lesson = existing_lesson
        print(f"  Updated existing lesson: {lesson.id}")
    else:
        # Create new lesson
        lesson = Lesson(**lesson_data)
        session.add(lesson)
        session.flush()  # Flush to get the ID
        print(f"  Created new lesson: {lesson.id}")
    
    return lesson


def load_exercise(session: Session, file_path: str) -> Exercise:
    """Load an exercise from a YAML file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    exercise_data = extract_exercise_metadata(content)
    print(f"Loading exercise: {exercise_data['title']}")
    
    # Resolve lesson_id if lesson_slug is provided
    if "lesson_id" not in exercise_data and "lesson_slug" in exercise_data:
        query = select(Lesson).where(Lesson.slug == exercise_data["lesson_slug"])
        lesson = session.exec(query).first()
        if not lesson:
            raise ValueError(f"No lesson found with slug: {exercise_data['lesson_slug']}")
        exercise_data["lesson_id"] = lesson.id
        del exercise_data["lesson_slug"]
    
    # Check if exercise exists
    if "id" in exercise_data:
        existing_exercise = session.get(Exercise, exercise_data["id"])
        if existing_exercise:
            # Update existing exercise
            for key, value in exercise_data.items():
                setattr(existing_exercise, key, value)
            exercise = existing_exercise
            print(f"  Updated existing exercise: {exercise.id}")
            return exercise
    
    # Create new exercise
    exercise = Exercise(**exercise_data)
    session.add(exercise)
    session.flush()  # Flush to get the ID
    print(f"  Created new exercise: {exercise.id}")
    return exercise


def load_lessons(session: Session, pattern: str) -> List[Lesson]:
    """Load multiple lessons from Markdown files."""
    lessons = []
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} lesson files to process")
    
    for file_path in files:
        try:
            lesson = load_lesson(session, file_path)
            lessons.append(lesson)
        except Exception as e:
            print(f"Error loading lesson from {file_path}: {e}")
    
    return lessons


def load_exercises(session: Session, pattern: str) -> List[Exercise]:
    """
    Загрузка упражнений из YAML-файлов. Каждый файл может содержать либо один
    словарь с описанием упражнения, либо список таких словарей.
    """
    exercises: List[Exercise] = []
    files = files = glob.glob(pattern)
    print(f"Найдено {len(files)} файлов упражнений для загрузки")

    for file_path in files:
        try:
            # Считываем и разбираем YAML
            with open(file_path, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f)
            # Если это не список — оборачиваем в список
            specs = raw if isinstance(raw, list) else [raw]

            for spec in specs:
                # Проверяем обязательные поля
                for field in ("title", "description_md", "init_sql", "expected_sql"):
                    if field not in spec:
                        raise ValueError(f"В файле {file_path} нет поля «{field}»")

                # По умолчанию order = 0
                spec.setdefault("order", 0)

                # Должен быть lesson_id или lesson_slug
                if "lesson_id" not in spec and "lesson_slug" not in spec:
                    raise ValueError(f"В файле {file_path} нет ни lesson_id, ни lesson_slug")

                # Если указан lesson_slug — находим lesson_id
                if "lesson_slug" in spec and "lesson_id" not in spec:
                    stmt = select(Lesson).where(Lesson.slug == spec["lesson_slug"])
                    lesson = session.exec(stmt).first()
                    if not lesson:
                        raise ValueError(f"Урок с slug={spec['lesson_slug']} не найден")
                    spec["lesson_id"] = lesson.id
                    del spec["lesson_slug"]

                # Создаём и сохраняем новое упражнение
                exercise = Exercise(**spec)
                session.add(exercise)
                session.flush()  # чтобы получить exercise.id сразу
                print(f"  Создано упражнение: {exercise.id} — {exercise.title}")
                exercises.append(exercise)

        except Exception as e:
            print(f"Ошибка при загрузке из {file_path}: {e}")

    return exercises


def main():
    parser = argparse.ArgumentParser(description="DB-Learn content management tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Load lessons command
    lessons_parser = subparsers.add_parser("load-lessons", help="Load lessons from Markdown files")
    lessons_parser.add_argument("pattern", help="File glob pattern for lesson files")
    
    # Load exercises command
    exercises_parser = subparsers.add_parser("load-exercises", help="Load exercises from YAML files")
    exercises_parser.add_argument("pattern", help="File glob pattern for exercise files")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    with Session(engine) as session:
        try:
            if args.command == "load-lessons":
                lessons = load_lessons(session, args.pattern)
                session.commit()
                print(f"Successfully loaded {len(lessons)} lessons")
            
            elif args.command == "load-exercises":
                exercises = load_exercises(session, args.pattern)
                session.commit()
                print(f"Successfully loaded {len(exercises)} exercises")
            
            else:
                parser.print_help()
                return 1
                
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())