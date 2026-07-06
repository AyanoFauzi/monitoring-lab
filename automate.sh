#!/usr/bin/env bash
set -e

echo "==> Menyalakan stack monitoring Lab 1"
docker compose up -d --build

echo "==> Menunggu service siap"
sleep 5

echo "==> Status service"
docker compose ps

echo ""
echo "Stack siap. Buka di browser:"
echo "  Aplikasi   : http://localhost:8000/"
echo "  Prometheus : http://localhost:9090"
echo "  Grafana    : http://localhost:3000"
