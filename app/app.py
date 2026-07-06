from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Counter adalah metrik yang nilainya hanya bisa naik, tidak pernah turun.
# Nama metriknya app_requests_total, dengan satu label bernama endpoint.
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Jumlah total request yang ditangani aplikasi dummy",
    ["endpoint"],
)

@app.route("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return "Halo dari aplikasi dummy. Buka /metrics untuk melihat angkanya.\n"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
