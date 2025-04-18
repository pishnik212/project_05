# Информаицонная система для прогнозирования результатов приемной кампании в ВУЗы

Веб-приложение предназначено для сотрудников приемной комиссии. 

Позволяет автоматизировать процесс определения минимального проходного балла для направления обучения.

## Структура проекта

project_05
  
      ├── frontend/ # Интерфейс пользователя (React) 
      
      ├── backend/ # Серверная логика (Python) 
      
      ├── .github/ # Настройки GitHub Actions 
      
      ├── .gitignore 
      
      └── README.md

## 🚀 Запуск проекта

### Скачивание проекта

```
git clone https://github.com/djulygpro/project_05.git

cd project_05

docker-compose up --build
```

### Backend

```bash
cd backend

# Установка зависимостей
npm install  # или pip install -r requirements.txt

# Запуск сервера
npm start
```

### Frontend

```
cd frontend
npm install
npm start
```

