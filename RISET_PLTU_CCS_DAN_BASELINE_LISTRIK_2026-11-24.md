# Data operasi Tanjung Jati B, biaya pensiun PLTU dan baseline listrik

24 November 2026 WIB

Temuan ini melanjutkan [riset prioritas](LANJUTAN_RISET_PRIORITAS_2026-11-24.md) dan [cek batch 23 PDF](CEK_BATCH_23_PDF_2026-11-24.md). Angka RUPTL dan GEM mengacu pada transkripsi workbook. Tabel operasi, kebutuhan peralatan dan biaya ETP diperiksa pada PDF yang sudah diarsipkan.

## Tanjung Jati B unit 5 dan 6

Tabel 4.1 ERIA memberi angka operasi **1 Oktober 2022 sampai 30 September 2023**. Unit 5 berhenti pada Mei dan Juni 2023. Baris kapasitas bertanda neto, sedangkan baris produksi tertulis *Power Generation*. Kolom intensitas dihitung dari emisi dibagi MWh pada basis tabel tersebut. [ERIA, hlm. 27, PDF hlm. 41](sources/2025_ERIA_Kelayakan-CCS-Pembangkit-Termal-Indonesia.pdf#page=41)

| Unit | GEM ID | MW neto | COD | Produksi (GWh) | CF tabel | Emisi (MtCO2) | Intensitas turunan (tCO2/MWh) |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| 5 | `G100000109958` | 1.000 | Maret 2022 | 6.748 | 77% | 5,8 | 0,860 |
| 6 | `G100000109959` | 1.000 | September 2022 | 7.546 | 86% | 6,4 | 0,848 |
| Gabungan | | 2.000 | | 14.294 | 81,6% dihitung | 12,2 | 0,854 |

Konsumsi batubara gabungan pada tabel **6,7 juta ton**. Pada basis produksi dan emisi yang sama, hasil aritmetikanya **0,469 ton batubara/MWh** dan **1,82 tCO2/ton batubara**. Pemisahan konsumsi per unit membutuhkan data tambahan. [ERIA, Tabel 4.1](sources/2025_ERIA_Kelayakan-CCS-Pembangkit-Termal-Indonesia.pdf#page=41)

- **Kalibrasi historis.** Pada produksi dan emisi periode tabel, 95% tangkapan memberi **11,59 MtCO2 tangkapan bruto ilustratif**. Nilai ini mengandaikan seluruh flue gas dapat diproses pada tingkat tangkap tersebut sepanjang periode. ERIA merancang **13 MtCO2/tahun** dengan margin kapasitas pada desain. Prabowo dan Dalimi mengestimasi **9,404 MtCO2/tahun** sebelum tangkap untuk dua unit yang sama dengan asumsi operasi lain. Jangan mengganti satu komponen dari estimasi stasiun Fadiilah dan Dye dengan angka historis ERIA tanpa menghitung ulang produksi dan emisi unit lain pada tahun yang sama. [ERIA, hlm. 27 sampai 28](sources/2025_ERIA_Kelayakan-CCS-Pembangkit-Termal-Indonesia.pdf#page=41) · [Prabowo dan Dalimi, Tabel 5](papers/Evaluation_of_Coal-Fired_Power_Plant_Emission_Redu.pdf#page=10)
- **B5 dan B4 bertemu pada dua ID unit.** Setelah unit pensiun, jadwal operasi dan tangkapan CCS unit itu menjadi nol. Pada skenario CCS, emisi unit tetap dihitung sesudah penangkapan dan sebelum pengurangan neto di seluruh rantai. Pada skenario pensiun, hitung emisi pengganti dari MWh yang benar-benar hilang. Pakai basis produksi yang sama untuk kedua alternatif. [Padanan ke studi pensiun](data/PADANAN_PENSIUN_PLTU_ETP_FADIILAH.csv) · [Fadiilah dan Dye, Tabel 3 dan §5.1](sources/2026_Fadiilah-Dye_Pensiun-Dini-PLTU.pdf#page=6)

### Kebutuhan energi yang sudah dihitung sebagian

Pada aliran desain **35.616 t/hari** (sekitar 13 Mt/tahun), Tabel 4.6 memberi kebutuhan pompa dan pemanas di terminal penerima Sumatra untuk rute A. Tabel 4.10 memberi daya pompa untuk satu stasiun booster pada rute B. Konversi memakai 0,7457 kW/hp, dengan aliran 24 jam, tanpa koreksi efisiensi motor atau pasokan panas. Baris A dan B adalah desain alternatif. [ERIA, Tabel 4.6, PDF hlm. 52](sources/2025_ERIA_Kelayakan-CCS-Pembangkit-Termal-Indonesia.pdf#page=52) · [Tabel 4.10, PDF hlm. 57](sources/2025_ERIA_Kelayakan-CCS-Pembangkit-Termal-Indonesia.pdf#page=57)

| Rute | Peralatan | Spesifikasi tabel (hp) | Setara MW | Setara kWh per ton CO2 dialirkan |
| --- | --- | ---: | ---: | ---: |
| A, kapal | Pompa terminal penerima | 9.081 | 6,77 mekanis | 4,56 mekanis |
| A, kapal | Penukar panas terminal penerima | 57.397 | 42,80 termal | 28,84 termal |
| B, pipa | Pompa booster | 3.258 | 2,43 mekanis | 1,64 mekanis |

Untuk melengkapi penalti site-specific, tambahkan listrik tangkap, kompresi atau pencairan, injeksi, sumber uap, bahan bakar kapal bila berlaku, dan perubahan keluaran neto. Tabel 4.17 menjelaskan sumber listrik dan uap. Pada kasus dasar listrik berasal dari jaringan dan biaya listrik dimodelkan sebagai rasio CAPEX dalam OPEX. Dampak terhadap keluaran neto untuk suplai dari unit sendiri ditunda ke tahap kajian berikutnya. Angka pompa dan penukar panas memberi input parsial. Simulasi Sugito 2 × 315 MW tetap pembanding konfigurasi berbeda. [ERIA, §6.1 dan Tabel 4.17](sources/2025_ERIA_Kelayakan-CCS-Pembangkit-Termal-Indonesia.pdf#page=63) · [Sugito dkk.](sources/2025_Sugito-dkk_CCS-PLTU-2x315-MW.pdf)

### Biaya per ton dengan basis yang konsisten

Harga ERIA **USD 63,7/t rute A** dan **USD 72,4/t rute B** dapat direplikasi dari `(CAPEX + OPEX 25 tahun) / (13 Mt/tahun × 25)`. Rute A memberi total **USD 20.687,2 juta**, rute B **USD 23.525,5 juta**. Estimasi tingkat awal ini mengecualikan antara lain pembelian lahan, reklamasi, dan pemantauan kebocoran. Perhitungan atas basis yang sama untuk biaya per ton dihindari memerlukan tonase tersimpan setelah kehilangan dikurangi emisi tambahan pada rantai. Gunakan harga USD/t tertangkap dibagi rasio tonase neto terhadap tonase tertangkap hanya jika biaya dan utilisasi datang dari kasus yang sama. Biarkan rasio belum terisi sampai pasokan energi, emisi dan keluaran terverifikasi. [ERIA, Tabel 5.9 sampai 5.12](sources/2025_ERIA_Kelayakan-CCS-Pembangkit-Termal-Indonesia.pdf#page=75) · [§1.3, pengecualian biaya](sources/2025_ERIA_Kelayakan-CCS-Pembangkit-Termal-Indonesia.pdf#page=69)

Gambar 5.1 menuliskan pembilang NPV dan penyebut produksi listrik 25 tahun. Jika penyebut dibaca sebagai produksi fisik tak didiskonto dari 2.000 MW, CF 86% dan 25 tahun, **7,42 dan 9,47 sen USD/kWh** mengimplikasikan pembilang masing-masing **USD 27,95 dan 35,67 miliar**, melebihi total biaya tak didiskonto di atas. Jadwal arus kas dan perlakuan diskonto atas MWh perlu dikonfirmasi. Simpan tarif levelized tersebut dalam register sebagai hasil terbitan dengan basis yang belum tereplikasi. [ERIA, Gambar 5.1 dan Tabel 5.13 sampai 5.14](sources/2025_ERIA_Kelayakan-CCS-Pembangkit-Termal-Indonesia.pdf#page=76)

## Padanan biaya ETP pada enam stasiun kandidat Fadiilah dan Dye

CSV padanan menggunakan nama aset ETP sebagai kunci ke tabel 32 kelompok yang telah diarsipkan. Kelompok yang mendapat valuasi beririsan pada Suralaya 1 sampai 8, Cilacap Sumber 1 dan 2, Paiton-2 (Jawa Power), serta Lontar 1 sampai 3. Nilai skenario ETP untuk **enam kelompok aset tersebut berjumlah USD 2.474,27 juta** pada tahun pensiun masing-masing, atau **USD 1.701,41 juta dalam nilai kini 2022**. Subtotal mencakup tiga baris kompensasi nol sesuai studi. Cocokkan tanggal pensiun sebelum menghitung kebutuhan pendanaan 2030 karena Paiton 5 dan 6 berada pada 2031 dalam tabel biaya. [CSV padanan](data/PADANAN_PENSIUN_PLTU_ETP_FADIILAH.csv) · [CSV valuasi ETP](sources/2023_ETP-Kompensasi-Pensiun-PLTU_Tabel-14-1.csv) · [ETP, Tabel 14.1](sources/2023_Studi-Implikasi-Fiskal-Pensiun-Dini-PLTU.pdf#page=184)

- **Paiton dan Cilacap.** `D_Gen_Eksisting!B87:H87` menyebut Paiton 5–6 (Jawa Power), padanan untuk stasiun Paiton-2 pada GEM. Kapasitasnya **1.220 MW** pada Lampiran 1.4 ETP dan peta RUPTL, **1.320 MW** pada GEM dan Fadiilah, dan **1.519 MW** pada Lampiran 1.3 ETP. Basis kapasitas perlu diperiksa dengan operator. Paiton 1 dan 2 milik PLN dalam tabel ETP adalah kelompok 800 MW, sedangkan Paiton-1 di artikel dan GEM menunjuk unit 7 dan 8 milik Paiton Energy. Cilacap 1 dan 2 memberi valuasi untuk fase I 600 MW. Cilacap Sumber unit 3 dan 4 tidak termasuk valuasi itu, dan Adipala adalah entri tersendiri. [ETP, Lampiran 1.3 dan 1.4](sources/2023_Studi-Implikasi-Fiskal-Pensiun-Dini-PLTU.pdf#page=213) · [Fadiilah dan Dye, Tabel 1](sources/2026_Fadiilah-Dye_Pensiun-Dini-PLTU.pdf#page=4)
- **Cakupan dan ketidakpastian.** Dari padanan nama, tahun dan kelompok, **25 unit** pada snapshot GEM memberi **14.420 MW**, sementara artikel menyebut **14.310 MW**. Pertahankan selisih **110 MW** sampai rincian unit dalam data penulis terverifikasi. Nilai Suralaya 1–4 dan 5–7 masing-masing berbeda 200 MW antar sumber meski total kedua kelompok sama. Belum ada biaya ETP untuk Tanjung Jati B, Cilacap Sumber 3–4 atau Paiton-1. Emisi **93,52 MtCO2/tahun** adalah estimasi bruto enam stasiun dalam artikel. Subtotal ETP hanya mencakup sebagian unit, sehingga menghitung USD/t dengan membaginya dengan emisi bruto tersebut akan mencampur cakupan dan periode. Padanan juga belum membuktikan daftar unit pada 36 Mt CM2 resmi. [Fadiilah dan Dye, §4.3](sources/2026_Fadiilah-Dye_Pensiun-Dini-PLTU.pdf#page=5) · [ETP, Lampiran 1.4](sources/2023_Studi-Implikasi-Fiskal-Pensiun-Dini-PLTU.pdf#page=216)

## Cek perpindahan pembangkitan pada RUPTL 2030

Kedua skenario mempunyai **468,249 TWh** total produksi termasuk impor. Tabel berikut membaca `D_RUPTL` kolom I pada tabel produksi 5.128 dan 5.130 serta tabel emisi 5.175 dan 5.176. ARED menambah produksi EBT sekitar **7,899 TWh** sambil menurunkan pembangkitan gas **5,703 TWh** dan batubara **2,825 TWh**. Impor juga naik **0,631 TWh**. Pada perubahan paket rencana ini, pengurangan pembangkitan gas lebih besar dari batubara. Efek proyek tambahan terhadap jaringan masih memerlukan dispatch dan faktor emisi per sistem. [Workbook, `D_RUPTL!I6:I60`](<Indonesia_NZE_Data_Grafik_v2 (4).xlsx>) · [Sumber RUPTL PLN](https://web.pln.co.id/stakeholder/ruptl)

| Indikator 2030 | RE Base | ARED | Selisih ARED dikurangi RE Base |
| --- | ---: | ---: | ---: |
| Produksi EBT (TWh) | 90,435 | 98,334 | +7,899 |
| Surya (TWh) | 9,027 | 13,800 | +4,773 |
| Panas bumi (TWh) | 26,635 | 26,577 | −0,058 |
| Gas dan LNG (TWh) | 106,620 | 100,917 | −5,703 |
| Batubara (TWh) | 268,983 | 266,158 | −2,825 |
| Emisi pembangkitan (MtCO2) | 354 | 348 | −6 |

Gunakan **0,756 dan 0,743 tCO2/MWh** masing-masing sebagai intensitas rata-rata rencana RE Base dan ARED berdasarkan penyebut yang mencakup impor. Rasio antara perubahan emisi dan tambahan produksi EBT sekitar **0,760 tCO2/MWh** adalah perbandingan dua paket rencana. Faktor marjinal surya memerlukan keluaran jam per jam, kurtailemen, transfer antarsistem dan unit yang tergantikan. Untuk penyatuan daftar proyek, `D_Gen_Eksisting!B1644:I1644` memuat Lumut Balai agregat **110 MW**, sementara `PRJ-GEN-00156` di pipeline memuat **55 MW Unit 2** dengan COD rencana 2025. Simpan sebagai kandidat duplikasi hingga tanggal snapshot dan unit yang masuk angka 110 MW dikonfirmasi. [Workbook, `D_RUPTL!I65:I70` dan `D_Gen_Eksisting`](<Indonesia_NZE_Data_Grafik_v2 (4).xlsx>) · [Pipeline EBT](data/PIPELINE_EBT_RUPTL.csv)

Permintaan langsung ke PLN, ESDM, UNFCCC dan operator terkait masih mendapat HTTP 403 dari proksi. PPA, FID, COD aktual proyek lain, biaya sambungan, dan perubahan RUPTL setelah edisi 2025–2034 masih perlu dokumen primer. Catatan memakai sumber PDF yang sudah tersimpan dan menjaga angka konfirmasi terpisah dari asumsi serta aritmetika.
