# DariDict Docker setup

## Development

From the folder containing `manage.py`, run:

```sh
make dev
```

Open <http://127.0.0.1:1234/admin/>. No env file is needed. The dev stack
uses Gunicorn and WhiteNoise, runs migrations at
startup, reloads Gunicorn workers on Python changes, and serves static files
directly from the source tree. Django debug mode and local HTTP remain enabled.
Run `make dev-down` to remove the dev containers without deleting the database.
Use `DARIDICT_PORT=1235 make dev` to change the host port.

The dev stack keeps the original `daridict_postgres_data` volume. PostgreSQL
has no published port. To open its CLI:

```sh
docker compose exec postgres psql -U daridict -d daridict_db
```

This stack is for local development only. It does not import a dump
automatically. On a fresh database, load the Dari, Farsi, and German
language rows before opening the dictionary page. Do not use
`docker compose down -v` unless you intend to delete the database.
