# RENCANA RISET UNTUK TIM: melengkapi data sebelum model dibangun (24 Nov 2026)

Tujuan studi: menjadi studi yang menyambung studi mapan, dengan keluaran portofolio solusi dan solusi kumulatif menuju net zero (target LCCP_L), lengkap dengan pelaksanaan, biaya, investasi, pengurangan emisi, dan persen selisih. Garis pembangunan dibangun dari rencana dan kebijakan (aktivitas x faktor emisi). Lihat PLAN_Model_Portofolio.md.

Prinsip: semua data dipahami konteksnya dan dicatat; tidak ada angka tebakan; hanya hitungan sederhana; resmi dahulu; sumber lain berlabel E dan tidak dijumlahkan dengan CM1 atau CM2.

## 1. Kondisi saat ini (jujur, berdasarkan isi repo)

| Blok | Yang sudah ada | Status |
|---|---|---|
| Listrik batubara | RUPTL, GEM unit PLTU, emisi PLTU, urutan phase-down, biaya, faktor emisi 0,96 (rentang resmi 0,911 sampai 1,297) | Sebagian |
| **Minyak dan gas** | Hanya gas suar (potensi resmi 1,7 Mt), kapasitas gas dan LNG di RUPTL, satu catatan penyimpanan CO2 (akuifer). Tidak ada emisi hulu, tengah, hilir per aktivitas, tidak ada rencana produksi, tidak ada metana fugitive, tidak ada kilang | **Belum terukur** |
| **Energi terbarukan** | Tambahan RUPTL per jenis, faktor kapasitas, biaya modal, tiga model terbit. Belum ada: riwayat terpasang, status proyek (PPA, FID, COD), pengurangan per teknologi, faktor emisi jaringan per wilayah, kurtailmen, laju pelaksanaan. Surya masih berupa sisa selisih | **Belum terukur** |
| Batubara hulu | Produksi 2022 (kutipan), PLTU captive (kutipan) | Belum |
| Efisiensi, biofuel, transportasi, industri | Angka resmi tingkat program, B40, Jakarta, TIMES (PDF, belum diekstrak per teknologi) | Sebagian |
| FOLU | 11 aksi (luas dan faktor), BTR-1, FREL, Renops, biaya Rossita dan Boer | Sebagian, rincian CM2 195 Mt belum |
| Garis pembangunan dari bawah ke atas | Hanya bagian listrik batubara dan FOLU terencana | Sebagian |
| Konkordansi studi mapan | 28 dokumen tercatat (836 butir) | Sebagian |

## 2. Aturan pencatatan (wajib untuk semua anggota tim)

- Gunakan `templates/TEMPLATE_Catat_Data.xlsx` (satu baris satu angka). Kolom konteks wajib: cakupan dan batas, basis (tahun harga, diskonto, GWP), tahun data, skenario, posisi terhadap garis dasar (di dalam CPOS atau CM1, CM2, di atas), jenis sumber, cara perolehan, pertanyaan yang dijawab angka.
- Berkas sumber disimpan di `sources/` dengan nama TahunTerbit_Penerbit_JudulPendek.pdf.
- Nilai tidak ada: biarkan kosong, isi kolom celah. Dilarang menebak.
- Dua sumber berbeda: catat keduanya, isi kolom konflik; keputusan dibuat bersama (lihat K_Konflik).
- Angka dibaca dari gambar: cara perolehan "dibaca gambar", wajib diperiksa orang kedua.
- Pemeriksaan kedua oleh orang berbeda untuk setiap catatan; 20 persen sampel dicek ulang oleh pemimpin riset.
- Teks: Indonesia baku (PUEBI); tanpa tanda pisah panjang (em atau en dash).
- Pembagian kerja: Claude membaca dan mengekstrak PDF di repo serta memasukkan hasil ke workbook; tim mencari sumber di luar repo (portal resmi, permintaan data ke kementerian, wawancara, basis data) dan mengisi template.

## 3. Kelengkapan jenis studi (daftar periksa agar tidak ada yang terlewat)

Setiap blok (listrik, migas, terbarukan, batubara hulu, transportasi, industri, gedung, FOLU) diperiksa terhadap 13 jenis sumber: (1) inventaris dan pelaporan resmi, (2) target dan rencana resmi, (3) regulasi, (4) statistik resmi, (5) data utilitas dan perusahaan, (6) basis data proyek, (7) peta jalan lembaga internasional, (8) lembaga riset dan LSM, (9) model sistem energi terbit, (10) studi empiris dan LCA, (11) katalog biaya, (12) data spasial dan perizinan, (13) sumber faktor emisi. Tiap paket kerja di bawah mencantumkan jenis mana yang dicari. Matriks blok x jenis diisi tim pada hari pertama (status: ada, sebagian, belum).

## 4. Paket kerja

Ukuran: S sekitar satu sampai dua hari, M sekitar tiga sampai lima hari, L lebih dari satu minggu. Prioritas P1 menghambat model, P2 menghambat solusi dan portofolio, P3 pelengkap.

### WP-C Minyak dan gas (blok baru, P1)
Pertanyaan kunci: berapa emisi sektor minyak dan gas per aktivitas hari ini, ke mana arah menurut rencana (garis pembangunan), dan solusi apa yang menutup selisihnya?
Data yang dicari:
- Emisi per aktivitas: hulu (produksi, flaring, venting, fugitive), tengah (pemrosesan, LNG, pipa), hilir (kilang, distribusi), pembakaran sendiri. Kategori inventaris 1B2 dan 1A1 migas di inventaris KLH dan BTR.
- Rencana produksi dan proyek: lifting minyak dan gas, WP&B, proyek besar (LNG, pengembangan gas, RDMP kilang) beserta tahun onstream.
- Volume gas suar per lapangan dan faktor emisi; gas yang dibakar dan dimanfaatkan.
- Faktor emisi metana per aktivitas; potensi deteksi dan perbaikan kebocoran (LDAR), pemulihan venting, elektrifikasi hulu.
- Penggunaan gas: gas ke pembangkit, pupuk, industri; kebijakan alokasi dan harga gas.
- CCS atau CCUS: potensi penyimpanan (lapangan habis dan akuifer salin), proyek, regulasi (verifikasi nomor), biaya.
- Biaya: pemanfaatan gas suar, LDAR, pemulihan venting per ton CO2e.
Sumber (resmi dahulu): KLH inventaris dan BTR (1B2), SKK Migas, Ditjen Migas, KESDM Handbook of Energy and Economic Statistics, Pertamina laporan keberlanjutan, dokumen NDC dan LTS bagian energi; lalu IEA Methane Tracker dan studi Global Methane Pledge (verifikasi); jurnal.
Keluaran: baris di template; tabel emisi migas per aktivitas; daftar proyek bertanggal; opsi solusi dengan S, F, D, C.
Selesai bila: emisi migas hulu sampai hilir terpetakan ke kategori inventaris, ada rencana produksi bertahun, dan minimal tiga solusi memiliki skala dan faktor bersumber.
Ketergantungan: WP-G (kategori inventaris). Ukuran: L.

### WP-D Energi terbarukan, ukur lengkap per teknologi (blok baru, P1)
Pertanyaan kunci: berapa potensi, rencana, yang sudah terbangun, yang sedang dibangun, dan yang realistis per teknologi, dan berapa emisi yang digantikan di jaringan mana?
Teknologi: surya skala utilitas, atap, terapung; angin darat dan laut; PLTA besar, mini hidro, pompa air (PS); panas bumi; bioenergi (biomassa, biogas, POME, sampah); nuklir; arus laut; penyimpanan; transmisi dan interkoneksi.
Data per teknologi:
- Potensi sumber daya (resmi) dan potensi teknis; batas lahan dan hutan.
- Rencana: RUPTL 2025 sampai 2034 per jenis, per tahun, per sistem (Jawa-Bali, Sumatera, lainnya); RUKN; RUEN; JETP CIPP; pengadaan PLN.
- Riwayat terpasang 2015 sampai 2025 per tahun; tambahan per tahun terhadap rencana (kalibrasi).
- Pipeline: PPA ditandatangani, penutupan finansial (FID), tanggal operasi (COD), proyek tertunda dan alasannya.
- Faktor kapasitas aktual per teknologi (ESDM) dan teoretis; kurtailmen.
- Biaya: biaya modal, BTT tetap, BTT variabel, harga patokan tertinggi menurut regulasi (Perpres 112 Tahun 2022 dan turunan), tarif realisasi.
- Kendala: jaringan, penyimpanan pendamping, TKDN, pembebasan lahan, perizinan.
- Faktor emisi jaringan menurut sistem dan tahun (rata-rata dan marginal), pembangkit mana yang digantikan.
- Emisi siklus hidup per teknologi (faktor pembanding).
Sumber: PLN RUPTL dan statistik, KESDM (EBTKE, Gatrik) dan Handbook, Perpres 112/2022, JETP CIPP, IEEFA, IESR, IRENA, katalog teknologi KESDM-DEA, jurnal; basis data proyek (GEM, proyek PLN).
Keluaran: template; tabel terpasang dan pipeline per tahun; faktor emisi jaringan per sistem; angka pengurangan per teknologi (S x CF x 8,76 x EF) dengan rentang EF; mengganti ukuran surya "sisa selisih" dengan kapasitas bersumber.
Selesai bila: tiap teknologi punya potensi, rencana, riwayat, dan pipeline bersumber, serta faktor emisi jaringan per sistem.
Ukuran: L.

### WP-A Pendorong garis pembangunan: listrik dan batubara (G1, P1)
Data: PLTU dalam konstruksi (14,9 GW), direncanakan, dibatalkan; PLTU captive (17,7 GW, 127 unit 2030) per unit (pemilik, kapasitas, lokasi, tahun operasi, industri yang dilayani); tambahan fosil RUPTL per tahun; jalur permintaan RUKN; faktor pemanfaatan; jadwal pensiun sudah ada di garis dasar (JETP, Perpres 112/2022). Sumber: PLN, KESDM, GEM, JETP, IESR, Squire dkk. (GitHub penulis), laporan nikel. Keluaran: tabel pendorong per unit atau kelompok dengan emisi = kapasitas x CF x EF. Selesai bila setiap tambahan fosil sampai 2034 berstatus dan bertahun. Ukuran: M.

### WP-B Pendorong garis pembangunan: lahan (G2, P1)
Data: konversi berizin atau direncanakan: kuota deforestasi terencana dan tidak terencana (Renops), izin HGU, PBPH, tambang di kawasan hutan (IPPKH), food estate, perkebunan energi (5,4 juta ha dicadangkan), perkebunan sawit dan target biofuel (B40, B50), laju deforestasi Renstra; basis data spasial. Sumber: KLH, KLHK Kementerian Kehutanan, ATR BPN, Kementan, Global Forest Watch (pembanding), BTR. Keluaran: luas per pendorong x faktor emisi; peta pendorong ke aksi FOLU. Ukuran: L.

### WP-E Batubara hulu dan efisiensi pembangkit (P2)
Data: produksi dan RKAB, kewajiban pasar domestik dan harga, emisi fugitive metana tambang, laju kalor dan efisiensi PLTU (lampiran Rachmad dkk. per unit), nilai kalor batubara. Sumber: KESDM, Minerba, inventaris KLH, Rachmad dkk. 2024. Ukuran: M.

### WP-F Kalibrasi pelaksanaan (G4, P1)
Rencana dibanding capaian historis per pendorong dan per solusi: tambahan EBT terhadap RUPTL (2015 sampai 2025), keterlambatan COD PLTU dan EBT, deforestasi terhadap kuota, restorasi gambut (capaian setelah 2018), HTI (setelah 2017), B40 volume aktual, EV (angka terbaru), efisiensi (22,7 persen), co-firing (14,3 persen). Keluaran: faktor pelaksanaan bersumber per solusi dengan tahun data. Selesai bila setiap solusi punya satu faktor pelaksanaan bersumber atau diberi label "tidak ada data". Ukuran: L.

### WP-G Jalur NZE per subsektor dan inventaris subsektor (G5, G6, P1)
Data: asumsi subsektor LCCP_L (LTS-LCCR, lampiran SNDC, Bappenas), inventaris KLH 2000 sampai 2024 per subkategori energi (pembangkit, industri, transportasi, gedung, fugitive), konsistensi GWP. Keluaran: tabel pemetaan pendorong ke kategori inventaris ke sektor SNDC. Ukuran: M.

### WP-H FOLU: parameter solusi dan rincian CM2 (P1 untuk rincian CM2)
Data: rincian CM2 tambahan 195 Mt per aksi dan padanan basis Renops dengan SNDC; capaian terbaru per aksi; faktor gambut tunggal (32,42; 45,5; 24,8) dan luas; tingkat hidup rehabilitasi; lahan tersedia; mangrove (target dan capaian); pencegahan kebakaran gambut; paludikultur. Sumber: Renops, BTR-1 dan BTR-2, BRGM, KLH SRN, Murdiyarso dkk., Aryapratama dkk. Ukuran: L.

### WP-I Energi sisi permintaan (P2)
Efisiensi (enam program: skala, penghematan per unit, biaya Indonesia), biofuel (volume B40 aktual, selisih harga per liter dari Fitrady Lampiran E, faktor siklus hidup termasuk alih guna lahan, B50), transportasi (km tempuh per kendaraan, penjualan EV, bus), industri (ekstraksi TIMES dan HEIO per teknologi), gedung dan pendingin. Ukuran: L.

### WP-J Biaya, jadwal investasi, batas laju, hubungan antar solusi (G8, G9, G10, P2)
Lama bangun per teknologi, jadwal belanja modal, harga bahan bakar (HBA, gas), diskonto (6 persen Afriani, 9 persen ADB), laju maksimum historis per tahun (GW surya, panas bumi, pensiun PLTU, ha tanam, EV), aturan tumpang tindih, jalur faktor emisi jaringan menurut tahun. Ukuran: M.

### WP-K Konkordansi studi mapan (G11, P1)
Kumpulkan dan catat jalur, potensi, dan biaya per solusi dari studi utama: LTS-LCCR, SNDC 2025, BTR, dokumen Bappenas, peta jalan IEA, IESR, JETP CIPP, Bank Dunia CCDR, RUKN, RUPTL, IEEFA, makalah yang sudah tercatat. Daftar di luar repo berasal dari pengetahuan umum dan wajib diverifikasi. Keluaran: matriks solusi x studi (angka, tahun, cakupan, status) untuk K_Studi. Ukuran: L.

### WP-L Jalur 2060 dan keputusan lingkup (G12, G13, P3)
Jalur resmi atau mapan 2060 per sektor; keputusan lingkup limbah (371 Mt pada 2060), pertanian, IPPU. Ukuran: M.

### WP-M Pemeriksaan ulang data yang sudah tercatat (P1, paralel)
Tinjau 836 butir di D_Register_Sumber agar setiap butir memiliki konteks: cakupan, basis, tahun dasar, posisi terhadap garis dasar. Selesaikan konflik K122 sampai K141. Verifikasi tabel yang dibaca dari gambar (Cahyo Tabel 2, 3, 4; Nursidik Tabel 4). Pembagian: Claude menyiapkan pra-isian kolom konteks dari PDF; tim memverifikasi. Ukuran: L.

## 5. Urutan kerja yang disarankan

1. Hari pertama: tim mengisi matriks blok x jenis studi; menentukan peran (pemimpin riset, analis energi, analis FOLU, pustakawan data dan penjamin mutu, analis biaya).
2. Minggu pertama sampai kedua: WP-M, WP-G, WP-A, WP-B, WP-C, WP-D (P1, paralel menurut orang).
3. Minggu ketiga sampai keempat: WP-F, WP-H, WP-K; mulai WP-E, WP-I, WP-J.
4. Setelah itu: WP-L dan penyelesaian celah.
5. Model dimulai bertahap: garis pembangunan listrik dan FOLU dimulai segera setelah WP-A, WP-B, WP-G memiliki data cukup; tidak menunggu seluruh paket selesai. Minggu sebenarnya disesuaikan kapasitas tim.

## 6. Tolok ukur selesai

- Setiap angka punya konteks lengkap, status, sumber, dan pemeriksaan kedua.
- Setiap solusi di A_Kesiapan_Solusi berstatus "Siap" atau punya celah tercatat dengan kode WP.
- Minyak dan gas, serta energi terbarukan, masuk ke audit kesiapan dengan baris per solusi.
- Tidak ada konflik K yang belum dikaji.

## 7. Hasil serah terima

Tim menyerahkan: template terisi, berkas sumber di `sources/`, daftar konflik, daftar celah yang tidak dapat diisi (dengan alasan). Claude mengimpor template ke D_Register_Sumber dan memperbarui K_Konflik, A_Kesiapan_Solusi, dan model.
