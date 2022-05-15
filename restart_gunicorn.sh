set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PROJECT="$(basename $DIR)"
cd ../${PROJECT}-data

if [ "$USER" == "$POSTGRES_USER" ]; then
  echo "restarting gunicorn_${PROJECT}"
  systemctl restart gunicorn_${PROJECT}
fi