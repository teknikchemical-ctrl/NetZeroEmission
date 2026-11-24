# PLAN: model portofolio solusi menuju net zero (24 Nov 2026)

Status: rencana, menunggu persetujuan. Menggantikan urutan kerja di PLAN_Sheet_Per_Solusi.md (lembar per solusi menjadi bagian lapis 4 di bawah).

## 1. Tujuan akhir (disepakati dengan pengguna)

Studi ini menyambung studi mapan yang sudah ada. Keluaran akhir: portofolio solusi dan solusi kumulatif yang menyelaraskan kita menuju net zero, dengan tabel utama dan grafik yang menunjukkan, per solusi dan kumulatif: pelaksanaan, biaya, investasi, pengurangan emisi, dan persen selisih yang tertutup.

- Target: jalur LCCP_L (SNDC), karena paling mapan.
- Garis pembangunan (development) tidak tetap: dibangun dari rencana, rencana pelaksanaan, dan kebijakan yang berlaku. Setiap rencana menghasilkan emisi lewat aktivitas x faktor emisi, dan emisi itu menjauhkan kita dari jalur net zero.
- Selisih = garis pembangunan dikurangi jalur LCCP_L. Selisih diurai menurut penyebab (pendorong).
- Hanya data bersumber dan hitungan sederhana. Tanpa proyeksi statistik. Biaya saja. Resmi dahulu, sisanya berlabel. Sumber pihak ketiga tidak dijumlahkan dengan CM1 atau CM2.

## 2. Celah riset inti (urut menurut penghambatan model)

### P1: menghambat rancangan model
| Kode | Celah | Yang dicari |
|---|---|---|
| G1 | Pendorong garis pembangunan, listrik | Daftar PLTU yang sedang dibangun dan direncanakan (14,9 GW dalam konstruksi per Squire), PLTU captive (17,7 GW, 127 unit 2030) per unit dengan status dan tahun operasi, tambahan fosil RUPTL per tahun, jalur permintaan RUKN, faktor pemanfaatan |
| G2 | Pendorong garis pembangunan, lahan | Konversi lahan yang sudah berizin atau direncanakan: kuota deforestasi terencana (D_Aksi sudah ada), izin HGU, PBPH-HT, tambang di kawasan hutan, food estate, perkebunan energi (5,4 juta ha kawasan dicadangkan per Squire), laju deforestasi Renstra |
| G4 | Kalibrasi pelaksanaan | Rencana dibanding capaian historis untuk tiap pendorong dan tiap solusi (tambahan EBT terhadap RUPTL, COD PLTU, deforestasi terhadap kuota, restorasi gambut, B40, EV) untuk faktor pelaksanaan bersumber |
| G5 | Jalur NZE per subsektor dan per tahun | LCCP_L hanya tingkat sektor pada tahun 2019, 2025, 2030, 2035, 2060; cari asumsi subsektor (LTS-LCCR, lampiran SNDC, Bappenas) agar pendorong dapat ditempatkan terhadap jalur |
| G11 | Konkordansi studi mapan | Angka jalur, potensi, dan biaya per solusi dari studi utama (LTS-LCCR, SNDC 2025, BTR, Bappenas, IEA, IESR, JETP CIPP, Bank Dunia CCDR, RUKN, RUPTL, IEEFA, Rossita dan Boer, makalah yang sudah dicatat). Daftar studi di luar repo berasal dari pengetahuan umum dan wajib diverifikasi |

### P2: menghambat solusi dan portofolio
| Kode | Celah | Yang dicari |
|---|---|---|
| G6 | Deret subsektor inventaris | Inventaris resmi energi per subkategori (pembangkit, industri, transportasi, fugitive) 2000 sampai 2024 untuk mencocokkan emisi pendorong dan menghindari hitung ganda |
| G7 | Parameter per solusi | Lihat DATA_NEEDS_PER_SOLUSI.md bagian A |
| G8 | Hubungan antar solusi | Aturan tumpang tindih (pensiun, CCS, co-firing, efisiensi terhadap kebutuhan pasokan) dan perubahan faktor emisi jaringan menurut tahun (0,87 menjadi 0,788, 0,445, 0,282) |
| G9 | Batas laju pembangunan | Laju maksimum yang pernah tercapai (GW surya per tahun, panas bumi, pensiun PLTU, ha tanam per tahun, penjualan EV) sebagai batas per tahun |
| G10 | Biaya dan jadwal investasi | Lama bangun per teknologi, jadwal belanja modal, biaya program FOLU, harga bahan bakar, tingkat diskonto (6 atau 9 persen) |

### P3
| Kode | Celah | Yang dicari |
|---|---|---|
| G3 | Pendorong energi non-listrik | Rencana kapasitas industri (smelter, semen, baja, pupuk), pertumbuhan armada, produksi batubara dan migas (RKAB), faktor emisi per aktivitas |
| G12 | Jalur 2060 | Jalur resmi atau mapan 2060 per sektor |
| G13 | Lingkup | Limbah (selisih 2060 sebesar 371 Mt), pertanian, IPPU |

## 3. Rancangan model (lima lapis, satu arah aliran)

Lapis 1, masukan: lembar D_ yang ada (tidak diubah; D_Model_v21 tidak pernah diubah).
Lapis 2, garis pembangunan dari bawah ke atas:
- `B_Pendorong`: satu baris per pendorong (misalnya tambahan PLTU RUPTL, PLTU captive, deforestasi terencana). Kolom: sektor SNDC, subkategori inventaris, aktivitas dan satuan, sumber rencana, jadwal (hanya titik bersumber), faktor emisi, emisi = aktivitas x faktor (rumus), faktor pelaksanaan bersumber, status.
- `B_Garis_Pembangunan`: jumlah pendorong per sektor dan tahun, dibandingkan dengan CPOS (SNDC), model v2.1, dan inventaris; selisih antar garis dicatat sebagai temuan.
Lapis 3, jalur dan selisih:
- `B_Garis_NZE`: LCCP_L pada tahun bersumber.
- `B_Selisih_Penyebab`: selisih per sektor dan per pendorong.
Lapis 4, solusi (satu lembar per solusi, templat dari PLAN_Sheet_Per_Solusi.md): rantai hitung S x F x D, biaya, investasi, deret tahunan bersumber, grafik. Setiap lembar menghasilkan blok keluaran baku: pendorong yang dituju, tahun mulai, investasi, biaya tahunan, pengurangan per tahun pada potensi dan pada pelaksanaan saat ini, status.
Lapis 5, portofolio:
- `P_Portofolio`: tabel utama (solusi, pendorong, tahun, investasi USD, biaya tahunan, MtCO2e per tahun, persen selisih, kumulatif persen, pelaksanaan saat ini, pengurangan pada pelaksanaan saat ini, status).
- `G_Portofolio`: grafik garis; selisih sebagai area berarsir; deret kumulatif potensi dan pada pelaksanaan saat ini; investasi kumulatif; kurva biaya; label angka pada tiap titik.
- `Q_Portofolio`: uji tanpa hitung ganda, jumlah sama dengan lapis, label status.
- `K_Studi`: matriks konkordansi per solusi lintas studi mapan.

Prinsip: setiap solusi bekerja pada pendorong tertentu, jadi mengubah aktivitas (bukan sekadar mengurangi angka). Dua bagian portofolio: (1) mengirim CM1 yang belum terlaksana, (2) solusi baru di atas CM1 dan CM2.

## 4. Pemakaian ulang dan audit lembar yang ada

Dapat dipakai ulang: C_Listrik_Rencana, C_Pembangkit, C_Jalur_NZE, C_Phasedown_Unit dan R_Unit_Skor, C_FOLU_Rencana, D_Aksi, D_Rencana, D_Kenyataan, C_Solusi_2030, C_Biaya_Teknologi.
Perlu diaudit terhadap aturan "tanpa proyeksi sendiri": C_Jalur_Sektor memakai garis lurus dari 2024 ke 2060 (diberi label A), C_FOLU_Rencana dan P_Selisih_Rencana dan C_Dampak berlabel "bergantung asumsi", C_Jalur_NZE memakai jalur lurus. Tiap lembar dipertahankan, diberi label jelas, atau diganti dengan titik bersumber.

## 5. Tahapan

1. Desain: tabel pemetaan pendorong ke kategori inventaris ke sektor SNDC; sumbu tahun (tahun bersumber saja); aturan tumpang tindih. Hasil: dokumen desain dan persetujuan.
2. Garis pembangunan listrik dan FOLU (data paling lengkap): B_Pendorong, B_Garis_Pembangunan, rekonsiliasi dengan CPOS dan model v2.1.
3. Selisih menurut penyebab 2030 (B_Garis_NZE, B_Selisih_Penyebab).
4. Lembar solusi gelombang 1 (contoh pertama: panas bumi), lalu energi dan FOLU yang siap menurut audit.
5. Portofolio, grafik, uji (P_, G_, Q_Portofolio).
6. Konkordansi studi mapan (K_Studi) dan validasi; jalur 2060 dari jalur model terbit; putaran perbaikan setelah dibuka di Excel.
Riset G1, G2, G4, G5, G11 berjalan paralel dengan tahap 1 sampai 3.

## 6. Standar mutu

Rapi dan seragam; grafik garis dengan area berarsir, legenda tepat, label angka pada titik, tanpa entri legenda "base" (deret dasar tanpa isi, nama kosong); tanpa freeze pane; tanpa tanda pisah panjang; 0 galat rumus; setiap angka berlabel status dan sumber; XML langsung, bukan simpan ulang LibreOffice; sumber pihak ketiga tidak dijumlahkan dengan CM1 atau CM2.

## 7. Risiko

- Data pendorong bisa tidak berada pada tingkat unit atau spasial yang dibutuhkan (G1, G2).
- Faktor pelaksanaan dari riwayat singkat bisa terlalu kasar; dilabel bila tidak cukup.
- Grafik buatan XML tidak dapat diuji di Excel di sini; perlu putaran perbaikan.
- Daftar studi mapan di luar repo berasal dari pengetahuan umum; setiap angka harus diverifikasi sebelum masuk model.

## 8. Status pembangunan (24 Nov 2026)

Tahap 1 sampai 5 dibangun: lembar 98 sampai 127 (lihat HANDOFF Addendum 6). Belum dibangun: lembar solusi efisiensi energi, gas suar, transportasi, industri, minyak dan gas, terbarukan terukur riil (menunggu WP-D), garis pembangunan non-listrik (WP-A, C, E, I), jalur 2060 per solusi (WP-L). Lembar pelaksanaan (Tabel G pada lembar terbarukan, Tabel E pada lembar tunggal) disediakan kosong untuk diisi tim.
