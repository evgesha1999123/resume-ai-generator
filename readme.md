<div align="center">

# 🚀 AI Resume Builder from Git

**Автоматическая генерация IT-резюме на основе анализа Git-репозиториев**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)](https://www.rabbitmq.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![MinIO](https://img.shields.io/badge/MinIO-C72A48?style=for-the-badge&logo=minio&logoColor=white)](https://min.io/)

</div>

---

## 📖 О проекте

Сервис анализирует **публичные Git-репозитории** (GitHub, GitLab, GitFlic) и на основе кода, структуры проекта и README автоматически генерирует персонализированное резюме разработчика в формате `.pdf` или `.docx` с помощью **OpenAI**.

> 🎯 **Цель** — превратить «цифровой след» разработчика в готовый, профессиональный документ за считанные минуты.

---

## 🧠 Архитектура и поток данных

Система построена на **асинхронной обработке задач** для работы с долгими операциями (клон репозитория, AI-генерация, постобработка).

```mermaid
    A[📡 FastAPI>GET /resume] --> B[(🗄️ PostgreSQL)];
    B --> C[🐇 RabbitMQListener];
    C --> D[🔍 Git Analyzer];
    D --> E[🌐 Client API Git];
    D --> F[📦 Git Dependense Parser];
    F --> G[(📋 ProjectInformationSchema)];
    G --> H[🤖 OpenAI API];
    H --> I[✅ ResumeValidator];
    I --> J[📄 ResumeBuilder];
    J --> K[💾 MinioRepo];
    K --> L[🔌 WebSocket/SSE];
```
⚙️ Этапы работы
```mermaid
1️⃣ Прием задачи
FastAPI получает user_id и git_url.

Данные сохраняются в БД вместе с уникальным task_id.

Задача публикуется в RabbitMQ для асинхронной обработки.
```

```mermaid
2️⃣ Анализ репозитория
Git analyzer выполняет глубокий анализ:

Что анализируется	Источник	Извлекаемая информация
📄 README.md	/readme	Цели проекта, примеры использования, архитектура
📝 Description + Topics	/repo	Краткое описание (если нет README)
🗂️ Структура папок	/git/trees	MVC, src/, notebooks/, cli/ и т.д.
🌍 Языки	/languages	Стек технологий (Python, Go, JS и др.)
📦 Зависимости	package.json, requirements.txt, go.mod, pom.xml	Библиотеки и фреймворки
3️⃣ Формирование модели (ProjectInformationSchema)
Все данные структурируются в единую схему:

python
class ProjectInformationSchema:
    general: GeneralInfoSchema      # readme, description, topics
    stack_info: StackInfo           # languages, dependencies
    structure: list[str]            # структура папок
```

```mermaid
4️⃣ AI-генерация
Модель преобразуется в оптимизированный промпт.

Отправка в OpenAI API (модель gpt-4 или выше).

На выходе — Markdown с черновиком резюме.
```

```mermaid
5️⃣ Постобработка
Компонент	Задача
ResumeValidator	Проверка на галлюцинации, соответствие стеку технологий
ResumePostProcessor	Приведение к формату: «Опыт», «Навыки», «Проекты»
6️⃣ Сборка и доставка
ResumeBuilder генерирует финальный файл (.pdf / .docx).

MinioRepo сохраняет файл в S3-совместимое хранилище (папка user_id).

WebSocket / SSE отправляет пользователю ссылку на скачивание.
```
