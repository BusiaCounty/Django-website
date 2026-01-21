# Government Institutional Website (Django)

Public-facing responsive website + secure back-office using Django Admin.

## Apps

- `accounts`: Custom user (`accounts.User`) + role groups (Content Editor, Department Officer)
- `content`: Pages, Departments, Services, News & Events, Careers, Site Settings
- `notices`: Notices & Announcements (optional attachment)
- `downloads`: Downloadable documents (PDF/images/etc.)
- `audit`: Activity logs (create/update/delete) with user/ip/user-agent

## Quickstart (Windows)

Create environment and install deps:

```bash
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

Run migrations:

```bash
.\.venv\Scripts\python manage.py migrate
```

Create a Super Admin:

```bash
.\.venv\Scripts\python manage.py createsuperuser
```

Start the server:

```bash
.\.venv\Scripts\python manage.py runserver
```

- Admin: `http://127.0.0.1:8000/admin/`
- Public site: `http://127.0.0.1:8000/`

## Environment-based settings

Settings modules:

- Development: `config.settings.dev`
- Production: `config.settings.prod`

Create a local `env` file (recommended) from `env.example`:

1. Copy `env.example` → `env`
2. Set `DJANGO_SECRET_KEY`, database creds, and allowed hosts

`manage.py` defaults to `config.settings.dev` unless `DJANGO_SETTINGS_MODULE` is set.

## Media + documents

- Uploads go to `media/` (development)
- Models using uploads:
  - `content.NewsItem.cover_image`
  - `content.SiteSettings.logo`
  - `notices.Notice.attachment`
  - `downloads.Document.file`

## Draft / publish workflow

Most content models have:

- `status`: Draft / Published / Archived
- `published_at`, `archived_at`

In Django Admin, use actions:

- “Publish selected items”
- “Archive selected items”

## Roles (RBAC)

- **Super Admin**: Django `is_superuser` (full access)
- **Content Editor**: group “Content Editor” (create/change core content)
- **Department Officer**: group “Department Officer” (create/change departmental content)

Groups are auto-created on migration via `accounts.signals`.

## Audit logging

All create/update/delete events for tracked models are logged in `audit.ActivityLog`.

Track list currently includes:

- `content.Page`, `content.Department`, `content.Service`, `content.NewsItem`, `content.CareerPosting`
- `notices.Notice`
- `downloads.Document`

## Deployment notes (high-level)

- Set `DJANGO_SETTINGS_MODULE=config.settings.prod`
- Set `DJANGO_ALLOWED_HOSTS` and `DJANGO_SECRET_KEY`
- Use PostgreSQL in production (see `env.example`)
- Configure HTTPS (reverse proxy / load balancer). `config.settings.prod` enables secure cookies + SSL redirect.
- Static files: WhiteNoise is enabled; collect with:

```bash
.\.venv\Scripts\python manage.py collectstatic
```

## Backup / restore strategy

- **PostgreSQL**:
  - Backup: `pg_dump` (daily + offsite)
  - Restore: `pg_restore`
- **Media files**: backup the `media/` folder alongside DB dumps (same schedule).

