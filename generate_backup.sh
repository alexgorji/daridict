#!/usr/bin/env bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PROJECT="$(basename $DIR)"
DB=${PROJECT}_db

#if [ $USER != ansible-admin ]; then
#  cd $DIR/$PROJECT
#  python manage.py collectstatic --no-input
#fi

cd $DIR

git add .
if git status | grep "nothing to commit" >/dev/null; then
  echo "nothing to commit"
else
  git commit -m backup
fi

git pull --rebase
git push

cd ../${PROJECT}-data

echo $()
pg_dump $DB > dumped_db

git add .

if git status | grep "nothing to commit" >/dev/null; then
  echo "nothing to commit"
else
  git commit -m dumped
fi

git pull --rebase
git push
