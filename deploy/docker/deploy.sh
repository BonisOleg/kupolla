#!/usr/bin/env bash
# Деплой/оновлення KUPOLLA на Droplet.
#   bash deploy/docker/deploy.sh          # HTTP (docker.conf), до сертифіката
#   bash deploy/docker/deploy.sh --prod   # HTTPS (docker.prod.conf + /etc/letsencrypt)
# Автовибір: якщо є /etc/letsencrypt/live/kupolla.com/fullchain.pem → prod.
set -uo pipefail

cd "$(dirname "$0")/../.."
PROJECT_DIR="$(pwd)"
DOMAIN="kupolla.com"
CERT="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"

MODE="auto"
[ "${1:-}" = "--prod" ] && MODE="prod"
[ "${1:-}" = "--http" ] && MODE="http"
if [ "${MODE}" = "auto" ]; then
  if [ -f "${CERT}" ]; then MODE="prod"; else MODE="http"; fi
fi

COMPOSE="docker compose -f docker-compose.yml"
[ "${MODE}" = "prod" ] && COMPOSE="${COMPOSE} -f docker-compose.prod.yml"

echo "==> Режим: ${MODE}  (${PROJECT_DIR})"

if [ ! -f .env ]; then
  echo "FATAL: немає .env — cp .env.example .env і заповнити" >&2
  exit 1
fi

if grep -Eq '^ALLOWED_HOSTS=.*DROPLET_IP' .env; then
  echo "FATAL: у .env лишився літерал DROPLET_IP — замінити на реальний IPv4" >&2
  exit 1
fi

for key in SECRET_KEY POSTGRES_PASSWORD ALLOWED_HOSTS; do
  if ! grep -Eq "^${key}=.+" .env; then
    echo "FATAL: ${key} порожній у .env" >&2
    exit 1
  fi
done

echo "==> Звільняю порти 80/443 від host-сервісів"
systemctl stop nginx 2>/dev/null || true
systemctl stop 'gunicorn-*' 2>/dev/null || true

echo "==> Build web"
if ! ${COMPOSE} build web; then
  echo "FATAL: build failed" >&2
  exit 1
fi

echo "==> Up (перший прохід нефатальний: web чекає міграції)"
${COMPOSE} up -d --remove-orphans || true

echo "==> Чекаю /healthz/ (до 5 хв)"
HEALTH_OK=0
for _ in $(seq 1 60); do
  if curl -sf -H "Host: ${DOMAIN}" http://127.0.0.1/healthz/ >/dev/null 2>&1; then
    HEALTH_OK=1
    break
  fi
  sleep 5
done

if [ "${HEALTH_OK}" -ne 1 ]; then
  echo "WARN: healthz ще не 200 — дивись логи:" >&2
  ${COMPOSE} logs --tail=40 web nginx
else
  echo "==> healthz OK"
fi

echo "==> Фінальний up (гарантує nginx після повільних міграцій)"
${COMPOSE} up -d --remove-orphans

echo "==> Інвентаризація сервісів"
MISSING=0
for svc in db web nginx; do
  if ${COMPOSE} ps --status running --services 2>/dev/null | grep -qx "${svc}"; then
    echo "    ${svc}: running"
  else
    echo "    ${svc}: MISSING" >&2
    MISSING=1
  fi
done

if [ "${MODE}" = "prod" ]; then
  echo "==> HTTPS перевірка"
  ${COMPOSE} exec -T nginx nginx -t 2>&1 | sed 's/^/    /'
  if curl -skf https://127.0.0.1/healthz/ -H "Host: ${DOMAIN}" >/dev/null; then
    echo "    HTTPS healthz OK"
  else
    echo "    WARN: HTTPS healthz не відповідає" >&2
  fi
fi

echo "==> Прибираю dangling images"
docker image prune -f >/dev/null 2>&1 || true

echo "==> ${COMPOSE} ps"
${COMPOSE} ps

[ "${MISSING}" -eq 0 ] && [ "${HEALTH_OK}" -eq 1 ]
