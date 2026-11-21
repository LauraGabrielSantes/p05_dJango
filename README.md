# Práctica 5 — API REST de usuarios y productos

Continuación de la práctica 4. Agrega la aplicación `gestion_productos`: CRUD, borrado lógico, búsqueda, filtro por precio y activación.

## Arranque

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp back_end_django/.env.example back_end_django/.env
cd back_end_django
python manage.py migrate
python manage.py runserver
```

Swagger: `http://127.0.0.1:8000/swagger/`

## Tests

```bash
cd back_end_django
python manage.py test
```
