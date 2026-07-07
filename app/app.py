import json
import logging
import time
from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Jumlah total request yang ditangani aplikasi dummy",
    ["endpoint"],
)

# Logger yang menulis satu baris JSON per peristiwa ke file di volume bersama.
logger = logging.getLogger("dummy-app")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("/logs/app.log")
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)

def log_event(level, message, **fields):
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "level": level,
        "message": message,
    }
    entry.update(fields)
    logger.info(json.dumps(entry))

@app.route("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()
    log_event("INFO", "Halaman utama diakses", endpoint="/")
    return "Halo dari aplikasi dummy. Buka /metrics untuk melihat angkanya.\n"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    log_event("INFO", "Aplikasi dummy mulai berjalan")
    app.run(host="0.0.0.0", port=8000)
