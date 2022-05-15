#!/usr/bin/env bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PROJECT="$(basename ${DIR})"
DB=${PROJECT}_db

cd $DIR
cd ../${PROJECT}-data

pg_dump $DB > dumped_db

git add .
git commit -m dumped
git push
