#!/usr/bin/env bash

set -e
bash db_git_pull.sh
bash db_postgres_import.sh
bash restart_gunicorn.sh
