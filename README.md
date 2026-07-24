# Lab 3: Containerisasi yang Lebih Benar

Kelanjutan dari Lab 2. Stack monitoring dan logging tetap sama, tetapi container
aplikasi dinaikkan kualitasnya dari sekadar berjalan menjadi dikerjakan dengan
praktik yang benar. Fokus lab ini bukan menambah komponen, melainkan memperbaiki
cara aplikasi dikemas dan dijalankan.

## Lima perbaikan yang dikerjakan

1. **Versi pustaka dikunci.** requirements.txt memakai tanda == dengan nomor versi
   pasti, demi keterulangan. Build kapan pun dan di mana pun menghasilkan versi
   pustaka yang sama.
2. **Server production menggantikan server pengembangan.** Flask development server
   diganti Gunicorn dengan dua worker. Flask sendiri memperingatkan servernya tidak
   untuk production.
3. **Container berjalan sebagai non-root.** Dibuat pengguna appuser, folder kerja dan
   folder log diserahkan kepadanya, lalu proses beralih ke pengguna itu. Prinsip
   least privilege, memberi hak sekecil mungkin yang cukup untuk bekerja.
4. **.dockerignore ditambahkan.** Membatasi apa yang ikut ke build context, agar build
   lebih bersih dan file tak semestinya tidak masuk ke image.
5. **HEALTHCHECK ditambahkan.** Docker rutin mengetuk endpoint aplikasi untuk menilai
   apakah layanan benar benar sehat, bukan sekadar prosesnya masih hidup.

## Temuan tambahan: metrik pada aplikasi multi worker

Setelah beralih ke Gunicorn dengan dua worker, metrik app_requests_total menjadi
tidak akurat. Penyebabnya, tiap worker adalah proses terpisah dengan memori sendiri,
sehingga masing masing menyimpan penghitungnya sendiri. Endpoint /metrics yang
dilayani satu worker hanya melaporkan angka milik worker itu.

Solusinya memakai mode multiproses prometheus_client. Tiap worker menulis metriknya
ke folder bersama (PROMETHEUS_MULTIPROC_DIR), lalu endpoint /metrics membaca seluruh
berkas di folder itu dan menjumlahkannya. Berkas gunicorn.conf.py menambahkan kait
child_exit agar jejak worker yang berhenti dibersihkan, sehingga totalnya tetap akurat.

Catatan menarik: log tidak mengalami masalah ini karena ditulis ke file di disk yang
dibagi bersama, sedangkan metrik disimpan di memori proses yang tidak dibagi.

## Cara menjalankan

    git clone <url-repo-ini>
    cd lab-03
    docker compose up -d --build

Lalu buka di browser:

- Aplikasi: http://localhost:8000/
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (login awal admin / admin)
- Kibana: http://localhost:5601

Verifikasi container yang sudah diperketat:

    docker compose ps                          # STATUS menampilkan (healthy)
    docker compose exec app whoami             # menjawab appuser, bukan root
    docker compose exec app ls -la /logs       # app.log dimiliki appuser
    curl -s http://localhost:8000/metrics | grep app_requests_total

## Konsep yang dipelajari

- Beda server pengembangan dan server WSGI production, serta arti app:app pada
  Gunicorn (nama modul di depan, nama objek di belakang).
- Prinsip least privilege pada container, dan konsekuensinya terhadap izin file.
- Named volume mewarisi kepemilikan dari folder di image saat volume masih kosong.
- Keterulangan lewat penguncian versi, berbeda dari pemisahan lewat environment.
- Beda "proses hidup" dan "layanan sehat", yang dijembatani HEALTHCHECK.
- Metrik berbasis memori tidak otomatis akurat pada aplikasi multi proses.

## Batasan dan kejujuran

Proyek ini adalah lab belajar, bukan sistem production. Yang belum tercakup:

- Keamanan Elasticsearch masih dimatikan, warisan dari Lab 2, hanya untuk belajar.
- Belum ada CI/CD, pemisahan environment, maupun alerting.
- Image belum dioptimalkan lebih jauh, misalnya multi-stage build.
- Belum ada pembatasan sumber daya per container di level Compose.
- Aplikasi yang dipantau tetap aplikasi dummy, bukan layanan nyata.

Hal hal di atas dibahas pada lab lab berikutnya.
