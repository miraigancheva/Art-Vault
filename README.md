# ArtVault - Digital Gallery Management System

ArtVault is a Django web application for managing a digital art gallery. It allows users to catalogue artists, manage their artworks, and curate exhibitions through a clean, responsive Bootstrap interface.

---

## Project Architecture

The project is split into three Django applications, each with a clearly defined responsibility:

| App | Responsibility |
|-----|---------------|
| `artists` | Manage artist profiles, biographies, and nationalities |
| `artworks` | Manage individual artworks and their medium categories |
| `exhibitions` | Curate exhibitions that group multiple artworks together |

### Database Relationships

- Many-to-One (ForeignKey): `Artwork -> Artist` (each artwork belongs to one artist), `Artwork -> Category`
- Many-to-Many: `Exhibition <-> Artwork` (an exhibition can feature many artworks; an artwork can appear in many exhibitions)

---

## Tech Stack

- Framework: Django 5.x
- Database: PostgreSQL
- Frontend: Bootstrap 5 + Bootstrap Icons
- Python: 3.10+

---

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/artvault.git
cd artvault
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Rename the example file to `.env`:

```bash
mv env.example .env
```

Then open `.env` and fill in your values:

```
SECRET_KEY=django-insecure-anyrandomlongstring1234567890abcdef
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
DB_NAME=artvault_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 5. Create the static folder

```bash
mkdir -p static
```

### 6. Create the PostgreSQL database

Make sure PostgreSQL is running, then:

```bash
sudo -u postgres createdb artvault_db
```

### 7. Create and apply migrations

```bash
python manage.py makemigrations artists artworks exhibitions
python manage.py migrate
```

### 8. Create a superuser

```bash
python manage.py createsuperuser
```

### 9. Run the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000

---

## Local Testing Credentials

These are the credentials needed to run the project locally without any modifications.

Database:

```
DB_NAME=artvault_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Admin panel (after running createsuperuser with the values below):

```
URL:      http://127.0.0.1:8000/admin
Username: admin
Email:    admin@admin.com
Password: admin1234
```

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | (required) | Django secret key |
| `DEBUG` | `True` | Enable/disable debug mode |
| `DB_NAME` | `artvault_db` | PostgreSQL database name |
| `DB_USER` | `postgres` | Database username |
| `DB_PASSWORD` | `postgres` | Database password |
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `5432` | Database port |
| `ALLOWED_HOSTS` | `localhost 127.0.0.1` | Space-separated allowed hosts |

---

## Features

### Artists App
- Full CRUD for artist profiles
- Filter by nationality and search by name or biography
- Custom template tags: lifespan, artwork_count, nationality_badge
- Pagination (9 per page)

### Artworks App
- Full CRUD for artworks
- Full CRUD for categories with colour picker
- Filter by category, display status, and sort order
- Related artworks panel on detail page
- Artwork value formatting via model method

### Exhibitions App
- Full CRUD for exhibitions
- Many-to-many artwork selector with scrollable checkbox list
- Live Now badge via is_ongoing() model method
- Duration display via get_duration_days() model method
- Active/All filter tabs

### Other
- Custom 404 page
- Bootstrap 5 responsive design
- Flash messages on all CRUD actions
- Confirmation step before every delete
- Breadcrumb navigation
- Consistent navigation and footer on all pages

---

## File Structure

```
artvault/
├── artvault/          # Project settings, root URLs, home view
├── artists/           # Artist model, CRUD views, templatetags
├── artworks/          # Artwork and Category models, CRUD views
├── exhibitions/       # Exhibition model, CRUD views
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── 404.html
│   ├── partials/
│   ├── artists/
│   ├── artworks/
│   └── exhibitions/
├── static/
├── manage.py
├── requirements.txt
├── env.example
└── README.md
```

---

## Notes

- Authentication is intentionally excluded per project requirements.
- The static/ folder must be created manually before running the server (see step 5).
- PostgreSQL must be installed and running before applying migrations.