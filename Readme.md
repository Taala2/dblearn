# 📦 DB Learn

Сайт для изучения и практики по Базе Данных sql

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Taala2/dblearn.git
cd dblearn
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Заполнить базу данных контентом

```bash
python manage_content.py load-lessons 'content/lessons/*.md'
python manage_content.py load-exercises 'content/exercises/*.yaml'
```

### 3. Запуск

```bash
uvicorn app.main:app
```
