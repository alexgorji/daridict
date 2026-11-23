# DariDict: local Docker setup

From the folder containing `manage.py`, run:

```sh
docker compose up --build
```

The Compose file supplies a local-only PostgreSQL password. No env file is
required. Do not reuse the development password on a server.

The admin login is at <http://127.0.0.1:1234/admin/>. The dictionary page
requires the Dari, Farsi, and German language rows; load your dictionary
data before opening it. To use a different local port, run
`DARIDICT_PORT=1235 docker compose up --build`. Rebuild after changing source
code or `uv.lock`.

The backend runs Django migrations at startup. PostgreSQL is only reachable
inside Compose and its named volume survives `docker compose down`. The
database starts empty; the existing PostgreSQL dump is not imported.

Open the local database CLI with:

```sh
docker compose exec postgres psql -U daridict -d daridict_db
```

Keep the same database password when reusing the volume. Editing
`POSTGRES_PASSWORD` does not change the password of an initialized database.
Do not use `docker compose down -v` unless you intend to delete the local
database. This stack uses Django's development server and is not for production.
