#!/usr/bin/env bash
# Одноразова підготовка Ubuntu 24.04 Droplet: Docker, swap, ufw, certbot.
# Запуск: bash deploy/docker/install-docker.sh
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "Запускати від root" >&2
  exit 1
fi

echo "==> apt update"
apt-get update -y
apt-get install -y --no-install-recommends ca-certificates curl git ufw certbot

if ! command -v docker >/dev/null 2>&1; then
  echo "==> Docker"
  curl -fsSL https://get.docker.com | sh
  systemctl enable --now docker
else
  echo "==> Docker вже встановлений: $(docker --version)"
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin відсутній" >&2
  exit 1
fi

# Swap: 2G, якщо RAM < 2GB і swap ще немає (docker build на 1GB → OOM)
MEM_MB=$(awk '/MemTotal/ {printf "%d", $2/1024}' /proc/meminfo)
if [ "${MEM_MB}" -lt 2000 ] && [ ! -f /swapfile ]; then
  echo "==> RAM ${MEM_MB}MB — створюю swap 2G"
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

echo "==> ufw: 22, 80, 443"
ufw allow OpenSSH >/dev/null
ufw allow 80/tcp >/dev/null
ufw allow 443/tcp >/dev/null
ufw --force enable >/dev/null
ufw status | sed 's/^/    /'

echo "==> Зупиняю host nginx/gunicorn (порти 80/443 має тримати лише Docker)"
systemctl disable --now nginx 2>/dev/null || true
systemctl disable --now 'gunicorn-*' 2>/dev/null || true

echo "==> Готово. Далі: cp .env.example .env && nano .env && bash deploy/docker/deploy.sh"
