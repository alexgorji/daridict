# DariDict Docker setup

## Development

From the folder containing `manage.py`, run:

```sh
make dev
```

Open <http://127.0.0.1:1234/admin/>. You don't need to create an env file.
Compose loads the tracked development defaults from [`container/env`](./container/env).
Use an optional, ignored `.env.local` to override backend settings such as
`DEBUG`, `ALLOWED_HOSTS`, or `SECRET_KEY`. A `SECRET_KEY` is required when
`DEBUG=false`.

The [container entrypoint](./container/daridict.sh) runs migrations before
starting Gunicorn. Development reloads workers on Python changes, and
WhiteNoise serves static files directly from the source tree.
Run `make dev-down` to remove the dev containers without deleting the database.
Use `DARIDICT_PORT=1235 make dev` to change the host port.

The dev stack keeps the original `daridict_postgres_data` volume. PostgreSQL
has no published port. To open its CLI:

```sh
docker compose exec postgres psql -U daridict -d daridict_db
```

Run a Django management command without starting another web server:

```sh
docker compose exec backend daridict manage check
```

This stack is for local development only. It does not import a dump
automatically. On a fresh database, load the Dari, Farsi, and German
language rows before opening the dictionary page. Do not use
`docker compose down -v` unless you intend to delete the database.
