"""Tulis catatan per sumber (notes/sumber/Sxxx.md), data register per sumber (data/per_sumber/Sxxx.csv) dan notes/INVENTARIS_SUMBER.csv.
Memakai /tmp/claude-0/inv.json (skrip 19) dan D_Register_Sumber pada workbook LATEST. Kedalaman baca: A angka diverifikasi pada PDF/CSV; B abstrak dan kesimpulan ditinjau dan ringkasan tim; C diarsip, konteks dari ringkasan tim."""
import json,re,csv,os,sys,openpyxl
R='/home/user/NetZeroEmission'
inv=json.load(open('/tmp/claude-0/inv.json'))
# (substring nama berkas) -> (jenis, WP, kedalaman, konteks)
C=[
('1.pdf',('Studi model','WP-K','A','Squire dkk. 2024 (Commun. Earth Environ.): kelayakan co-firing limbah biomassa di PLTU Indonesia; skenario pasokan dan permintaan, emisi PLTU 2020 sampai 2030.')),
('2.pdf',('Studi empiris','WP-B','A','Aryapratama dkk. 2026 (Biomass Bioenergy): kesesuaian biofisik restorasi lahan terdegradasi untuk kayu dan energi; batas atas luas 3,6 Mha.')),
('3.pdf',('Model sistem energi','WP-I','A','Utama dkk. 2025 (Energy and Climate Change): model TIMES untuk industri (semen, baja, pulp, amonia, metanol, olefin); efisiensi sekitar 8 sampai 9 persen abatement 2060.')),
('4.pdf',('Studi biaya','WP-B/H','A','Rossita dan Boer 2025 (Carbon Balance Manage.): biaya LUCF menuju NDC; COMAP, USD per ha dan per tC; sumber persentase pelaksanaan gambut dan HTI.')),
('2021_Sijabat',('Studi empiris','WP-D','A','Perbandingan kelayakan finansial PLTS Indonesia dan Arab Saudi; tabel 1 berupa gambar, dibaca langsung.')),
('2022_KLHK',('Dokumen resmi','WP-H','A','Renops FOLU Net Sink 2030 (SK 168/2022): luas dan anggaran per aksi, Tabel 1, 2, 111, 133 sampai 146; sumber resmi sasaran FOLU. Dokumen besar (sekitar 550 ribu karakter); bagian ditelusuri lewat tabel.')),
('2023_ETP-Kompensasi',('Data tabular (CSV)','WP-A/J','A','Tabel 14.1 ETP/UNOPS: kompensasi 32 aset PLTU; jumlah baris diperiksa langsung.')),
('2023_Studi-Implikasi',('Studi fiskal','WP-A/J','A','ETP/UNOPS Oktober 2023: implikasi fiskal pensiun dini PLTU; mekanisme pembayaran, Tabel 4.10, 4.11, 14.1, studi Ombilin.')),
('2024_Fitriana',('Model sistem energi','WP-K','A','Fitriana dkk. 2024 (IJSEPM): optimisasi bauran pembangkit LEAP-NEMO sampai 2075 dan 2100.')),
('2024_Forests',('Studi empiris','WP-H','A','Hermudananto dkk. 2024 (Forests): RIL-C di konsesi, emisi per ha tebangan.')),
('2024_Hilmiyati',('Studi empiris','WP-I','A','Hilmiyati dkk. 2024: LPG ke listrik (induksi) di Jawa-Bali.')),
('2024_PNAS',('Studi empiris','WP-H','A','Murdiyarso dkk. 2024 (PNAS): faktor emisi gambut dan mangrove; FRL kebakaran gambut.')),
('2024_Pambudi',('Ulasan teknis','WP-D','A','Pambudi dan Ulfa 2024 (RSER 189): lanskap panas bumi Indonesia; potensi 29,5 GW, terpasang 2.356 MW.')),
('2024_Squire-dkk_Biomassa',('Data tabular (CSV)','WP-K','A','Data penulis Squire: potensi limbah biomassa per provinsi (8 jenis); jumlah 504,4 miliar MJ.')),
('2024_Squire-dkk_Emisi',('Data tabular (CSV)','WP-K','A','Data penulis Squire: emisi PLTU 2020 sampai 2030 menurut lima skenario co-firing.')),
('2024_Squire_cofiring',('Studi model','WP-K','A','Salinan duplikat makalah Squire (nama berbeda).')),
('2024_Zahari',('Studi model','WP-I','A','Zahari dan McLellan 2024: transportasi rendah karbon (dinamika sistem, ASI).')),
('2025_ERIA',('Studi kelayakan','WP-C/J','A','ERIA/Sumitomo 2025: kelayakan CCS PLTU Tanjung Jati B 5 dan 6; biaya, rute kapal dan pipa, penyimpanan Corridor.')),
('2025_LCA',('Studi LCA','WP-I','A','Wahyono dkk. 2020: LCA biodiesel sawit cradle to gate.')),
('2025_PLN',('Laporan perusahaan','WP-D/G','A','PLN Climate-Related Disclosure Report 2024 (IFRS S2): emisi lingkup 1 sampai 3, jalur ARED dan BAU, realisasi pengurangan, co-firing, CCS Indramayu.')),
('2025_Sugito',('Studi simulasi','WP-J','A','Sugito dkk. 2025: simulasi CCS PLTU 2 x 315 MW; penalti daya dan biaya tangkap.')),
('2025_Suntoro',('Studi empiris','WP-I','A','Suntoro dkk. 2025: program rice cooker (kompor listrik) untuk memasak bersih.')),
('2025_Zain',('Model','WP-I','A','Zain dkk. 2025: perubahan energi dan emisi industri (HEIO/SDA); faktor emisi IPCC.')),
('2026_Fadiilah',('Studi empiris','WP-A','A','Fadiilah dan Dye 2026: pensiun dini PLTU, emisi dari Sentinel 5P dan HYSPLIT, dampak populasi; enam PLTU prioritas.')),
('2026_Fitriana',('Model sistem energi','WP-K','A','Fitriana dkk. 2026 (Results in Engineering): analisis biaya manfaat transisi listrik LEAP-NEMO.')),
('2026_IEEFA',('Laporan LSM','WP-D','A','IEEFA Agustus 2026: ekonomi listrik dan target surya 100 GW; biaya, CF, perbandingan batubara.')),
('2026_OWID_Energi',('Data tabular (CSV)','WP-G','A','Our World in Data, cuplikan Indonesia 2015 sampai 2024 (Energy Institute, Ember).')),
('2026_OWID_Kamus',('Data tabular (CSV)','WP-G','C','Kamus indikator untuk cuplikan OWID.')),
('2026_Usman',('Studi sumber daya','WP-C','A','Usman dkk. 2026 (Evergreen): kematangan sumber daya penyimpanan CO2 Indonesia (SPE-SRMS).')),
('Analysis_of_the_political',('Studi kebijakan','WP-K','A','Syuryansyah dan Amalia 2025: model arus sistem politik Easton untuk ratifikasi NZE (konteks kelembagaan; sama dengan papers/2025_Syuryansyah).')),
('At what cost',('Studi fiskal','WP-J','A','Fitrady dkk. 2026 (Energy Policy 212): biaya ekonomi dan fiskal program biodiesel.')),
('Cahyo-Adhi',('Makalah konferensi','WP-A/D','A','Cahyo dkk. (PLN Research Institute, 2024): tantangan sektor listrik menuju NZE; tabel LCOE dan EPC berupa gambar, dibaca langsung.')),
('Cost Co Firing',('Studi biaya','WP-K','A','Biaya co-firing biomassa (sumber CREA/PLN); harga dan pasokan.')),
('Economic_Strategies',('Studi model','WP-A','A','Rachmad dkk. 2024: strategi ekonomi dan efisiensi PLTU batubara menuju NZE.')),
('Evaluating renewable',('Model OSeMOSYS','WP-K','A','Afriani dan Poletti 2026 (Energy Policy 211): jalur EBT dan target emisi untuk PLN.')),
('Impact_of_Net_Zero',('Studi dinamika sistem','WP-I','A','Robbi 2026: dampak NZE 2060 terhadap adopsi kendaraan listrik komersial.')),
('Jakarta Transportation',('Laporan LSM','WP-I','A','Greenpeace dan RDI 2023: transformasi transportasi Jakarta, faktor emisi jaringan.')),
('Optimization_of_Electricity',('Model LEAP','WP-K','A','Nursidik dkk. 2025: optimasi skenario transisi listrik NZE 2060, LEAP.')),
('Optimizing power sector',('Model kebijakan','WP-K','A','Sunanda dkk. 2026 (MISCAP): dekarbonisasi sektor listrik, kerangka kebijakan terpadu.')),
('2026_Sunanda',('Studi model','WP-K','A','Salinan unggahan main dari Sunanda dkk. 2026 (MISCAP); isi teks identik dengan berkas Optimizing power sector decarbonization (byte berbeda). Butir register dicatat pada berkas asli.')),
('PaperAndrew',('Makalah konferensi','WP-A/D','A','Salinan Cahyo dkk. (nama berbeda).')),
('spesifikasi-b40',('Dokumen resmi','WP-I','A','SK Dirjen Migas 384.K/2024 dan Kepmen ESDM 341.K/2024: spesifikasi biosolar B40.')),
('2024_Amalia',('Ulasan hukum','WP-K','B','Amalia dkk. 2024: kerangka hukum dan kebijakan listrik menuju NZE; mengutip Perpres 112/2022 (pengecualian PLTU). Konteks, tanpa angka tercatat.')),
('2025_Aminy',('Statistik deskriptif','WP-G','B','Aminy dkk. 2025: faktor penyumbang emisi CO2 Indonesia dari data OWID 1970 sampai 2023; klaim pangsa global perlu jejak indikator.')),
('2025_Bhakti',('Model ANFIS','WP-K','B','Bhakti dkk. 2025: proyeksi transisi energi nasional dengan ANFIS; sumber daftar 22 rujukan; akurasi 93,5 persen tidak dijelaskan. Tidak dipakai untuk angka.')),
('2025_Kanugraha',('Ulasan kebijakan','WP-D','B','Kanugraha 2025: peran RUPTL dan investasi PLTN; jadwal dua unit 250 MW 2032 sampai 2033.')),
('2025_Syuryansyah',('Studi kebijakan','WP-K','B','Syuryansyah dan Amalia 2025: arus sistem politik ratifikasi NZE; konteks kelembagaan.')),
('2026_Susilo',('Studi ekonometrik','WP-B','B','Susilo dkk. 2026: model koreksi galat pertumbuhan, deforestasi, dan CO2 2004 sampai 2023; tidak memberi faktor per hektare.')),
('3.Artikel',('Studi keuangan','WP-J','B','Aminin dan Khayati 2025: green sukuk untuk energi terbarukan; alokasi dan klaim pengurangan 2018 sampai 2022.')),
('Accelerating',('Model sistem energi','WP-K/D','B','Gulagi dkk. 2025 (IET RPG): transisi batubara ke EBT, skenario BPS, DPS, CPS; transfer antarwilayah dan biaya sistem.')),
('Analysis_of_The_Effectiveness',('Tinjauan sistematis','WP-F/H','B','Irwanto 2025: efektivitas FOLU Net Sink 2020 sampai 2024 (tinjauan); capaian kumulatif sampai 2023.')),
('Ancaman_Deforestasi',('Ulasan hukum','WP-B','B','Maulida dkk. 2025: ancaman deforestasi terhadap NZE; kutip proyeksi LTS-LCCR 14,6 dan 6,8 juta ha.')),
('Artikel_Hukum',('Ulasan hukum','WP-K','C','Eka dkk.: kerangka hukum transisi energi; kontradiksi kebijakan batubara. Konteks; angka Rp117 triliun tidak dipakai.')),
('Bridging',('Studi konferensi','WP-D','B','Ardiansyah dkk. 2024: tolok ukur LCOE IESR dan emisi siklus hidup per teknologi.')),
('Bursa_Karbon',('Studi kebijakan','WP-J','B','Mukti dkk. 2025: bursa karbon IDXCarbon; harga dan volume 2024.')),
('Carbon_Pricing',('Studi kebijakan','WP-J','B','Nurhayati dkk.: kebijakan harga karbon; batas bawah Rp30 per kg (UU HPP).')),
('Contesting',('Studi kelembagaan','WP-H','C','Pendekatan ekosistem dan translasi kebijakan; konteks, memuat rujukan Cirata.')),
('Discourse',('Analisis wacana','WP-K','C','Fadlan dkk. 2026: kerangka media atas wacana NZE (10 artikel); bukan data teknis.')),
('Dukungan_Partisipasi',('Studi sosial','WP-H','C','Partisipasi masyarakat dalam FOLU Net Sink 2030 di Lampung.')),
('ENERGI_NUKLIR',('Ulasan hukum','WP-D','B','Fautngiljanana 2023: regulasi nuklir (BAPETEN, PP 2/2014, limbah); daftar periksa verifikasi milestone RUPTL.')),
('Energy_Security',('Studi kualitatif','WP-D','C','Luthfiani 2024: peran IRENA dalam ketahanan energi; konteks, mengutip Cirata 145 MW.')),
('Evaluation_of_Coal',('Studi model','WP-A','B','Prabowo dan Dalimi 2026: lintasan emisi armada PLTU (GEM, 526 unit); Tabel 1, 2, 3, 5.')),
('Examining_legal',('Ulasan hukum','WP-D','B','Sudarwanto dan Daryanti 2025: instrumen hukum; Cirata USD 129 juta, 250 GWh.')),
('Implementasi_Just',('Ulasan kebijakan','WP-J','B','Implementasi JETP: CIPP, USD 49,2 miliar untuk 16,1 GW; roadmap jaringan pintar PLN.')),
('Implementation_of_forest',('Studi empiris','WP-H','B','Dharmawan dan Pratiwi 2023: rehabilitasi hutan dan lahan 2015 sampai 2019 dan target FOLU 2022 sampai 2030.')),
('Kajian',('Kajian provinsi','WP-H','C','Gap analysis rencana kerja FOLU Net Sink Riau, Semenanjung Kampar-Kerumutan (115 hlm.): cakupan RO per lokasi; belum dibaca per bagian.')),
('Malik',('Ulasan hukum','WP-K','C','Malik: peran hukum nasional dalam dekarbonisasi menuju NZE 2060; konteks normatif.')),
('Policybriefinti',('Ringkasan kebijakan','WP-B','C','Policy brief lahan terdegradasi 14 juta ha (2018) dan rehabilitasi; konteks yang sama dengan 2.pdf.')),
('Potensi_Kebijakan',('Studi mineral','WP-K','C','Puspita dkk. 2025: logam tanah jarang Belitung; rantai pasok, tanpa angka NZE.')),
('Rafif',('Esai mahasiswa','WP-C','C','Esai NZE Pertamina; petunjuk sumber, tanpa bukti proyek.')),
('Reaktualisasi',('Ulasan hukum','WP-B','B','Subekti dan Aristawidya 2025: reaktualisasi FOLU Net Sink; deforestasi direncanakan 5,32 juta ha.')),
('ReformatManual',('Dokumen resmi','WP-H','C','Manual BRGM B-05/2023: pembacaan data geospasial Renops (RO2 sampai RO12); definisi aksi dan tumpang tindih. 68 hlm.; belum dibaca per bagian.')),
('Solar_Energy',('Ulasan kebijakan','WP-D','B','Kibtiah dkk. 2024: energi surya Indonesia, PLTS terapung Cirata 145 MW.')),
('TantanganRegulasi',('Ulasan hukum','WP-K','C','Nurbaety: tantangan regulasi transisi energi; Perpres 112/2022.')),
('The_Role_of_Carbon',('Studi kualitatif','WP-J','B','Saputri dan Diswandi 2025: pasar karbon dan REDD+.')),
('The_energy_mix',('Tinjauan pustaka','WP-K','B','Nasir dan Bengi 2024: dilema bauran energi; rujukan DEN dan biaya transisi USD 994 miliar.')),
('The_perspective',('Studi persepsi','WP-H','C','Perspektif multipihak terhadap implementasi FOLU Net Sink; konteks.')),
('Upaya_Pemerintah',('Ulasan kebijakan','WP-H','B','Husain dan Korbaffo 2024: pelestarian lahan basah; kinerja KLHK 2023.')),
('artikel8',('Ulasan kebijakan','WP-K','C','Makraja dan Azmi: ekonomi hijau dan Indonesia Emas 2045; konteks.')),
('bookchapter02',('Bab buku','WP-H','C','Pengelolaan hutan dan KPH; studi kasus faktor keberhasilan; konteks.')),
('2026_EI_Indonesia',('Data tabular (CSV)','WP-C/I','A','Seri Indonesia dari Energy Institute Statistical Review 2026 (salinan olahan pihak ketiga pada commit tetap, nilai dicek langsung terhadap JSON): produksi dan konsumsi biofuel (PJ), gas suar (miliar m3) dan CO2 gas suar (MtCO2), 2015 sampai 2025. Salinan pihak ketiga, belum dicocokkan dengan publikasi EI asli.')),
('2024_Perpres-132',('Dokumen resmi (OCR pihak ketiga)','WP-I/J','A','Perpres 132/2024 tentang pengelolaan dana perkebunan kelapa sawit; Pasal 18 dan 19: dana menutup selisih kurang HIP solar dan HIP biodiesel, dibayar paling lambat tiga bulanan, dibatasi kebijakan Komite Pengarah. Salinan OCR dari repositori pihak ketiga; cocokkan dengan naskah pengundangan sebelum mengutip verbatim.')),
('PADANAN_PENSIUN',('Data tabular (CSV)','WP-A/J','A','Padanan enam stasiun pensiun dini (Fadiilah dan Dye) dengan unit GEM dan aset ETP: 25 unit 14.420 MW dibanding 14.310 MW makalah; kapasitas Paiton 5-6 dan Suralaya 1-4/5-7 berbeda antar sumber.')),
('PADANAN_CAPTIVE',('Data tabular (CSV)','WP-A','A','Padanan captive RUPTL dan GEM (3 kelompok, 7 unit).')),
('PADANAN_PLTU',('Data tabular (CSV)','WP-A','A','Padanan PLTU RUPTL dan GEM (9 kelompok, 18 unit).')),
('PIPELINE_EBT',('Data tabular (CSV)','WP-D','A','Pra-isian 882 proyek pembangkit RUPTL (teknologi, status, COD RE Base dan ARED).')),
]
TEMUAN=[
('2024_Amalia','Ulasan hukum normatif: kontradiksi antara komitmen NZE dan peraturan nasional (penyederhanaan izin tambang, penambahan PLTU 31,9 GW atau 43 persen dari eksisting, pelonggaran pensiun PLTU). Rekomendasi revisi UU. Tidak ada data teknis baru.'),
('2025_Aminy','Statistik deskriptif OWID: Indonesia sekitar 3 persen emisi CO2 global (646 Mt), puncak 1997 (2,70 Gt, kebakaran gambut), bahan bakar fosil dominan sejak 2020. Teks dan gambar tidak konsisten untuk 1984 (K166).'),
('2025_Bhakti','ANFIS untuk proyeksi transisi energi; akurasi 93,5 persen tidak dijelaskan; tidak dipakai (aturan tanpa proyeksi buatan sendiri).'),
('2025_Kanugraha','RUPTL 2025 sampai 2034 menambah 69,5 GW (EBT 42,6 GW, penyimpanan 10,3, fosil 16,6) dengan nuklir 500 MW pertama kali; investasi nuklir USD 5 sampai 10 miliar, konstruksi 8 sampai 12 tahun. Totalnya mendekati jumlah pipeline proyek (K163 kemungkinan perbedaan periode).'),
('2025_Syuryansyah','Analisis kualitatif sistem politik Easton: input dukungan dan tuntutan, output kebijakan, umpan balik; angka kebijakan seperti pajak karbon Rp75 per kg (RUU KUP, lebih tinggi dari batas bawah Rp30 di UU HPP), potensi manufaktur EBT Rp8.824 triliun 2060, deforestasi neto turun 8,4 persen dan bruto 14,1 persen pada 2021 sampai 2022. Konteks kelembagaan.'),
('2026_Susilo','ECM 2004 sampai 2023: pertumbuhan dan deforestasi tidak signifikan secara individual; R2 0,6156; tidak memberi faktor emisi per hektare.'),
('3.Artikel','Green sukuk 2018 sampai 2022: 5,49 Mt CO2 (0,46 persen sasaran energi), kesenjangan investasi USD 146,4 miliar sampai 2030; pembilang dan penyebut tidak setara.'),
('Accelerating','Model sistem energi (BPS, DPS, CPS): transfer antarwilayah 158, 107, 22 GW; biaya listrik 2050 EUR 37, 41, 87 per MWh; 53 GW batubara terdampar bernilai USD 26 miliar; CCS tidak masuk bauran biaya terendah.'),
('Analysis_of_The_Effectiveness','Tinjauan pustaka: deforestasi neto 104 ribu ha (2022) dibanding 450 ribu ha per tahun (2010 sampai 2015); restorasi gambut 1,7 Mha; mangrove 600 ribu ha ditargetkan 2024; hambatan: kapasitas daerah, El Nino, pendanaan, integritas pasar karbon.'),
('Ancaman_Deforestasi','Ulasan hukum: deforestasi 14,6 Mha (kebijakan saat ini) dibanding 6,8 Mha (LCCP) menurut LTS-LCCR; klaim penurunan 460 ribu ke 120 ribu ha per tahun; rekomendasi penegakan hukum dan kolaborasi internasional.'),
('Artikel_Hukum','Telaah sosio-legal: UU Minerba 3/2020 memperpanjang tambang batubara sampai 2049, tumpang tindih kewenangan, subsidi Rp117 triliun (IESR 2023); bandingan EEG Jerman. Angka subsidi tidak dipakai; Cirata disebut 16 MW (konflik dengan 145 MW).'),
('Bridging','Tolok ukur LCOE dan intensitas siklus hidup per teknologi (IESR 2023); potensi panas bumi 23,9 GW (K164); nuklir LCOE tertinggi 10,16 sen per kWh.'),
('Bursa_Karbon','IDXCarbon: unit terdaftar 1,35 juta tCO2e, transaksi 908 ribu tCO2e (Rp50,6 miliar); harga 2024 Rp40.000 sampai 80.000; klaim potensi USD 300 miliar per tahun tidak bersumber.'),
('Carbon_Pricing','Ratio legis pajak karbon (UU HPP, batas bawah Rp30 per kg; 2022 sampai 2024 hanya PLTU); bandingan Finlandia USD 73 dan Swedia USD 137 per t.'),
('Contesting','Studi kelembagaan FOLU Net Sink: pendekatan ekosistem, intersubjektivitas tipis, terjemahan kebijakan nasional ke daerah diperebutkan; PCA delapan faktor. Tidak ada angka teknis.'),
('Discourse','Analisis framing media atas NZE 2060 (10 artikel, enam berbingkai ekonomi); fosil sekitar 80 persen bauran energi menurut penulis. Bukan data teknis.'),
('Dukungan_Partisipasi','Partisipasi masyarakat RHL di Lampung efektif; kawasan hutan 948.641 ha; target RPJMN 2029: penurunan emisi 30,11 persen dan intensitas 72,13 persen. Konteks sosial.'),
('ENERGI_NUKLIR','Tinjauan hukum normatif nuklir (BAPETEN, PP 2/2014, limbah); nuklir dipandang rendah karbon kedua setelah hidro; tidak ada angka biaya atau jadwal.'),
('Energy_Security','Kualitatif: kerja sama IRENA, USD 4 miliar pendanaan, 185.662 rumah tangga belum berlistrik; Cirata 145 MW. Tidak dipakai di model.'),
('Evaluation_of_Coal','Lintasan emisi 526 PLTU (127,68 GW; baseline 318 unit 71,63 GW): 394,6 Mt per tahun dan 7,89 Gt sampai 2045; 20 unit hampir seperempat emisi; subkritis 55,6 persen unit; mencakup captive.'),
('Examining_legal','Ulasan instrumen hukum: revisi target EBT 17 sampai 19 persen (2025) dan 19 sampai 21 persen (2030); Cirata USD 129 juta, 250 GWh.'),
('Implementasi_Just','JETP USD 20 miliar (publik 10 dari IPG); VRE 1 persen ke 14 persen (2030) dan 25 persen (2040); CO2 energi 696,7 Mt (2022).'),
('Implementation_of_forest','Rehabilitasi 2015 sampai 2019 sekitar 237 ribu ha per tahun dibanding target FOLU 917 ribu ha per tahun (sekitar 3,9 kali); lahan kritis 14,01 Mha (2018).'),
('Kajian','Gap analysis Riau: lanskap Kampar dan Kerumutan 1,595 Mha rencana aksi (27,95 persen target Renja Riau); terbesar tata air gambut 781 ribu ha, pencegahan deforestasi gambut 455 ribu ha, restorasi 231 ribu ha; kritik: ambisi Riau, koordinasi lapangan, integrasi karhutla. Dibaca: daftar isi, Tabel 1, tujuan, kritik dan rekomendasi; bab ancaman dan analisis RO per bagian belum dibaca rinci.'),
('Malik','Ulasan hukum: kerangka progresif (Paris, UU HPP, Perpres 98/2021) tetapi kesenjangan target 23 persen EBT 2025 dan realisasi. Tidak ada data teknis.'),
('Policybriefinti','Ringkasan kebijakan: lahan terdegradasi 14 Mha (2018); rehabilitasi KLHK 2016 sampai 2020: 198.346; 200.990; 188.630; 395.169; 112.419 ha; target 8,26 Mha (917 ribu ha per tahun).'),
('Potensi_Kebijakan','Geologi logam tanah jarang Belitung (granit, monasit, xenotim); rantai pasok; tidak ada angka NZE.'),
('Rafif','Esai mahasiswa: Pertamina 10 persen energi terbarukan 2025 dan 30 persen pengurangan GRK 2030 (target tanpa sitasi langsung); petunjuk sumber PGE dan PHE.'),
('Reaktualisasi','Ulasan hukum FOLU Net Sink: target emisi negatif 140 Mt 2030; deforestasi 2012 sampai 2030 tertulis 7,27 Mha dengan komponen 5,32 + 5,15 Mha (tidak konsisten, K165); FWI 1,47 Mha per tahun; PSN dan food estate 2,68 Mha di Papua.'),
('ReformatManual','Manual BRGM B-05/2023: definisi RO2 sampai RO12, Indeks Prioritas Lokasi dari skor ordinal emisi, serapan, kebakaran (0 sampai 3), dua aliran pelaporan (implementasi dan emisi tahunan), tumpang tindih aksi diizinkan. Dibaca: daftar istilah, bagian IPL dan Tabel 6; bab teknis lain belum.'),
('Solar_Energy','PLTS: Rp165 triliun untuk 5.000 MW, potensi surya sangat tinggi, EBT 2,1 persen dari potensi 400 GW; Cirata 145 MW dengan Masdar.'),
('TantanganRegulasi','Tinjauan yuridis: Perpres 112/2022, batubara 40,46 persen bauran, pembatasan kapasitas PLTS atap 10 sampai 15 persen perlu diganti kuota atau net metering.'),
('The_Role_of_Carbon','Wawancara dan studi kasus REDD+: peluang kredit karbon, partisipasi masyarakat; tidak ada biaya atau hektare terukur.'),
('The_energy_mix','Tinjauan: jalan peta DEN 2025, 2035, 2050 (231,2; 388; 1.043,8 MtCO2e) dengan syarat induksi 8,1; 28,2; 46,6 juta rumah tangga, kendaraan listrik, jaringan gas, biofuel 40 persen; konsumsi 2022 1,18 miliar BOE; EBT bisa hanya 17 persen pada 2025.'),
('The_perspective','Persepsi pengelola hutan Sulawesi Tengah: pandangan berbeda antar pemangku kepentingan terhadap FOLU Net Sink. Kualitatif.'),
('Upaya_Pemerintah','Kinerja KLHK 2023: gambut 271.721 ha, mangrove 3.064 ha (BRGM) dan 747 ha (RHL); 16,4 dari 24,2 Mha KHG rentan sedang dan tinggi; FOLU diproyeksikan hampir 60 persen target penurunan.'),
('artikel8','Ulasan ekonomi hijau menuju Indonesia Emas 2045: batubara lebih dari 60 persen listrik, EBT kurang dari 15 persen bauran, target 23 persen 2025. Konteks.'),
('bookchapter02','Bab buku pengelolaan hutan dan KPH: studi kasus faktor keberhasilan dan kegagalan (Sulawesi, 72 lokasi); konteks kelembagaan kehutanan.'),
]
def temuan(name):
    for k,v in TEMUAN:
        if k in name: return v
    return ''
def ctx(name):
    for k,v in C:
        if k in name: return v
    return ('Belum diklasifikasikan','','C','')
# register mapping: kata kunci dokumen register -> awalan nama berkas
MAP={'Statistik biofuel dan gas suar':'2026_EI_Indonesia','Perpres 132/2024':'2024_Perpres-132','Gap analysis rencana kerja FOLU':'Kajian','Kerangka hukum dan kebijakan listrik':'2024_Amalia','Faktor penyumbang emisi CO2':'2025_Aminy','Peran IRENA':'Energy_Security','FOLU Net Sink 2030':'2022_KLHK','Transport ASI':'2024_Zahari','Industrial energy HEIO':'2025_Zain','Solar 2021':'2021_Sijabat','IEEFA 100 GW':'2026_IEEFA','ERIA CCS':'2025_ERIA','LPG to induction':'2024_Hilmiyati','Faktor emisi gambut':'2024_PNAS','RIL-C konsesi':'2024_Forests','Kelayakan co-firing':'1.pdf','Restorasi lahan terdegradasi':'2.pdf','TIMES industry':'3.pdf','Biaya LUCF':'4.pdf','Co-firing biomassa di Indonesia':'Cost Co Firing','Tantangan sektor listrik':'PaperAndrew','Strategi ekonomi dan efisiensi':'Economic_Strategies','Optimasi skenario transisi':'Optimization_of_Electricity','Dampak inisiatif NZE':'Impact_of_Net_Zero','Analisis model arus':'Analysis_of_the_political','Biaya ekonomi dan fiskal':'At what cost','Jalur EBT dan target':'Evaluating renewable','Dekarbonisasi sektor listrik':'Optimizing power sector','Spesifikasi biosolar':'spesifikasi-b40','Penilaian siklus hidup biodiesel':'2025_LCA','Transformasi transportasi Jakarta':'Jakarta Transportation','Early retirement CFPP':'2026_Fadiilah_Dye','Rice cooker programme':'2025_Suntoro','Laporan pengungkapan terkait iklim PLN':'2025_PLN','Lanskap energi panas bumi':'2024_Pambudi','Evaluasi emisi PLTU':'Evaluation_of_Coal','Transisi batubara ke EBT':'Accelerating','Kerangka kebijakan dan realisasi':'Bridging','Implementasi Just':'Implementasi_Just','Bursa karbon':'Bursa_Karbon','Green sukuk':'3.Artikel','Rehabilitasi hutan dan lahan':'Implementation_of_forest','Pelestarian lahan basah':'Upaya_Pemerintah','Dilema bauran':'The_energy_mix','Studi implikasi fiskal':'2023_Studi-Implikasi','Penangkap karbon PLTU':'2025_Sugito','Kematangan sumber daya penyimpanan':'2026_Usman','Analisis biaya manfaat transisi':'2026_Fitriana','Optimisasi bauran pembangkit':'2024_Fitriana','RUPTL dan investasi PLTN':'2025_Kanugraha','Proyeksi transisi energi nasional':'2025_Bhakti','Surya terapung Cirata':'Solar_Energy','Pertumbuhan ekonomi, deforestasi':'2026_Susilo','Statistik energi Indonesia 2015':'2026_OWID_Energi','Efektivitas FOLU Net Sink':'Analysis_of_The_Effectiveness','Ancaman deforestasi':'Ancaman','Reaktualisasi FOLU':'Reaktualisasi','Kebijakan penetapan harga karbon':'Carbon_Pricing','Skenario emisi PLTU co-firing':'2024_Squire-dkk_Emisi'}
wb=openpyxl.load_workbook(sys.argv[1] if len(sys.argv)>1 else f'{R}/Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx',read_only=True,data_only=True)
reg={}
for r in wb['D_Register_Sumber'].iter_rows(min_row=6,values_only=True):
    if not r[1]: continue
    stem=next((s for k,s in MAP.items() if k in r[1]),None)
    if r[1].startswith('Kelayakan co-firing'): stem='1.pdf'
    reg.setdefault(stem,[]).append(r[:7])
kon={}
for r in wb['K_Konflik'].iter_rows(min_row=5,values_only=True):
    if r[0] and str(r[0]).startswith('K'): kon[r[0]]=' '.join(str(x) for x in r[:12] if x)
rows=[]
for rec in inv:
    jenis,wp,depth,ctxt=ctx(rec['name'])
    tm=temuan(rec['name'])
    if tm and depth=='C': depth='B'
    stem=next((s for s in reg if s and (rec['name'].startswith(s) or s==rec['name'] or (s.endswith('.pdf') and rec['name']==s))),None)
    items=reg.get(stem,[]) if stem else []
    # PaperAndrew dan Cahyo: berbagi daftar
    if rec['name'].startswith('Cahyo'): items=reg.get('PaperAndrew',[])
    ks=sorted([k for k,v in kon.items() if rec['name'][:12] and any(w in v for w in [rec['name'].split('_')[1] if '_' in rec['name'] else rec['name'][:10]])])[:0]
    note=f"# {rec['id']}: {rec['name']}\n\n- Jalur: `{rec['path']}`\n- Jenis: {jenis}\n- WP terkait: {wp}\n- Halaman: {rec['pages'] or '-'}; SHA-256: `{rec['sha'][:16]}`\n- Duplikat isi dari: {rec['dup_of'] or 'tidak ada'}\n- Kedalaman baca: **{depth}** (A angka diverifikasi pada sumber; B abstrak, kesimpulan, dan kalimat berangka dibaca (bagian lain belum); C diarsip tanpa pembacaan)\n- Butir pada D_Register_Sumber: {len(items)}\n\n## Konteks\n{ctxt}\n\n"
    if tm: note+=f"## Temuan pembacaan ulang (24 Nov 2026)\n{tm}\n\n"
    if rec.get('title'): note+=f"## Metadata PDF\nJudul: {rec['title']}; penulis: {rec['author']}\n\n"
    if rec.get('abstract'): note+=f"## Abstrak (ekstrak otomatis)\n{rec['abstract']}\n\n"
    if rec.get('conclusion'): note+=f"## Kesimpulan (ekstrak otomatis)\n{rec['conclusion']}\n\n"
    if rec['type']=='csv': note+=f"## Isi\nBaris data: {rec.get('nrows','')}; kolom: {rec['first']}\n\n"
    if items:
        note+='## Butir yang tercatat\n|No|Bagian|Butir|Nilai|Satuan|\n|---|---|---|---|---|\n'
        for it in items: note+=f"|{it[0]}|{str(it[2])[:40]}|{str(it[3])[:80]}|{str(it[4])[:140]}|{str(it[5])[:30]}|\n".replace('\n','\n',1)
        with open(f"{R}/data/per_sumber/{rec['id']}.csv",'w',newline='',encoding='utf-8') as f:
            w=csv.writer(f); w.writerow(['no','dokumen','bagian','butir','nilai','satuan','catatan']); w.writerows([[x if x is not None else '' for x in it] for it in items])
    note+='\n## Catatan peninjau\nRingkasan konteks di atas disusun dari abstrak, daftar butir tercatat, dan catatan tim; bagian yang tidak tertulis di sini belum dibaca penuh.\n'
    open(f"{R}/notes/sumber/{rec['id']}.md",'w',encoding='utf-8').write(note)
    rows.append([rec['id'],rec['name'],rec['path'],rec['type'],jenis,wp,rec['pages'],rec['sha'][:12],rec['dup_of'],depth,len(items),f"notes/sumber/{rec['id']}.md",f"data/per_sumber/{rec['id']}.csv" if items else '',ctxt])
for k in [x for x in reg if x is None]:
    byd={}
    for it in reg[k]: byd.setdefault(it[1],[]).append(it)
    for j,(d,items) in enumerate(sorted(byd.items()),1):
        sid=f'X{j:03d}'
        note=f"# {sid}: {d}\n\n- Jenis: sumber tanpa berkas di repo (penelusuran web atau catatan pengguna)\n- Kedalaman baca: **C** (tidak ada PDF untuk diperiksa; status E atau sesuai kolom catatan)\n- Butir pada D_Register_Sumber: {len(items)}\n\n## Butir yang tercatat\n|No|Bagian|Butir|Nilai|Satuan|\n|---|---|---|---|---|\n"
        for it in items: note+=f"|{it[0]}|{str(it[2])[:40]}|{str(it[3])[:80]}|{str(it[4])[:140]}|{str(it[5])[:30]}|\n"
        open(f"{R}/notes/sumber/{sid}.md",'w',encoding='utf-8').write(note)
        with open(f"{R}/data/per_sumber/{sid}.csv",'w',newline='',encoding='utf-8') as f:
            w=csv.writer(f); w.writerow(['no','dokumen','bagian','butir','nilai','satuan','catatan']); w.writerows([[x if x is not None else '' for x in it] for it in items])
        rows.append([sid,d[:80],'(tanpa berkas)','web','Penelusuran atau catatan','', '','','','C',len(items),f'notes/sumber/{sid}.md',f'data/per_sumber/{sid}.csv','Tidak ada PDF; butir dari penelusuran web 23 Nov 2026 atau teks tempel pengguna'])
with open(f'{R}/notes/INVENTARIS_SUMBER.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['id','nama','jalur','tipe','jenis','wp','halaman','sha12','duplikat_dari','kedalaman','butir_register','catatan','data','konteks']); w.writerows(rows)
from collections import Counter
print(len(rows),Counter(r[9] for r in rows),'tanpa klasifikasi:',[r[1] for r in rows if r[4]=='Belum diklasifikasikan'])
