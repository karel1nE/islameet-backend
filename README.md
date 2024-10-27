# ISLAMEET

Современное приложение для знакомств с упором на мусульманскую аудиторию

# Стек технологий:
  Python FastAPI
  - Database: SQLAlchemy (В данный момент используется SQLite, но благодаря ORM нетрудно в будущем поменять на PostreSQL)
  - Auth: FastAPI Auth
  - Users: FastAPI Users

# ER-диаграмма
![ERD](images/erd.png)


# Роли пользователей
![Admin](images/admin.png)
![User](images/user.png)
![General](images/general.png)

# API Сервера:
app/main.py

# Текущее дерево проекта (Oct 27, 2024)
ISLAMEET
│
├── app
│   ├── main.py
│   ├── models
│   │   └── user.py
│   ├── schemas
│   │   └── user.py
│   ├── repositories
│   │   └── user_repository.py
│   ├── services
│   │   └── user_service.py
│   └── routers
│       └── user_router.py
├── db
│   └── database.py
└── requirements.txt