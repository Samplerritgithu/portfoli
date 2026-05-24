"""
Production settings — Render, Docker, AWS EC2.
"""
import os

import dj_database_url
from decouple import Csv, config

from .base import *  # noqa: F403

DEBUG = config('DEBUG', default=False, cast=bool)

# --- ALLOWED_HOSTS (Render: set ALLOWED_HOSTS=* or your .onrender.com URL) ---
def _parse_allowed_hosts():
    raw = os.environ.get('ALLOWED_HOSTS') or config('ALLOWED_HOSTS', default='')
    raw = str(raw).strip()
    if raw == '*' or '*' in [p.strip() for p in raw.split(',') if p.strip()]:
        return ['*']
    hosts = [h.strip() for h in raw.split(',') if h.strip()]
    render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if render_host and render_host not in hosts:
        hosts.append(render_host)
    # Subdomain wildcard for all Render apps
    if '.onrender.com' not in hosts:
        hosts.append('.onrender.com')
    if not hosts:
        hosts = ['localhost', '127.0.0.1', '.onrender.com']
    return hosts


ALLOWED_HOSTS = _parse_allowed_hosts()

# --- CSRF (required for HTTPS on Render) ---
_csrf = list(config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv()))
_render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if _render_host:
    _csrf.append(f'https://{_render_host}')
_render_url = os.environ.get('RENDER_EXTERNAL_URL', '').rstrip('/')
if _render_url and _render_url not in _csrf:
    _csrf.append(_render_url)
CSRF_TRUSTED_ORIGINS = _csrf

# --- Database: Render PostgreSQL via DATABASE_URL ---
_database_url = os.environ.get('DATABASE_URL')
if _database_url:
    DATABASES['default'] = dj_database_url.parse(  # noqa: F405
        _database_url,
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )

# --- Security behind Render proxy ---
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# --- CORS: include Render URL when deployed ---
_cors = list(CORS_ALLOWED_ORIGINS)  # noqa: F405
if _render_url and _render_url not in _cors:
    _cors.append(_render_url)
CORS_ALLOWED_ORIGINS = _cors

# --- Static files (Whitenoise) ---
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
