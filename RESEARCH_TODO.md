# RESEARCH_TODO: riset yang masih harus dikerjakan dan usulan pengembangan

Terakhir diperbarui 24 Nov 2026. Berkas kerja terbaru selalu bernama `Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx`.
Aturan kerja: setiap berkas masuk dibaca seluruhnya, diekstrak, dicatat di `D_Register_Sumber`, diproses ke lembar hitung, lalu usulan pengembangan ditulis di sini. Pengembangan spreadsheet dikerjakan di repo ini, skrip di `scripts/`, PDF sumber di `sources/`.

## A. Riset yang harus dicari (urut prioritas)

Tujuan studi: memerinci solusi pengurangan emisi agar menutup selisih CPOS ke LCCP_L (2030: 434,7 MtCO2e; 2060: 1.967,8). Biaya saja, tanpa skema pembiayaan.

| No | Data yang dicari | Mengapa penting | Dipakai di |
|---|---|---|---|
| R1 | Selisih subsidi B40 per liter dan CO2 yang dihindari per liter | Biaya B40 belum ada; klaim ESDM 41,46 Mt (K122) | C_Solusi_2030 |
| R2 | Biaya efisiensi energi dari sumber Indonesia (USD per tCO2) | Hanya ada rentang 50 sampai 200 dari catatan tempel, status E | C_Solusi_2030, K124 |
| R3 | Faktor emisi batubara (kgCO2 per MWh atau per GJ), nilai kalor, dan laju kalor PLTU | Syarat mengubah biaya per MWh menjadi biaya per tCO2 | rencana C_Biaya_Per_tCO2 |
| R4 | Harga bahan bakar penuh (HBA batubara, gas, biomassa) dan BTT variabel | Tabel 96.A belum memuat bahan bakar; LCOE penuh perlu | C_Biaya_Teknologi |
| R5 | Verifikasi Tabel 4 Nursidik (katalog Generation and Storage of Electricity 2024, ESDM dan DEA) dan Tabel 4 EPC PLN (rujukan [32] Cahyo) | Tabel sumber berupa gambar, dibaca visual; kolom nuklir, hidrogen, PS, mikrohidro tidak terbaca utuh | C_Biaya_Teknologi, K128 sampai K130 |
| R6 | Biaya nuklir Indonesia (NEPIO, RUPTL 2025 sampai 2034, studi SMR, jadwal operasi) | Kini ada EPC 6.000 sampai 7.000 (PLN) dan 5.800 (LEAP); jadwal belum ada | opsi 2060 |
| R7 | Biaya CCS TJB dan penalti energi CCS | Hanya faktor 2,4 kali biaya modal PLTU dari LEAP; belum ada angka proyek | C_Solusi_2030 B5 |
| R8 | Rincian CM2 yang tidak dirinci: energi 50,3 Mt dan FOLU 195 Mt | Menentukan klaim penutupan selisih resmi | C_Solusi_2030 |
| R9 | Kuantifikasi resmi 2060 (energi dan FOLU) | Selisih 2060 sebesar 1.967,8 belum punya angka resmi | P_Ringkasan_Utama |
| R10 | Data BTR, FREL, dan inventaris terbaru (FOLU realisasi setelah 2024) | Beberapa baris C_Solusi_2030 bertanda "data terbaru belum ada" | C_FOLU_Net0_2030 |
| R11 | Data tambahan Squire dkk. 2024 (GitHub penulis): permintaan dan pasokan biomassa per provinsi dan per PLTU | Membatasi opsi co-firing menurut pasokan; K125 dan K127 | C_Cofiring_Biaya |
| R12 | Lampiran Rachmad dkk. 2024: data per PLTU (efisiensi, biaya operasi, CO2) | Menyusun urutan pensiun dini menurut efisiensi; K131 dan K132 | R_Unit_Skor |
| R13 | Satuan rencana PV skala besar 2030 (rujukan [23] Cahyo) | Angka tercetak MW tidak masuk akal (4,67 juta MW) | Tabel 96.D |
| R14 | Biaya restorasi gambut, mangrove, dan reforestasi per ha dari sumber Indonesia kedua (selain Rossita dan Boer) | Triangulasi biaya FOLU; Tabel 27.K | C_Opsi_Hitung |
| R15 | Biaya transmisi, penyimpanan, dan cadangan untuk surya dan angin (LEAP mengabaikan transmisi) | Biaya sistem surya 37,5 GW belum lengkap | C_Solusi_2030 B7 |
| R16 | Faktor emisi LPG, serbuk gergaji; sumber untuk catatan faktor K113 sampai K124 | Masih asumsi penulis atau status E tanpa sumber | D_Faktor |
| R17 | PLTU captive 17,7 GW (127 unit) pada 2030: kapasitas dan opsi pensiun | Squire dkk. mencatat captive berlipat dua; cakupan pensiun dini belum memasukkan | C_Phasedown_Unit |
| R18 | Biaya hidrogen dan amonia untuk co-firing, bila dianggap opsi | Disebut sebagai pilot PLN; belum ada biaya | opsi lanjutan |
| R19 | Rencana kapasitas 2030 untuk surya atap, surya terapung, angin darat (terpisah dari PLTS) dan angin laut | Hasil audit: RUPTL menggabung PLTS dan PLTB; tanpa pemisahan lembar angin dan surya atap tidak dapat dihitung | lembar S_ gelombang 1 |
| R20 | Aturan pembukuan emisi biomassa (netral atau tidak) bersumber, dengan rentang LCA | Menentukan tanda pengurangan PLTBm dan co-firing; NREL menyebut negatif 1.000 sampai positif 1.300 gCO2e per kWh | lembar biomassa |
| R21 | Volume gas suar dan faktor emisinya | Pengurangan 1,7 Mt resmi tanpa data teknis | lembar gas suar |
| R22 | Pengurangan per teknologi dari skenario TIMES (Utama 2025) dan HEIO (Zain 2025) untuk semen, baja, kertas, amonia, metanol, olefin | Data ada di PDF, belum diekstrak per teknologi | lembar industri |
| R23 | Kilometer tempuh per jenis kendaraan dan jumlah bus listrik 2030 bersumber | Mengubah target 15,2 juta EV dan bus menjadi MtCO2e | lembar BEV dan angkutan umum |
| R24 | Luas sawah AWD dengan faktor CH4, kapasitas PLTSa dengan faktor emisi sampah | Tidak ada data skala | lembar AWD dan PLTSa |

## B. Data yang masih harus diverifikasi (sudah dicatat, status ragu)

- Tabel 4 Nursidik dan Tabel 2 serta 4 Cahyo dibaca dari gambar; angka mungkin salah baca satu digit.
- Cahyo Tabel 3: satuan MW atau kW (R13).
- Rachmad: "23 persen" sama dengan 26 dari 113, bukan 26 dari 105 (K131); biaya operasi 0,19 USD per kWh tampak tidak sebanding dengan LCOE (K132).
- Aryapratama Tabel 4: GWPdyn kumulatif, bukan per tahun; pemetaan rentang persen BAU total dan FOLU dibaca dari teks.
- Nursidik: pernyataan "emisi energi 2030 sekitar 440 MtCO2e" bercampur dengan puncak pembangkit; samakan cakupan dengan model v2.1 sebelum dibandingkan.

## Catatan: lima PDF baru di sources/ (24 Nov 2026) belum dibaca; lihat sources/README.md

## C. Usulan pengembangan spreadsheet

1. **C_Biaya_Per_tCO2** (butuh R3, R4): ubah biaya per MWh (Tabel 96.A dan C) menjadi USD per tCO2 untuk surya, angin, panas bumi, nuklir, CCS, biomassa terhadap PLTU yang digantikan. Ini mengganti asumsi biaya per opsi yang masih kosong.
2. **Urutan pensiun dini menurut efisiensi**: gabungkan daftar PLTU efisien dan tidak efisien (Rachmad) dengan `R_Unit_Skor` dan `C_Phasedown_Unit` agar 57,5 Mt pensiun lanjutan memakai PLTU paling tidak efisien lebih dulu.
3. **Batas pasokan biomassa untuk co-firing**: tambahkan batas 504,4 miliar MJ per tahun (Squire) dan skenario Rendah, Menengah, Tinggi pada `C_Cofiring_Biaya`; bandingkan 11 Mt asumsi CM1 dengan 14,2 sampai 152,5 Mt (K125).
4. **Batas luas lahan restorasi**: bandingkan 0,44 sampai 3,60 Mha (Aryapratama) dengan target rehabilitasi LCCR 4,32 sampai 5,30 Mha di `C_Portofolio_FOLU_2030` (K126).
5. **Opsi nuklir 2060**: tambahkan baris opsi nuklir (biaya modal 5.800 sampai 7.000 USD per kW, umur 60 tahun) pada lembar opsi 2060 setelah R6; tidak dihitung pada 2030.
6. **Faktor emisi bus**: pakai 66,6 tCO2 per bus per tahun (Robbi) sebagai pembanding bus listrik di `C_Opsi_Hitung`; tinjau selisih harga solar subsidi 6.800 dan industri 25.750 Rp per liter.
7. **Silang periksa model LEAP**: bandingkan jalur emisi pembangkit 2030 sampai 2060 (Nursidik CS, ET, EBT) dengan jalur G_Model dan C_Listrik_Rencana; tambahkan baris konflik bila cakupan sama.
8. **Pemeriksaan otomatis baru di Q_Cek**: tambahkan uji "D_SNDC sama dengan Tabel 5 Robbi" (25 dari 25 CPOS sudah cocok secara manual).
9. **Sensitivitas diskonto**: C19 pada C_Biaya_Teknologi sudah dapat diubah; tambahkan tabel 6, 9, 12 persen bila dibutuhkan.
10. **Pembersihan format**: tab terpilih tunggal, tanpa freeze pane, tanpa tanda pisah panjang (aturan tetap).

## D. Riwayat pengerjaan

- 24 Nov 2026: legenda "base" pada Gambar 42.2, 42.4, 42.5 dikosongkan; freeze pane dan tab terpilih ganda dibersihkan; tanda pisah panjang dihapus (dua sampai tiga lokasi).
- 24 Nov 2026: Squire 2024 dan Aryapratama 2026 dicatat (22 butir), K125 sampai K127 ditambahkan.
- 24 Nov 2026: audit kesiapan 51 solusi selesai (lembar A_Kesiapan_Solusi, Lembar 97; AUDIT_Kesiapan_Solusi.md).
- 24 Nov 2026: lima makalah baru dicatat (46 butir, No 764 sampai 809), K128 sampai K132 ditambahkan, lembar baru `C_Biaya_Teknologi` (Lembar 96), hyperlink Indeks dijadikan internal (sebelumnya menunjuk ke nama berkas lama).
