from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.core.database import create_db_and_tables
from app.routers import exercises, lessons, runner

app = FastAPI(
    title="DB-Learn API",
    description="Interactive database learning platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://192.168.1.210:8000", "http://192.168.1.210:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавляем роутеры API
app.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
app.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
app.include_router(runner.router, prefix="/exercises", tags=["runner"])

app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Основной маршрут для главной страницы
@app.get("/", tags=["frontend"])
async def serve_index():
    return FileResponse("frontend/index.html")

# Маршруты для конкретных HTML-страниц
@app.get("/lessons.html", tags=["frontend"])
async def serve_lessons_page():
    return FileResponse("frontend/lessons.html")

@app.get("/lesson.html", tags=["frontend"])
async def serve_lesson_page():
    return FileResponse("frontend/lesson.html")

@app.get("/exercises.html", tags=["frontend"])
async def serve_exercises_page():
    return FileResponse("frontend/exercises.html")

@app.get("/exercise.html", tags=["frontend"])
async def serve_exercise_page():
    return FileResponse("frontend/exercise.html")

# Обработчик для всех остальных статических файлов
@app.get("/{path:path}", tags=["frontend"], include_in_schema=False)
async def serve_static_files(path: str):
    file_path = f"frontend/{path}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    # Если файл не найден, возвращаем 404 или перенаправляем на главную
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)