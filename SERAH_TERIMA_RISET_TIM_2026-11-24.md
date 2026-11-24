# Serah terima awal riset untuk tim

24 November 2026 WIB

Tim dapat melanjutkan pencatatan dari [TEMPLATE_Catat_Data.xlsx](templates/TEMPLATE_Catat_Data.xlsx). Format disusun dari kolom wajib dalam rencana tim karena template yang disebut dan `PLAN_Model_Portofolio.md` belum tersedia di checkout ini. Workbook induk tetap utuh. Pra-isian mencakup 1.158 baris bernilai dan enam baris celah dengan nilai kosong. Angka dari dokumen resmi yang belum dapat dibuka ditelusurkan ke sel transkripsi workbook. Kolom pemeriksa kedua dan cek pemimpin masih kosong.

| Lembar | Isi yang dapat diperiksa |
| --- | --- |
| `Catat_Data` | 1.164 baris, termasuk tambahan kapasitas RUPTL per jenis dan tahun, proyek PLTU bernama, kapasitas dan status unit GEM, jalur SNDC, parameter FOLU, data awal migas dan seri ko-pembakaran dari CSV penulis |
| `Matriks_Sumber` | Cakupan awal delapan blok terhadap 13 jenis sumber beserta rujukan contoh dan batasannya |
| `Celah_WP` | Status dan kebutuhan bukti berikutnya untuk seluruh WP-A sampai WP-M |
| `Kesiapan_Solusi` | Status awal skala, faktor, dampak dan biaya untuk 22 opsi migas, energi terbarukan dan infrastruktur |
| `K_Studi_Awal` | Sembilan baris contoh konkordansi dengan skenario, cakupan, satuan dan rujukan |
| `Audit_Register` dan `Konflik` | 741 butir sumber yang tersedia, salinan 99 entri konflik, serta penanda bahwa K125 sampai K141 belum ada di checkout |

### Data baru dari penulis

Squire, Lou, dan Hilde (2024) menyediakan CSV Gambar 2 dan 6 di repositori yang dirujuk pada bagian *Data availability* dalam makalah. Salinan sumber memakai commit `6f1dce4069eb05fc55a16e09547f721e57129dc1`. Seri Gambar 6 berisi 55 nilai untuk 2020 sampai 2030 dan lima skenario. Pada 2030, BAU memberi 369,491737 MtCO2 dan skenario *Low* 355,304840 MtCO2. Selisih keduanya **14,186897 MtCO2** pada batas model penulis. Gambar 6 mencakup PLTU dalam model dan membatasi pengurangan pada tahap pembakaran. Dampak produksi dan pengangkutan biomassa berada di luar hasil ini. Pertahankan status E dan hindari penjumlahan dengan CM1 atau CM2. CSV provinsi diarsipkan untuk penelusuran potensi pasokan dengan memeriksa satuan grafik sebelum konversi. [Makalah penulis, Gambar 6 dan bagian Data availability](1.pdf) · [Repositori penulis](https://github.com/Jiehonglou/Viability-of-Co-Firing-Biomass-Waste-to-Mitigate-Coal-Plant-Emissions-in-Indonesia/tree/6f1dce4069eb05fc55a16e09547f721e57129dc1) · [CSV emisi](sources/2024_Squire-dkk_Emisi-Skenario-Co-firing.csv) · [CSV biomassa provinsi](sources/2024_Squire-dkk_Biomassa-Provinsi.csv)

### Temuan yang memengaruhi kesiapan model

- **WP-A dan WP-D.** Tambahan RUPTL tersedia per teknologi dan tahun untuk RE Base dan ARED. Pertahankan pemisahan kedua skenario, dan hubungkan agregat dengan proyek tanpa penjumlahan ganda. Status dan tahun dalam GEM mengikuti cuplikan Juli 2026 di workbook. Jadwal COD aktual, FID, PPA, riwayat kapasitas terpasang, faktor emisi jaringan per sistem dan CF terukur masih perlu sumber. Kapasitas surya dalam RUPTL memberi tolok ukur rencana. Kapasitas tambahan yang dapat dikreditkan terhadap CPOS memerlukan pencocokan proyek dan jaringan. [Portal RUPTL PLN](https://web.pln.co.id/stakeholder/ruptl)
- **WP-B dan WP-H.** Pra-isian membedakan kuota kehilangan, luas arahan, luas tindakan dan pengurangan emisi. Target rehabilitasi 4,32 dan 5,30 Mha berasal dari LTS-LCCR hlm. 43 pada CPOS dan LCCP. Temuan ini melengkapi penelusuran K126, meski baris konflik K126 sendiri belum ada. Selisih Renops 195 MtCO2e dan SNDC 186,859 MtCO2e tetap terpisah. Pembagian resmi CM2 dalam ton per aksi, konversi aktual per izin, realisasi setelah 2024 dan biaya lapangan masih kosong. [Rekonsiliasi FOLU dan rujukan](RESEARCH_NZE_2026-11-24.md#folu-workbook-reconciliation-and-remaining-research)
- **WP-C dan WP-G.** Yang dapat ditelusuri dari workbook adalah potensi agregat pemanfaatan gas suar dan kutipan kapasitas penyimpanan geologis. Pemisahan hulu, tengah, hilir dan pembakaran sendiri memerlukan tabel inventaris 1B2 dan 1A1 serta data aktivitas 2000 sampai 2024. Penggunaan gas oleh pembeli akhir perlu tetap berada di sektor pengguna. Untuk memenuhi syarat tiga opsi, tim masih memerlukan skala dan faktor terukur untuk gas suar, LDAR, pemulihan venting atau elektrifikasi pada fasilitas teridentifikasi. Rencana lifting dan daftar proyek migas bertanggal masih belum diperoleh. [UNFCCC BTR](https://unfccc.int/first-biennial-transparency-reports) · [Ditjen Migas](https://migas.esdm.go.id/) · [SKK Migas](https://www.skkmigas.go.id/)
- **WP-M.** Checkout ini mempunyai 741 nomor register sampai baris 746, dibanding 836 dalam rencana. Konflik yang tersedia berakhir pada K124. Lembar audit menyalin isi asli termasuk nilai majemuk agar tim dapat memecahnya ke format satu angka per baris dengan jejak asal. Pemeriksaan angka grafik Cahyo dan Nursidik, keputusan konflik, pemeriksa kedua dan pemeriksaan ulang 20 persen belum dilakukan. [Workbook sumber](<Indonesia_NZE_Data_Grafik_v2 (4).xlsx>)

Permintaan HTTP langsung ke portal ESDM, UNFCCC dan GEM ditolak proksi dengan status 403. Data baru yang didapat melalui GitHub tersimpan di `sources/`. Arsip PDF yang sudah ada tetap dapat ditelusuri melalui [daftar riset](RESEARCH_NZE_2026-11-24.md). Paket yang memerlukan data resmi di luar checkout, salinan register terbaru, atau verifikasi oleh anggota tim masih terbuka. Tidak ada perubahan pada model.

## Rujukan PDF yang baru ditambahkan

[Lihat peta 15 unggahan ke PDF dan baris register yang sudah ada](CEK_ARSIP_SUMBER_2026-11-24.md).
