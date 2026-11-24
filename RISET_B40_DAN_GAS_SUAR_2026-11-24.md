# B40, subsidi, dan emisi per liter

24 November 2026 WIB

Harga penyelesaian dan volume B100 yang dibayar masih perlu data primer per bulan. Faktor emisi siklus hidup nasional juga masih kosong. Pembanding publik terbaru memberi seri aktivitas biofuel dan gas suar Indonesia sampai 2025. Gunakan seri tersebut sebagai angka sementara sampai workbook penerbit bisa diperiksa.

## Pembanding aktivitas 2021–2025

Energi biofuel mencakup biogasoline seperti etanol serta biodiesel termasuk bahan bakar penerbangan berkelanjutan. Kuantitasnya sudah disesuaikan dengan kandungan energi. Angka berikut adalah baris Indonesia dari salinan olahan *Statistical Review of World Energy 2026*. Skrip dashboard membulatkan ke enam angka penting. Simpan sebagai pembanding aktivitas nasional dan pertahankan asal salinannya. [Tabel Energy Institute](https://www.energyinst.org/statistical-review/resources-and-data-downloads) · [Salinan data dengan commit tetap](https://github.com/hall-brad/energy-statistical-review-dashboard/blob/4803eba5eddf7e52b4deb0d117dda9abf0388e8c/ei_data.json) · [Parser](https://github.com/hall-brad/energy-statistical-review-dashboard/blob/4803eba5eddf7e52b4deb0d117dda9abf0388e8c/extract.py)

| Tahun | Produksi biofuel (PJ) | Konsumsi biofuel (PJ) | Gas suar (miliar m³ standar) | CO2 gas suar (MtCO2) |
| ---: | ---: | ---: | ---: | ---: |
| 2021 | 337,070 | 305,930 | 0,746395 | 1,50742 |
| 2022 | 389,605 | 343,949 | 0,765623 | 1,54625 |
| 2023 | 432,912 | 404,552 | 1,00386 | 2,02739 |
| 2024 | 458,544 | 433,164 | 0,893973 | 1,80547 |
| 2025 | 515,214 | 440,313 | 0,865840 | 1,74865 |

Asal kolom di JSON `sheets` adalah `Biofuels production - PJ`, `Biofuels consumption - PJ`, `Natural Gas Flaring`, dan `CO2 from Flaring`. Cocokkan `years` dengan `entities[name=Indonesia].values`. Konsumsi 2025 setara **122,309 TWh** setelah dibagi 3,6. Gunakan sebagai pembanding energi biofuel total. Liter B100 yang dialokasikan, dicampur, dikirim, atau dibayar membutuhkan seri sendiri. [Data](https://github.com/hall-brad/energy-statistical-review-dashboard/blob/4803eba5eddf7e52b4deb0d117dda9abf0388e8c/ei_data.json)

Gas suar 2025 sebesar **0,866 miliar m³ standar** dan **1,749 MtCO2** memberi pembanding skala nasional untuk WP-C dan WP-G. Catatan tabel CO2 menjelaskan bahwa estimasi dari 2013 memakai VIIRS Nightfire, mencakup suar migas hulu dan hilir, serta menyebut perubahan metodologi pada 2025. Tabel memakai GCV **40 MJ/m³** dan asumsi pembakaran sempurna untuk menghitung CO2 dari volume. Perlakukan volume dan CO2 sebagai satu rantai estimasi. Kemiripan angka CO2 dengan potensi pengurangan 1,7 MtCO2e pada workbook belum merekonsiliasi cakupan, metode, atau potensi pemulihan gas. Inventaris fasilitas, metana, venting dan kategori 1B2/1A1 perlu sumber sendiri. [Data dan catatan tabel](https://github.com/hall-brad/energy-statistical-review-dashboard/blob/4803eba5eddf7e52b4deb0d117dda9abf0388e8c/ei_data.json) · [Pembanding workbook](LANJUTAN_RISET_PRIORITAS_2026-11-24.md)

## Angka yang diperlukan untuk USD/tCO2e

**Dasar penyelesaian.** Salinan OCR Perpres 132/2024, Pasal 18 ayat (1)–(4), menjelaskan bahwa dana menutup selisih kurang antara HIP minyak solar dan HIP biodiesel dari kelapa sawit, dengan kedua indeks ditetapkan oleh menteri yang menangani energi. Ayat (4) menyebut semua jenis minyak solar. Ayat (5)–(9) mengaitkan pembayaran dengan verifikasi, syarat badan usaha, dan batas maksimum sesuai kebijakan Komite Pengarah. Perhitungan dilakukan paling lambat setiap tiga bulan berdasarkan kedua HIP periode transaksi. Pasal 19 ayat (4) menetapkan HIP solar untuk harga penyaluran biodiesel yang akan dicampur, dan ayat (6) menggunakan rerata kurs tengah BI untuk penetapan HIP biodiesel periode transaksi. Simpan segmen penyaluran dan volume yang lolos verifikasi sebagai kolom terpisah. Cocokkan salinan OCR hlm. 9–11 dengan naskah pengundangan sebelum mengutip pasal secara verbatim. [OCR Perpres 132/2024, hlm. 9–11](https://github.com/wahyubumi/regulasi-indonesia/blob/bb7bb491289c2a8a4441363e7255698dbc7586ad/regulasi/pusat/perpres/2024/perpres-2024-132-pengelolaan-dana-perkebunan/dokumen.md#L444-L558) · [Portal peraturan](https://peraturan.go.id/)

| Objek | Data yang diperlukan | Jejak sumber dan perlakuan |
| --- | --- | --- |
| Selisih HIP bruto (Rp/L B100) | HIP BBN biodiesel dan HIP solar sesuai metode penyelesaian pada bulan yang sama | Cek keputusan harga ESDM dan dasar penyelesaian yang dipakai BPDP. Catat bulan, harga, pajak, ongkos angkut dan tanggal efektif secara terpisah. [Arsip ESDM](https://www.esdm.go.id/id/media-center/arsip-berita) · [JDIH ESDM](https://jdih.esdm.go.id/) |
| Biaya fiskal aktual (Rp/L B100 terbayar) | Rupiah dana insentif yang dicairkan, liter yang dicakup pencairan, dan komponen yang termasuk | Padankan tanggal penyaluran, periode pencairan, penyesuaian, serta segmen PSO dan non-PSO. Agregasi sebagai total rupiah dibagi liter terbayar pada cakupan yang cocok. Rp35,5 triliun di `D_Register_Sumber!E478` masih berstatus kutipan sekunder dengan periode dan cakupan belum terverifikasi. [BPDP](https://www.bpdp.or.id/) · [Catatan awal B40](RESEARCH_NZE_2026-11-24.md#1-b40-biodiesel) |
| Emisi dihindari (kgCO2e/L B100 dan kgCO2e/L campuran) | Intensitas siklus hidup solar dan B100 (gCO2e/MJ), nilai kalor per liter masing-masing, dan sumber atau skenario bahan baku Indonesia | Samakan batas siklus hidup dan GWP, lalu pisahkan sensitivitas perubahan guna lahan dan metana limbah pabrik kelapa sawit. Gunakan data skala kebun/pabrik yang sesuai dengan bahan baku penyaluran. [Zahari dan McLellan, §2.3](sources/2024_Zahari-McLellan_Low-Carbon-Transport-Indonesia.pdf#page=3) · [Catatan awal B40](RESEARCH_NZE_2026-11-24.md#1-b40-biodiesel) |

Untuk perbandingan energi setara B40 dengan B0, gunakan `0,40 × nilai kalor B100 (MJ/L) × (intensitas B0 − intensitas B100) / 1.000` untuk kgCO2e per liter campuran. Untuk tambahan dari B35, hitung emisi setiap campuran per MJ lalu bandingkan pada energi terkirim yang sama. Transkripsi klaim ESDM **41,46 MtCO2e** per **15,6 juta kL alokasi B100** menyiratkan **2,658 kgCO2e/L B100** atau sekitar **1,063 kgCO2e/L B40** pada perbandingan volumetrik. Angka klaim dan faktor siklus hidup memerlukan kolom tersendiri. [Jejak klaim dan pembanding pembakaran](RESEARCH_NZE_2026-11-24.md#1-b40-biodiesel)

Hitung USD/tCO2e dengan membagi pengeluaran terukur dalam USD dengan abatement bersih dalam ton pada intervensi, periode dan cakupan volume yang sama. Publikasikan dua baris bila yang dibutuhkan adalah dampak seluruh mandat terhadap B0 dan tambahan B40 terhadap B35. **1 USD/tCO2e sama dengan 1 juta USD/MtCO2e.**

## Pemeriksaan sumber berikutnya

Permen ESDM 4/2025 tentang Pengusahaan dan Pemanfaatan Bahan Bakar Nabati dapat ditelusuri ke URL JDIH yang disebut Fitriana dkk., rujukan [53]. Untuk perhitungan harga cari pula Kepmen 341.K/EK.01/MEM.E/2024, publikasi HIP per bulan serta laporan penyelesaian BPDP tahun yang sama. Portal resmi ESDM dan BPDP menolak akses dari lingkungan ini. Untuk data primer siklus hidup, telusuri studi Meijide dkk. tentang kebun sawit Indonesia sebagai pembanding berdasarkan sejarah penggunaan lahan, dengan batas studi dan keterwakilan pasokan B40 diperiksa terlebih dahulu. [JDIH Permen 4/2025](https://jdih.esdm.go.id/dokumen/download?id=2025pmesdm4.pdf) · [Fitriana dkk., pustaka](sources/2026_Fitriana-dkk_Analisis-Biaya-Manfaat-Transisi-Listrik.pdf#page=15) · [Meijide dkk.](https://doi.org/10.1038/s41467-020-14852-6)
