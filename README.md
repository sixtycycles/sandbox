# pizza-cloud

A Django web application for tracking orders placed with vendors.
Originally an internal lab ordering tool (UCLA EPSS context) — kept here as a
public sandbox after its private history was archived.

## What it does

Lets a user create an **Order** for a **Vendor**, attach one or more line-item
**Items** to that order, and record delivery details via a **DeliveryLabel**.
Users are a custom `User` model (Django `AbstractUser` extended with a `uid`
field).

## Tech stack

- **Python 3** + **Django** (web framework)
- **django-localflavor** — US state / ZIP / postal-code model fields
- **django-widget-tweaks** — form rendering in templates
- **Black** — code formatting (dev dependency)

See `requirements.txt` for pinned packages.

## Project layout

```
pizza-cloud/
├── manage.py                  # Django entry point
├── pizzacloud/               # Project config package
│   ├── settings.py            # Django settings (DB, apps, middleware)
│   ├── urls.py                # Root URL config
│   └── wsgi.py
├── pizzas/                    # Main application
│   ├── models.py              # User, Vendor, DeliveryLabel, Order, Item
│   ├── views.py               # List / detail / create / edit views
│   ├── forms.py               # Model forms
│   ├── urls.py                # App URL routes
│   ├── admin.py               # Django admin registrations
│   ├── migrations/            # DB migrations
│   └── templates/             # HTML templates (order & item views, landing)
└── requirements.txt
```

## Data model

| Model           | Key fields                                                        |
| --------------- | ----------------------------------------------------------------- |
| `User`          | extends `AbstractUser` + `uid` (10-char code)                     |
| `Vendor`        | `name`, `street`, `city`, `state` (US), `zip`, `email`, `phone`   |
| `DeliveryLabel` | `deliver_to`, `email`, `room_number`, `ship_method`, `delivery_date`, `mark_urgent`, order contact info |
| `Order`         | `user` (FK), `vendor` (FK), `timestamp_created`                   |
| `Item`          | `order` (FK), `quantity`, `unit`, `catalog_number`, `cost_per_unit`, `description`, `link_to_item` |

## Local setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations (uses a local SQLite DB by default)
python manage.py migrate

# 4. Create an admin user
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Then open http://localhost:8000/ .

> **Note:** `settings.py` is configured for local development (`DEBUG = True`,
> a local SQLite database, and `ALLOWED_HOSTS` restrained to localhost). The
> tracked development database is intentionally **not** committed to this repo.
> Do not use these settings for production without changing `SECRET_KEY`,
> `DEBUG`, and the database credentials.

## License

BSD 3-Clause — see [LICENSE](LICENSE). Copyright (c) 2026, Rod.
