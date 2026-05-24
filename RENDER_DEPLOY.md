# Deploy to Render

## Fix: `DisallowedHost` / Bad Request (400)

Add this in **Render Dashboard → Your Web Service → Environment**:

| Key | Value |
|-----|--------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `ALLOWED_HOSTS` | `*` |
| `SECRET_KEY` | *(generate a long random string)* |
| `DEBUG` | `False` |
| `DATABASE_URL` | *(auto if PostgreSQL is linked)* |

After saving, **Manual Deploy → Deploy latest commit**.

`ALLOWED_HOSTS=*` allows your Render URL (e.g. `portfoli-42ul.onrender.com`).  
The app also auto-adds `RENDER_EXTERNAL_HOSTNAME` and `.onrender.com` when not using `*`.

---

## Required environment variables

| Variable | Required | Example |
|----------|----------|---------|
| `DJANGO_SETTINGS_MODULE` | Yes | `config.settings.production` |
| `SECRET_KEY` | Yes | `your-50-char-random-secret` |
| `ALLOWED_HOSTS` | Yes | `*` or `portfoli-42ul.onrender.com` |
| `DATABASE_URL` | Yes* | Auto from Render PostgreSQL |
| `DEBUG` | No | `False` |
| `CSRF_TRUSTED_ORIGINS` | Recommended | `https://portfoli-42ul.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | No | `https://portfoli-42ul.onrender.com` |
| `GITHUB_URL` | No | Your GitHub profile URL |
| `LINKEDIN_URL` | No | Your LinkedIn URL |
| `CONTACT_EMAIL` | No | your@email.com |
| `CONTACT_NOTIFICATION_EMAIL` | No | your@email.com |
| `EMAIL_HOST_USER` | No | SMTP user |
| `EMAIL_HOST_PASSWORD` | No | SMTP password |

\* Create a **PostgreSQL** database on Render and link it to the web service so `DATABASE_URL` is injected.

---

## Steps

### 1. PostgreSQL on Render

1. **New +** → **PostgreSQL**
2. Name: `portfolio-db`
3. Copy **Internal Database URL** (or link DB to web service)

### 2. Web Service (Docker)

1. **New +** → **Web Service**
2. Connect your GitHub repo
3. **Runtime:** Docker
4. **Dockerfile path:** `./Dockerfile`
5. Add environment variables from the table above
6. **Create Web Service**

### 3. First deploy commands (optional)

Migrations run automatically via `scripts/entrypoint.sh`.

To load demo content once:

```bash
# Render Shell (one time)
RUN_SEED=true
# Or in shell:
python manage.py seed_portfolio
python manage.py createsuperuser
```

Set `RUN_SEED=true` only for the first deploy, then remove it.

### 4. CSRF for HTTPS

If forms fail after deploy, set:

```
CSRF_TRUSTED_ORIGINS=https://portfoli-42ul.onrender.com
```

Replace with your actual Render URL.

---

## Using render.yaml (Blueprint)

1. Push `render.yaml` to your repo
2. **New +** → **Blueprint**
3. Connect repo — Render creates web service + database
4. Fill sync=false vars (`GITHUB_URL`, etc.) in the dashboard

---

## Health check

Render uses `/` as health check. Gunicorn binds to `PORT` (default `8000`).

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `DisallowedHost` | Set `ALLOWED_HOSTS=*` and redeploy |
| 502 / app not starting | Check logs; ensure `DATABASE_URL` is set |
| Static files 404 | `collectstatic` runs in Docker build; check build logs |
| CSRF error on contact form | Add site URL to `CSRF_TRUSTED_ORIGINS` |
| Database connection | Use Render PostgreSQL `DATABASE_URL`, not SQLite |
