# Lab 2: Metrik dan Log, Menambah Pipeline ELK

Kelanjutan dari Lab 1. Selain memantau metrik dengan Prometheus dan Grafana,
lab ini menambahkan pipeline log dengan ELK, yaitu Elasticsearch, Kibana, dan
Filebeat, semuanya di dalam Docker. Aplikasi dummy kini menulis log terstruktur,
Filebeat mendorongnya ke Elasticsearch, dan Kibana menampilkannya.

## Arsitektur

Dua pipeline berdampingan.

Metrik (model pull): Aplikasi mengekspos /metrics, Prometheus men-scrape secara
terjadwal, Grafana memvisualkan.

Log (model push): Aplikasi menulis log JSON ke file di volume bersama, Filebeat
membacanya lalu mendorong ke Elasticsearch, Kibana menampilkan dan menyaring.

## Komponen baru di Lab 2

- app/app.py Ditambah structured logging, menulis log JSON per baris ke /logs/app.log.
- filebeat/filebeat.yml Konfigurasi Filebeat, membaca /logs/app.log dengan parser
  ndjson, lalu output ke Elasticsearch.
- Service elasticsearch, kibana, dan filebeat di docker-compose.yml.
- Volume bersama logs untuk menjembatani aplikasi dan Filebeat.

## Cara menjalankan

Prasyarat: Docker dan Docker Compose terpasang, serta vm.max_map_count minimal
262144 (di banyak sistem Linux nilai ini sudah memadai secara bawaan).

    git clone <url-repo-ini>
    cd lab-02
    docker compose up -d --build

Lalu buka di browser:

- Aplikasi: http://localhost:8000/
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (login awal admin / admin)
- Kibana: http://localhost:5601

Di Kibana, buka Discover, buat data view dengan pola indeks filebeat-* dan
timestamp field @timestamp, lalu perluas rentang waktu untuk melihat log.

## Konsep yang dipelajari

- Beda peran metrik dan log, dan pasangannya masing masing (Prometheus-Grafana,
  Elasticsearch-Kibana).
- Elasticsearch sebagai mesin penyimpan dan pencari, Kibana sebagai penampil.
- Structured logging dengan JSON, dan parser ndjson pada Filebeat.
- Filebeat sebagai pengirim log, wujud nyata model push.
- API HTTP sebagai loket bersama tempat Filebeat, curl, dan Kibana menghubungi
  Elasticsearch.

## Batasan dan kejujuran

Proyek ini adalah lab belajar, bukan sistem production. Yang belum tercakup:

- Keamanan Elasticsearch sengaja dimatikan (xpack.security.enabled=false) untuk
  menyederhanakan setup lokal. Ini TIDAK boleh dipakai di production, yang wajib
  memakai autentikasi dan enkripsi.
- Belum ada Logstash. Log langsung dari Filebeat ke Elasticsearch, memungkinkan
  karena log sudah terstruktur JSON. Logstash dibutuhkan saat log belum
  terstruktur dan perlu diurai lebih dulu.
- Belum ada alerting maupun dashboard log.
- Data view Kibana masih dibuat manual, belum otomatis via provisioning.
- Aplikasi yang dipantau adalah dummy, bukan layanan nyata.

Hal hal di atas dibahas pada lab lab berikutnya.
