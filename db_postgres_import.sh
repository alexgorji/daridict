#!/usr/bin/env bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$DIR/config.sh"

PROJECT="$(basename $DIR)"
DB=${PROJECT}_db

#if [ $USER = root ]; then
#  sudo -u postgres psql -U postgres -d postgres -c "ALTER USER root WITH SUPERUSER"
#fi
PROJECT="$(basename $DIR)"

cd ../${PROJECT}-data

psql -U $POSTGRES_USER -d postgres -c "DROP DATABASE IF EXISTS ${DB}"
psql -U $POSTGRES_USER -d postgres -c "CREATE DATABASE ${DB}"
psql -U $POSTGRES_USER -d postgres -c "ALTER DATABASE ${DB} OWNER TO ${POSTGRES_USER}"


FILE=dumped_db
if test -f "$FILE"; then
    psql -U $POSTGRES_USER -d $DB < $FILE
fi

