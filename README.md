# DSCC CW1 — Django Blog Application (ID: 00017298)

A full-stack Django blog application with complete DevOps pipeline including Docker containerization, Nginx reverse proxy, PostgreSQL database, CI/CD with GitHub Actions, and HTTPS deployment.

## Features

- **User Authentication:** Registration, login, logout, password change/reset
- **Article Management:** Full CRUD (Create, Read, Update, Delete) operations
- **Rich Text Editor:** CKEditor integration for article body content
- **Image Uploads:** Photo uploads for articles
- **Comments System:** Users can comment on articles (many-to-one)
- **Tagging System:** Articles can be tagged with multiple tags (many-to-many)
- **Admin Panel:** Full Django admin with custom user admin, inline comments, and tag management
- **Responsive Design:** Bootstrap 5 based responsive UI

## Technologies Used

| Technology | Purpose |
|---|---|
| Django 6.0 | Web framework |
| PostgreSQL 16 | Primary database |
| Docker | Containerization |
| Docker Compose | Multi-service orchestration |
| Nginx | Reverse proxy & static file serving |
| Gunicorn | WSGI HTTP server |
| GitHub Actions | CI/CD pipeline |
| Let's Encrypt | SSL/HTTPS certificates |
| Bootstrap 5 | Frontend CSS framework |
| CKEditor | Rich text editor |
| WhiteNoise | Static file compression |
| pytest-django | Testing framework |
| flake8 | Code quality linting |

## Database Models

| Model | Type | Relationships |
|---|---|---|
| **CustomUser** | Auth model | Extends AbstractUser (has `age` field) |
| **Article** | Content model | ForeignKey → User (many-to-one), ManyToMany → Tag |
| **Comment** | Content model | ForeignKey → Article (many-to-one), ForeignKey → User |
| **Tag** | Taxonomy model | ManyToMany ← Article (many-to-many) |

## Project Structure

```
├── .github/workflows/    # CI/CD pipeline
│   └── deploy.yml
├── accounts/             # User authentication app
├── articles/             # Blog articles app (CRUD)
├── config/               # Django project settings
├── nginx/                # Nginx configuration
│   └── nginx.conf
├── pages/                # Static pages (home)
├── static/               # Static assets
├── templates/            # HTML templates
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Production orchestration
├── docker-compose.dev.yml # Development orchestration
├── requirements.txt      # Python dependencies
└── .env.example          # Environment variable template
```

## Local Setup Instructions

### Prerequisites
- Docker & Docker Compose installed
- Git installed

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/theKhursandbek/-DSCC_CW1_00017298.git
   cd -DSCC_CW1_00017298
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. **Start with Docker Compose (development):**
   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```

4. **Run migrations:**
   ```bash
   docker compose -f docker-compose.dev.yml exec web python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   docker compose -f docker-compose.dev.yml exec -it web python manage.py createsuperuser
   ```

6. **Access the application:**
   - Application: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Production Deployment

### Server Requirements
- Ubuntu 22.04+ server
- Docker & Docker Compose installed
- Domain pointed to server IP
- Ports 22, 80, 443 open in firewall

### Deployment Steps

1. **SSH into the server:**
   ```bash
   ssh user@your-server-ip
   ```

2. **Clone and configure:**
   ```bash
   git clone https://github.com/theKhursandbek/-DSCC_CW1_00017298.git ~/dscc-cw1-00017298
   cd ~/dscc-cw1-00017298
   cp .env.example .env
   nano .env  # Fill in production values
   ```

3. **Start services:**
   ```bash
   docker compose up -d --build
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py collectstatic --noinput
   docker compose exec -it web python manage.py createsuperuser
   ```

4. **Install SSL certificate:**
   ```bash
   sudo apt install certbot
   sudo certbot certonly --webroot -w /var/www/certbot \
       -d yourdomain.uz -d www.yourdomain.uz \
       --email your@email.com --agree-tos
   docker compose restart nginx
   ```

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `your-random-50-char-string` |
| `DEBUG` | Debug mode (False in production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `yourdomain.uz,www.yourdomain.uz` |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF | `https://yourdomain.uz` |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@db:5432/dbname` |
| `POSTGRES_DB` | PostgreSQL database name | `newsdb` |
| `POSTGRES_USER` | PostgreSQL username | `newsuser` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `newspass` |

## CI/CD Pipeline

The GitHub Actions pipeline (`.github/workflows/deploy.yml`) runs on every push to `main`:

1. **Lint** — Code quality check with flake8
2. **Test** — Run pytest-django test suite (23 tests)
3. **Build** — Build Docker image (multi-stage, <200MB)
4. **Push** — Push image to Docker Hub (tagged with `latest` + commit SHA)
5. **Deploy** — SSH to production server, pull image, restart services, run migrations

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `SSH_PRIVATE_KEY` | SSH private key for server |
| `SSH_HOST` | Server IP address or domain |
| `SSH_USERNAME` | SSH username |

## Running Tests

```bash
# With Docker
docker compose exec web python -m pytest --tb=short -q

# Locally
python -m pytest --tb=short -q
```

## Screenshots

*(Screenshots of the running application will be added here)*

## Author

**Khursandbek Saidov** — Student ID: 00017298

## License

This project is developed for DSCC coursework at Westminster International University in Tashkent.
