# de Baffo Backend

This repository contains the Django backend for the **de Baffo** restaurant website. It exposes REST APIs for managing menu categories and dishes.

## Setup

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Configure PostgreSQL (update credentials in `debaffo_backend/settings.py` if necessary) and apply migrations:

```bash
python manage.py migrate
```

3. Run the development server:

```bash
python manage.py runserver
```

### Loading initial data

You can load menu data from a JSON or CSV file using the custom command:

```bash
python manage.py load_initial_data path/to/data.json
```

## API

- Browse APIs at `/swagger/` or `/redoc/`.
- CRUD endpoints are available under `/api/`.
