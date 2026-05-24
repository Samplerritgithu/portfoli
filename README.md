# Shiva Shankar Chanda — Portfolio

Premium, recruiter-focused portfolio built with **Django**, **Django REST Framework**, **PostgreSQL**, and modern HTML/CSS/JavaScript.

## Features

- Stunning hero with typing animation, particle background, glassmorphism UI
- About, Skills, Experience timeline, Projects, Architecture showcase
- Certifications, Education, Blog, Contact form
- Dark/Light theme, AI chatbot, Resume analyzer, PWA support
- REST APIs with JWT authentication and admin dashboard APIs
- Docker + NGINX + Gunicorn production setup
- GitHub Actions CI/CD pipeline

## Project Structure

```
├── config/                 # Django settings (base, dev, production)
├── apps/
│   ├── core/               # Site settings, stats, architecture diagrams
│   ├── portfolio/          # Skills, experience, projects, certs, education
│   ├── blog/               # Blog posts, categories, tags, comments
│   ├── contact/            # Contact messages, chatbot
│   └── api/                # DRF REST API endpoints
├── templates/              # Django templates
├── static/                 # CSS, JS, images
├── nginx/                  # NGINX config
├── docker-compose.yml
└── Dockerfile
```

## Quick Start (Local)

### 1. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Environment variables

```bash
copy .env.example .env
```

Edit `.env` with your database and email settings.

### 3. Start PostgreSQL

Use Docker:

```bash
docker compose up db -d
```

Or install PostgreSQL locally and create database `portfolio_db`.

### 4. Migrate & seed

```bash
python manage.py migrate
python manage.py seed_portfolio
python manage.py createsuperuser
```

Default seed admin: `admin` / `admin123` (change immediately).

### 5. Run development server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

Admin: http://127.0.0.1:8000/admin/

## Docker (Full Stack)

```bash
copy .env.example .env
docker compose up --build
```

- App: http://localhost (via NGINX on port 80)
- Direct Django: http://localhost:8000

## API Endpoints

| Endpoint                     | Method | Description             |
| ---------------------------- | ------ | ----------------------- |
| `/api/v1/site/`              | GET    | Site settings           |
| `/api/v1/skills/`            | GET    | Skill categories        |
| `/api/v1/projects/`          | GET    | All projects            |
| `/api/v1/projects/featured/` | GET    | Featured projects       |
| `/api/v1/contact/`           | POST   | Submit contact form     |
| `/api/v1/chatbot/`           | POST   | AI assistant            |
| `/api/v1/resume/analyze/`    | POST   | Resume keyword analyzer |
| `/api/v1/blog/`              | GET    | Blog posts              |
| `/api/v1/auth/token/`        | POST   | JWT login               |

## Admin Panel

Manage via Django Admin (`/admin/`):

- Projects, Skills, Experience, Certifications
- Blog posts (Markdown/HTML), comments
- Contact messages
- Site settings & theme toggle
- Resume file upload
- Architecture diagrams

## Production Deployment (AWS EC2)

1. Launch EC2 instance (Ubuntu)
2. Install Docker & Docker Compose
3. Clone repo, configure `.env` with production values
4. Set `DJANGO_SETTINGS_MODULE=config.settings.production`
5. Run `docker compose up -d --build`
6. Point domain to EC2, configure SSL (Certbot)

## Tech Stack

- **Backend:** Django 5, DRF, SimpleJWT, PostgreSQL
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **DevOps:** Docker, NGINX, Gunicorn, GitHub Actions

## License

MIT — Personal portfolio project.
