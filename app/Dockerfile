FROM python:3.12-slim

# Buat pengguna non-root bernama appuser.
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY gunicorn.conf.py .

# Siapkan folder log dan serahkan kepemilikannya ke appuser.
RUN mkdir -p /logs && chown -R appuser:appuser /logs

# Folder bersama tempat tiap worker menulis metriknya.
ENV PROMETHEUS_MULTIPROC_DIR=/prom_multiproc
RUN mkdir -p /prom_multiproc && chown -R appuser:appuser /prom_multiproc

# Serahkan kepemilikan folder kerja ke appuser, lalu beralih ke pengguna itu.
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Docker mengetuk /metrics secara berkala untuk menilai kesehatan aplikasi.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/metrics')" || exit 1

CMD ["gunicorn", "-c", "gunicorn.conf.py", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
