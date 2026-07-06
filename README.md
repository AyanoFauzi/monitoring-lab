# Lab 1: Fondasi Monitoring dengan Docker, Prometheus, dan Grafana

Proyek belajar membangun stack monitoring berbasis pull dari nol, sebagai
bagian dari perjalanan memperkuat jalur IT Application Support dan IT
Operations. Lab ini menjalankan sebuah aplikasi dummy yang mengekspos metrik,
lalu memantau metrik itu dengan Prometheus, dan memvisualkannya di Grafana,
semuanya di dalam Docker.

## Arsitektur

Aplikasi dummy mengekspos metrik di endpoint /metrics. Prometheus secara
terjadwal menarik (scrape) metrik itu dan menyimpannya sebagai time series.
Grafana membaca data dari Prometheus dan menampilkannya sebagai dashboard.

Grafana  ->  Prometheus  ->  Aplikasi dummy (/metrics)

## Komponen

- app/ Aplikasi dummy berbasis Python Flask, terinstrumentasi dengan
  prometheus_client, mengekspos metrik app_requests_total di /metrics.
- prometheus/prometheus.yml Konfigurasi Prometheus, men-scrape aplikasi
  di alamat app:8000 setiap 15 detik.
- grafana/dashboards/dummy-app.json Ekspor dashboard Grafana agar dapat
  diimpor ulang.
- docker-compose.yml Orkestrasi ketiga service dalam satu jaringan.
- automate.sh Skrip bash untuk menyalakan seluruh stack dengan satu perintah.

## Cara menjalankan

Prasyarat: Docker dan Docker Compose terpasang.

  git clone <url-repo-ini>
  cd lab-01
  ./automate.sh

Lalu buka di browser:

- Aplikasi: http://localhost:8000/
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (login awal admin / admin)

Untuk dashboard Grafana, impor manual berkas grafana/dashboards/dummy-app.json
lewat menu Import di Grafana, lalu pilih Prometheus sebagai data source.

## Konsep yang dipelajari

- Model pull pada Prometheus dan perbedaannya dengan model push pada ELK.
- Perbedaan metrik tunggal dan time series.
- Peran label dalam membentuk identitas time series.
- Jaringan antar container pada Docker Compose (memanggil service lewat namanya).
- Perbedaan bind mount dan named volume.

## Batasan dan kejujuran

Proyek ini adalah lab belajar, bukan sistem production. Yang belum tercakup:

- Belum ada alerting.
- Belum ada penyimpanan metrik jangka panjang.
- Belum ada pengamanan (Prometheus dan Grafana berjalan tanpa hardening).
- Aplikasi yang dipantau adalah aplikasi dummy, bukan layanan nyata.
- Impor dashboard Grafana masih manual, belum otomatis via provisioning.

Hal hal di atas akan dibahas pada lab lab berikutnya.
