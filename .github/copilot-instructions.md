# Copilot Instructions – Government Institutional Website (Django)

This is a multi-tenant Django 5.1 institutional website with a public-facing front-end and secure role-based back-office. 

## Architecture Overview

**Five modular apps** with clear boundaries:
- **`accounts`**: Custom user model (`User`) with role field; role groups auto-created on migration (`Content Editor`, `Department Officer`)
- **`content`**: Core entities (Pages, Departments, Services, News/Events, Career Postings, Site Settings)
- **`notices`**: Announcements with optional file attachment
- **`downloads`**: Document repository (PDFs, images)
- **`audit`**: Activity logging for all CRUD events + IP/user-agent tracking via middleware

**Settings** are environment-driven:
- `config/settings/base.py` — shared config; loads `.env` or `env` file using `python-dotenv`
- `config/settings/dev.py` — development (SQLite default)
- `config/settings/prod.py` — production (requires `DB_ENGINE`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` env vars)
- Default: `config.settings.dev` unless `DJANGO_SETTINGS_MODULE` is set

## Key Design Patterns

### 1. **Abstract Model Hierarchy**
Three reusable mixins in [content/models.py](content/models.py):
- **`TimeStampedModel`** — auto-managed `created_at`, `updated_at`
- **`AuthorTrackedModel`** — `created_by`, `updated_by` ForeignKey to User
- **`PublishableModel`** — `status` (DRAFT/PUBLISHED/ARCHIVED), `published_at`, `archived_at`

All content models inherit from these. Public views filter by `status=PublishStatus.PUBLISHED`.

### 2. **Publish/Archive Workflow**
Django Admin includes two bulk actions (`PublishActionsMixin`, `AuthorAdminMixin` in [content/admin.py](content/admin.py)):
- "Publish selected items" — sets status→PUBLISHED, `published_at→now()`
- "Archive selected items" — sets status→ARCHIVED, `archived_at→now()`
- `updated_by` is auto-set to request.user on save

### 3. **Automatic Audit Logging**
[audit/signals.py](audit/signals.py) registers `post_save` and `post_delete` handlers for a hardcoded `TRACKED_MODELS` tuple. When a tracked model is modified, [audit/utils.py](audit/utils.py) logs to `ActivityLog`:
- User, IP, user-agent (captured by [audit/middleware.py](audit/middleware.py) → thread-local storage)
- Model label (e.g., `content.Page`), object ID, action type (CREATE/UPDATE/DELETE)

**When adding a new trackable model:** add it to `TRACKED_MODELS` in [audit/signals.py](audit/signals.py).

### 4. **Role-Based Access Control (RBAC)**
Two Django `Group`-based roles auto-created on migration via [accounts/signals.py](accounts/signals.py):
- **Content Editor** — can create/change Pages, NewsItems, Services, Notices, Documents
- **Department Officer** — subset: NewsItems, Documents, Notices only

Super Admin: Django's built-in `is_superuser` flag (full access).
Assign users to groups in Django Admin under `Users > Groups` and edit user membership.

### 5. **Public/Admin URL Split**
[config/urls.py](config/urls.py) routes:
- `/admin/` — Django Admin (requires `is_staff`)
- `""` → `content.urls_public` (home, pages, departments, services, news, careers)
- `notices/` → `notices.urls_public`
- `downloads/` → `downloads.urls_public`

Apps have separate `urls_public.py` files; views are generic (ListView, DetailView) filtering by `PublishStatus.PUBLISHED`.

## Critical Developer Workflows

### Setup & Run
```bash
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt

# Migrate database
.\.venv\Scripts\python manage.py migrate

# Create superuser
.\.venv\Scripts\python manage.py createsuperuser

# Run server
.\.venv\Scripts\python manage.py runserver
# Admin: http://127.0.0.1:8000/admin/ | Public: http://127.0.0.1:8000/
```

### Environment Configuration
1. Copy `env.example` → `env` (for local use, `.env` may be blocked in some environments)
2. Set `DJANGO_SECRET_KEY`, `DB_*` vars, `DJANGO_ALLOWED_HOSTS`, `DJANGO_DEBUG`
3. Restart server; settings auto-reload from file

### Database & Migrations
- Default: SQLite (`db.sqlite3`)
- Production: PostgreSQL (requires `psycopg[binary]` — already in requirements)
- After model changes: `python manage.py makemigrations <app>` then `python manage.py migrate`

### Media & Uploads
Uploads go to `media/` directory. Models with file fields:
- `content.NewsItem.cover_image`
- `content.SiteSettings.logo`
- `notices.Notice.attachment`
- `downloads.Document.file`

In `DEBUG=1`, Django serves media; in production, use WhiteNoise or reverse proxy.

## Dependency Insights

- **django==5.1.5** — main framework
- **python-dotenv** — env file loading
- **Pillow** — image processing (covers, logos)
- **django-widget-tweaks** — template form rendering customization
- **whitenoise==6.7.0** — static files in production
- **psycopg[binary]** — PostgreSQL adapter

## Common Tasks & Patterns

### Add a New Content Type
1. Define model in `content/models.py` inheriting from `TimeStampedModel`, `AuthorTrackedModel`, `PublishableModel`
2. Register in `content/admin.py` with `PublishActionsMixin`, `AuthorAdminMixin`
3. Add to `TRACKED_MODELS` in [audit/signals.py](audit/signals.py) to enable audit logging
4. Create `urls_public.py` route if public-facing
5. Create view(s) in `views.py` filtering by `status=PublishStatus.PUBLISHED`
6. Add template to `templates/public/`

### Add a New Role/Permission
1. Edit `ROLE_GROUPS` dict in [accounts/signals.py](accounts/signals.py)
2. Run `migrate` or `python manage.py post_migrate` to sync (post_migrate signal runs automatically)
3. Assign users via Admin UI

### Debug Audit Logs
- Query `ActivityLog` in Admin or shell: `ActivityLog.objects.filter(model_label='content.Page').order_by('-created_at')`
- Check `ip_address`, `user_agent`, `action` fields for compliance/troubleshooting
- Middleware context set in [audit/middleware.py](audit/middleware.py) — runs after auth

### Context Processors & Template Globals
[content/context_processors.py](content/context_processors.py) provides `site_settings` to all templates (logo, contact info, etc.). Defined in `TEMPLATES[OPTIONS][context_processors]`.

## Troubleshooting

- **Audit logs missing?** Ensure model is in `TRACKED_MODELS`; check middleware order (must be after `AuthenticationMiddleware`)
- **Groups not created?** Run `migrate` or `python manage.py post_migrate --app accounts`
- **Env vars not loading?** Check `.env` vs `env` file existence; `dotenv` loads both if present
- **Static/media 404 in DEBUG=0?** Enable WhiteNoise or configure reverse proxy; see `settings/prod.py`
