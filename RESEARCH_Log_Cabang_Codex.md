# Log penelanan cabang `research/nze-data-handoff` (commit 7139bd6)

Tanggal penelanan: 24 November 2026. Cabang tim dibuat dari commit lama ce2d199 (sebelum model), sehingga tidak digabung utuh (akan menghidupkan kembali berkas xlsx lama). Yang dilakukan adalah impor selektif, pencatatan, dan pemeriksaan silang.

## 1. Yang diimpor
| Isi | Lokasi di repo | Catatan |
|---|---|---|
| Catatan serah terima, cek arsip, ringkasan riset | `SERAH_TERIMA_RISET_TIM_2026-11-24.md`, `CEK_ARSIP_SUMBER_2026-11-24.md`, `RESEARCH_NZE_2026-11-24.md` | Berkas tim, tidak diubah |
| Templat terisi tim | `templates/TEMPLATE_Catat_Data_terisi_codex.xlsx` | Templat kosong milik kami tetap `TEMPLATE_Catat_Data.xlsx` |
| 34 makalah kebijakan, hukum, pasar karbon, FOLU, nuklir, JETP | `papers/` | Semua dibaca (teks diekstrak) |
| 9 PDF sumber yang sebelumnya hanya berupa transkripsi | `sources/` | IEEFA, ERIA, Zain, Zahari, Hilmiyati, Sijabat, Murdiyarso, Hermudananto, Renops; 4 berkas lain identik (SHA-256) dengan yang sudah ada dan dilewati |
| Dua CSV penulis Squire | `sources/2024_Squire-dkk_*.csv` | Deret emisi skenario dan biomassa per provinsi |

## 2. Pemeriksaan silang (angka register terhadap PDF asli)
`scripts/verify_all_sources.py` kini mencakup 27 dokumen. Dari sekitar 700 butir berangka yang dapat diperiksa, hanya 5 tidak ditemukan sebagai teks: tabel gambar Cahyo (2), tabel gambar Sijabat (2; dibaca mata langsung dari gambar dan cocok: 1,36; 1,97; 0,0947; 0,0561; 0,0474), satu nilai turunan TIMES (873), satu turunan ERIA (131,3 = 1.706,7 dibagi 13). Tidak ada nilai register yang salah.

## 3. Yang baru dicatat ke model
- Register D_Register_Sumber: 842 menjadi 866 butir, 29 menjadi 43 dokumen (skrip `scripts/16_log_codex_branch.py`; tiap angka diperiksa terhadap teks PDF atau CSV sebelum ditulis, mode `--strict`).
- K_Konflik K147 sampai K153 (7 konflik baru), lihat bagian 4.
- S_Cofiring: deret skenario Squire 2030 dan pengurangan Rendah 14,19; Setara 40,96; Menengah 57,97; Tinggi 152,51 MtCO2 per tahun (sebelumnya hanya Rendah dan Tinggi). Jumlah 34 provinsi biomassa = 504,40 miliar MJ, cocok dengan 504,4 pada Tabel 1 (pasokan tervalidasi dua arah).
- S_CCS_TJB: emisi unit 5 dan 6 (9,404) terhadap tangkapan 13 Mt (rasio 1,38) dan biaya dikoreksi 63,7 sampai 72,4.

Dari 1.164 baris templat tim, 1.088 adalah transkripsi workbook lama (sudah ada), 55 baris CSV Squire (kini dicatat), 5 baris migas kosong (WP-C), selebihnya hitungan kecil yang sudah ada padanannya.

## 4. Temuan penting dari penelanan
1. **K147, kesalahan biaya CCS.** Rentang 63,7 sampai 92,6 USD per tCO2 dipakai untuk 13 Mt (dua unit). Menurut ERIA Tabel 5.11 dan 5.12, 92,6 adalah kasus SATU unit 6,5 Mt dengan pipa. Untuk dua unit 13 Mt: 63,7 (kapal dan pipa darat) sampai 72,4 (pipa). Dampak bila dikoreksi: biaya tahunan tinggi 1.204 menjadi 941 USD juta, biaya tengah 1.016 menjadi 885. Belum diubah pada tabel judul (D_Opsi_Solusi baris 205, C_Solusi_2030 H34, P_Portofolio); menunggu keputusan karena nilai berantai ke banyak lembar. Koreksi sudah tersedia sebagai sensitivitas di S_CCS_TJB.
2. **K150.** Tangkapan kotor ERIA 13 Mt lebih besar daripada emisi estimasi unit 5 dan 6 (9,404 Mt, Prabowo dan Dalimi dari GEM). Asumsi pemanfaatan dan bahan bakar perlu diseragamkan sebelum 13 Mt dipakai sebagai pengurangan.
3. **K148.** Emisi PLTU 2030: Squire BAU 369,5 lebih tinggi dari RUPTL 354 (RE Base) dan 348 (ARED).
4. **K149.** Biaya restorasi gambut: Renops 2025 sampai 2030 USD 400 per ha dibanding Rossita dan Boer swasta USD 584 sampai 670 per ha (cakupan biaya berbeda).
5. **K151 sampai K153**: efisiensi 30 dibanding 31,87 Mt; ketidakkonsistenan internal makalah Prabowo dan Dalimi (12.645 dibanding 14.545 MW); tiga batas biaya mangrove (USD 1.524; 1.870; 3.863 per ha).
6. Temuan lama yang dikonfirmasi tim: B40 tersirat 2,658 kg per liter B100 (sudah ada di D_Solusi_Kuantif baris 68); TJB unit 5 dan 6 beririsan dengan pensiun dini (sudah ada di S_CCS_TJB).

## 5. Pernyataan tim yang tidak dapat dipenuhi dari repo ini
- Nomor baris yang dirujuk tim (mis. D_Register_Sumber baris 474 atau D_Opsi_Solusi baris 172) merujuk workbook lama; nomor di workbook terbaru berbeda. Gunakan nama butir, bukan nomor baris.
- Tim tidak menemukan butir 742 sampai 836 dan K125 sampai K141; semuanya ada di workbook terbaru (register 866 butir).
- Akses ESDM, UNFCCC, SKK Migas, GEM masih HTTP 403 bagi tim. Verifikasi resmi migas dan proyek EBT, serta pemeriksaan kedua 20 persen, masih tertunda (WP-C, WP-D, WP-M).

## 6. Usulan pengembangan berikutnya
1. Putuskan koreksi K147 (disarankan: ubah batas atas menjadi 72,4 dan hitung ulang seluruh rantai biaya).
2. Pisahkan cabang portofolio pensiun dini unit TJB 5 dan 6 dibanding retrofit CCS agar tidak dihitung ganda (K150).
3. Rekonsiliasi pengurangan CM2 FOLU per aksi dengan luas BTR-1 Tabel 2-28 dan 2-29 (luas CM1 ke CM2 sudah ada di D_Solusi_Resmi); sisa FOLU CM2 resmi 32,8 sampai 101,4 Mt tanpa alokasi aksi.
4. Selaraskan efisiensi: dapatkan tabel SRN dan POME ESDM untuk menjelaskan 30 dan 31,87 Mt (K151).
5. Baca 34 makalah di `papers/` untuk sembilan butir kebijakan yang masih tidak numerik; hanya angka bersumber yang dicatat (tidak ada angka baru yang dijumlahkan dengan CM1 atau CM2).
6. Migas (WP-C): lima baris masih kosong; tidak ada data bersumber untuk metana, venting, dan CCS migas.

## 7. Tambahan: tiga unggahan baru di `main` (24 November 2026)
Saat penelanan berlangsung, `main` menerima tiga PDF. Semuanya dipindah ke `sources/`, dibaca, dan dicatat (skrip `scripts/17_log_main_uploads.py`, register 866 menjadi 882 butir, 43 menjadi 45 dokumen, K154 sampai K157).
- **Laporan pengungkapan iklim PLN 2024 (IFRS S2)**, `sources/2025_PLN_Laporan-Pengungkapan-Iklim-2024.pdf` (82 halaman): emisi PLN menurut lingkup (276,56 Mt; PLTU milik PLN 125,1 Mt), jalur ARED (puncak 326 Mt pada 2030, nol pada 2060, tanpa pensiun dini), realisasi pengurangan 2024 (12,7 Mt; co-firing 1,8 Mt), konsumsi biomassa 1,62 juta ton, penundaan RUPTL EBT (25 persen dari 5,09 GW), studi CCS Indramayu 6,3 Mt per tahun pada 2040. Jalur ARED 326 Mt (2030) menambah satu titik pada K148 (RUPTL ARED 348, RE Base 354, Squire BAU 369,5).
- **Lanskap panas bumi Indonesia 2023 (Pambudi dan Ulfa 2024)**: potensi 29,5 GW, terpasang 2.356 MW (sekitar 8 persen), tambahan 2018 sampai 2022 sekitar 104 MW per tahun (AC); data laju historis untuk B6 panas bumi 3 GW.
- **Pensiun dini PLTU (Fadiilah dan Dye)**: salinan lain makalah yang sudah ada (teks sama, 54.761 karakter; 93,52 dan 14.310 cocok); disimpan sebagai `..._salinan_unggahan_main.pdf`, tidak dicatat ulang.

Cek silang bermanfaat: PLN melaporkan co-firing 1,8 MtCO2 (2024), sebanding dengan 1,57 Mt hasil S_Cofiring (14,3 persen kali target 11 Mt). Angka 44,1 Mt untuk Jawa 9 dan 10 di teks PLN tidak konsisten dengan totalnya (13,9) dan tidak dipakai (K157).

## 8. Tambahan: commit 07379a1 (batch 23 PDF, data padanan, lanjutan riset)
Diimpor: `CEK_BATCH_23_PDF`, `CEK_REFERENSI_NZE`, `LANJUTAN_RISET_PRIORITAS`, `data/` (padanan PLTU RUPTL dan GEM 18 unit, captive 7 unit, pipeline EBT 882 baris), 8 makalah di `papers/`, serta di `sources/`: laporan ETP/UNOPS 2023, CSV kompensasi 32 aset, Sugito (CCS), Usman (penyimpanan), Fitriana 2024 dan 2026, Cahyo (salinan), dan dua CSV OWID. Sembilan unggahan duplikat tidak dibawa. Dicatat lewat `scripts/18_log_codex_batch23.py` (register 882 menjadi 897 butir, 45 menjadi 55 dokumen, K158 sampai K162). Jumlah CSV kompensasi (11.757,36 dan 7.578,96) dan angka OWID dicek langsung; tabel gambar Cahyo dibaca mata (cocok dengan catatan tim).

Temuan baru:
1. **Biaya pensiun dini kemungkinan terlalu rendah (K158).** Model memakai USD 13,49 per tCO2 (UMD/IESR). ETP/UNOPS memberi USD 32 per tCO2e untuk Ombilin (140,8 juta per 4,4 Mt, 2,37 kali biaya model) dan IESR Cirebon-1 31 sampai 40. Kompensasi aset saja, belum biaya pengganti. Disarankan memakai rentang 13,5 sampai 40 pada B1 dan B4; belum diubah di judul.
2. **CCS (K159).** Biaya tangkap Sugito 51,8 USD per t (hanya tangkap, penalti daya 30,8 persen) dibanding komponen tangkap ERIA 30,5. Biaya per ton dihindari untuk Tanjung Jati B masih terbuka.
3. **K150 dipertajam.** Tanpa margin desain, tangkapan bruto ERIA 11,83 Mt, masih 1,26 kali emisi estimasi unit 5 dan 6 (9,404 Mt).
4. **Penyimpanan (K160)** dan **listrik 2060 (K161)**: Usman 680,57 Gt dibanding 572,77 Gt di workbook (kemungkinan tumpang tindih); Fitriana BAU 544 dan NZE 60 MtCO2 per tahun untuk pembangkitan saja.
5. Peringatan metode: Bhakti dkk. (ANFIS, akurasi 93,5 persen) tidak dipakai; konsisten dengan aturan tanpa proyeksi buatan sendiri.
6. Data padanan RUPTL-GEM menunjukkan Sumsel-1 600 MW (RUPTL) dibanding 700 MW (GEM) dan Sumut-1 ditangguhkan; berguna untuk garis dasar (B_Garis_Pembangunan), belum diproses lebih lanjut.

## 9. Pengembangan lembar data dan catatan per sumber (24 November 2026)
- **Induk sumber** (`D_Sumber`, Lembar 129): 85 sumber (83 berkas dan 2 sumber tanpa berkas), kedalaman baca A 45, B 23, C 17, 2 berkas duplikat isi. Catatan per sumber di `notes/sumber`, data register per sumber di `data/per_sumber` (lihat `notes/README.md`).
- **Data terstruktur** (`D_Data_Struktur`, Lembar 130): 548 angka satu per baris (Squire, OWID, ETP 32 aset, pipeline EBT RUPTL menurut jenis dan tahun COD, PLN, titik pembanding studi lain). Pemecahan 897 butir register yang masih bercampur dilakukan bertahap.
- **Grafik** (`G_Data_Sumber`, Lembar 131): 13 grafik garis berlabel: skenario co-firing dan pengurangannya terhadap BAU (berarsir), jalur ARED PLN, emisi dan realisasi pengurangan PLN, pembangkitan dan intensitas listrik nasional, produksi dan konsumsi migas, kompensasi pensiun ETP, tambahan kapasitas terbarukan RUPTL (RE Base dan ARED, berarsir; menurut teknologi), dan pembanding jalur emisi listrik antar studi.
- **Temuan baru K163:** pipeline proyek RUPTL memberi PLTS 4.679 MW (RE Base) dan 7.912 MW (ARED) pada 2025 sampai 2030, sedangkan agregat tercatat tim 2.596 dan 5.046 MW; perlu ditelusuri.
- Keterbatasan jujur: 23 sumber berkedalaman B dan 17 berkedalaman C belum dibaca penuh (di antaranya Riau 115 hlm., manual geospasial 68 hlm., Renops sebagian).
