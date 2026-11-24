# PLAN: satu lembar per solusi alternatif (tabel teknis dan grafik pengurangan emisi)

Status: rencana, belum dikerjakan. Disusun 24 Nov 2026. Menunggu persetujuan pengguna.

## 1. Permintaan dan aturan

- Setiap solusi alternatif mendapat lembar sendiri yang memuat tabel parameter teknis dan grafik.
- Setiap grafik wajib menampilkan pengurangan emisi (MtCO2e per tahun).
- Semua angka bersumber. Tidak ada proyeksi statistik buatan sendiri. Hanya hitungan sederhana: kali, bagi, jumlah, konversi satuan, persen.
- Aturan tetap: grafik garis saja; tanpa freeze pane; tanpa tanda pisah panjang; Indonesia PUEBI; status T/P/R/D/E/AC/A; sumber pihak ketiga tidak dijumlahkan dengan CM1 atau CM2 resmi; D_Model_v21 tidak diubah; edit lewat XML, bukan simpan ulang LibreOffice atau openpyxl.

## 2. Batas hitungan yang diizinkan

Diizinkan: pengurangan = kapasitas atau luas bersumber x faktor kapasitas bersumber x faktor emisi bersumber (dengan konversi satuan); jumlah, selisih, rasio terhadap selisih 2030.
Tidak diizinkan: regresi, ekstrapolasi, interpolasi antar tahun di luar titik bersumber, kurva belajar, ukuran solusi "sebesar sisa selisih".
Akibat langsung: **Surya PV B7 (61,4 Mt) sekarang berupa sisa selisih, bukan angka bersumber.** Lembarnya harus memakai kapasitas surya bersumber (misalnya rencana RUPTL atau IEEFA) dikali faktor kapasitas dan faktor emisi, dan sisa selisih dipindah ke baris "selisih yang belum tertutup".
Titik data yang tidak ada ditulis kosong (#N/A untuk celah garis), bukan diisi.

## 3. Cakupan solusi (kandidat 41 opsi, dari D_Teknis_Opsi dan C_Solusi_2030)

Gelombang 1: opsi yang sudah punya nilai pengurangan di C_Solusi_2030.
- Energi: EBT RUPTL (surya, panas bumi, angin, hidro, bioenergi dirinci bila sumber memungkinkan), efisiensi energi, B40, co-firing biomassa, pensiun dini PLTU (dua bagian), gas suar, CCS PLTU TJB.
- FOLU: tata air gambut, penghindaran degradasi dan deforestasi gambut, restorasi gambut, pengelolaan hutan lestari, penghindaran degradasi dan deforestasi hutan mineral, rehabilitasi tanpa dan dengan rotasi, hutan tanaman.
Gelombang 2: opsi yang punya parameter teknis tetapi belum punya nilai pengurangan: nuklir, angin laut, surya atap dan terapung, PLTA dan mini hidro, baterai, BEV, angkutan umum, industri (semen, baja, amonia, metanol, olefin, CCS industri, efisiensi industri, captive nikel), LPG ke induksi, rice cooker, sawah AWD, PLTSa, mangrove.
Aturan masuk: sebuah opsi hanya mendapat lembar bila memiliki, dari sumber, (a) skala yang direncanakan atau potensi, dan (b) faktor emisi atau pengurangan yang dilaporkan. Bila tidak, opsi dicatat di `S_Ringkasan` dengan alasan dan masuk `RESEARCH_TODO.md`, tanpa grafik kosong.

## 4. Templat satu lembar (tetap sama untuk semua opsi)

Nama lembar `S_<opsi>` (awalan S_ baru, warna tab baru), judul "Lembar n. ...", tabel "Tabel n.X.", grafik "Gambar n.m.".

- **Tabel X.A Ringkasan opsi**: sektor, lapis (A dalam CM1 atau B di atas garis dasar), status, pengurangan 2030 rendah dan tinggi, persen dari selisih 2030, tautan ke baris C_Solusi_2030.
- **Tabel X.B Parameter teknis**: tarik dengan rumus dari `D_Teknis_Opsi` (kelas: potensi, skala, kinerja, faktor emisi, umur, kendala, status penerapan), setiap baris dengan status dan sumber. Tidak ada angka baru yang diketik tanpa sumber.
- **Tabel X.C Rantai hitung pengurangan emisi**: langkah demi langkah, satu operasi per baris (kapasitas, faktor kapasitas, jam, faktor emisi, hasil), semua masukan menunjuk sel sumber.
- **Tabel X.D Deret tahunan bersumber**: dari `C_Deret_Opsi` dan `D_*` (hanya titik yang ada di dokumen; sisanya #N/A).
- **Tabel X.E Celah data**: parameter yang belum ada, dengan nomor R di RESEARCH_TODO.md.
- **Grafik (garis saja)**, selalu dengan sumbu Y pengurangan emisi:
  1. Pengurangan emisi per tahun menurut tiap sumber (resmi, RUPTL, pihak ketiga) dibanding garis selisih 2030.
  2. Pengurangan emisi terhadap pendorong teknis (kapasitas GW atau luas Mha), titik dari skenario bersumber ditambah garis hitung sederhana kapasitas x faktor (dua titik, tanpa kurva).
  3. Bila tersedia: pengurangan emisi kumulatif terhadap selisih CPOS ke LCCP_L.
- **Catatan** sumber dan keterbatasan, status campuran ditandai (E tidak dijumlahkan dengan P atau T).

Lembar `S_Ringkasan` (satu tabel semua opsi: pengurangan, persen dari selisih, kesiapan data, tautan) dan entri Indeks, A_Audit, Q_Cek.

## 5. Cara membangun (aman bagi grafik)

1. Skrip Python membuat XML lembar dengan id gaya yang sudah ada di workbook, rumus menunjuk lembar D_ dan C_, nilai cache dihitung di skrip.
2. XML grafik dibuat dari templat grafik asli (gaya grafik garis yang sudah ada di master), bukan hasil simpan LibreOffice; bagian drawing, rels, dan content types ditambahkan langsung ke paket.
3. Tidak menyentuh D_Model_v21 dan lembar yang ada; hanya menambah lembar, baris Indeks, dan baris Q_Cek.
4. Skrip disimpan di `scripts/` dan dijalankan ulang bila data berubah.

## 6. Tahapan

- **Tahap 0, audit kesiapan (tanpa mengubah workbook)**: per opsi, cek apakah skala dan faktor emisi bersumber ada. Keluaran: tabel kesiapan (siap, kurang satu masukan, belum bisa) dan daftar riset tambahan.
- **Tahap 1, templat dan satu lembar contoh** (usul: Panas bumi) untuk persetujuan bentuk tabel dan grafik.
- **Tahap 2, gelombang 1**: semua opsi energi dan FOLU yang siap.
- **Tahap 3, S_Ringkasan, Indeks, Q_Cek**: uji otomatis (lihat bagian 7).
- **Tahap 4, gelombang 2**, setelah riset mengisi celah.

## 7. Pengendalian mutu

- Uji silsilah: setiap sel angka di lembar S_ adalah rumus ke sel sumber atau nilai bersumber berlabel status dan sumber; skrip menandai sel angka yang diketik tanpa label.
- Uji penjumlahan: jumlah pengurangan per lapis sama dengan C_Solusi_2030; opsi status E tidak masuk jumlah resmi.
- Uji grafik: setiap grafik punya deret pengurangan emisi, tiap deret punya data numerik, legenda tidak merujuk Indeks!B1; render LibreOffice untuk melihat bentuk; peringatan bahwa Excel tidak dapat diuji di lingkungan ini.
- Tanpa pane, tanpa tanda pisah panjang, 0 galat rumus, jumlah grafik lama tetap 173.

## 8. Risiko

- Banyak opsi gelombang 2 belum punya pengurangan bersumber; lembarnya akan menunggu riset (jangan diisi angka sendiri).
- Beberapa nilai di D_Teknis_Opsi berasal dari gambar tabel yang dibaca visual (status E); lembar menampilkan status itu.
- Grafik buatan XML tidak dapat diuji di Excel di sini; kemungkinan perlu satu putaran perbaikan setelah Anda membuka berkasnya.

## 9. Keputusan pengguna (24 Nov 2026) dan pembaruan rencana

- Cakupan: semua solusi alternatif yang sudah ada di workbook (C_Solusi_2030 dan D_Teknis_Opsi), bukan daftar baru.
- Lembar dan grafik dibuat hanya sampai data kajian tersedia; solusi tanpa data bersumber menunggu (lihat AUDIT_Kesiapan_Solusi.md dan RESEARCH_TODO.md).
- Tahap 0 selesai: `A_Kesiapan_Solusi` (Lembar 97): 51 baris; siap 18, siap setelah hitung ulang 1, kurang masukan 18, belum bisa 7, pendukung 1, pembanding 3, bukan solusi 3. Penilaian sebagian bersifat pertimbangan dari katalog data; diverifikasi ulang pada Tahap 1 untuk setiap solusi yang dibangun.
- Standar tampilan wajib untuk setiap lembar dan grafik: rapi dan seragam; tanpa grafik rusak; grafik rinci dengan area berarsir (selisih atau rentang, memakai area bertumpuk dengan deret dasar tanpa isi dan entri legenda dasar dihapus serta nama dasar dikosongkan, agar legenda tidak menampilkan "base"); legenda tepat sama dengan nama deret dan status sumber; label angka pada setiap titik data; sumbu dan satuan jelas; setiap grafik memuat pengurangan emisi.
- Langkah berikutnya: Tahap 1, satu lembar contoh (Panas bumi), untuk disetujui sebelum gelombang 1.
