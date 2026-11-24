# HANDOFF v3: Indonesia NZE 2060 workbook (state 23 Nov 2026, 15:20 WIB)

## 1. Goal
`Indonesia_NZE_Data_Grafik_v2.xlsx`: show, by year X, invest USD Y to cut Z MtCO2e per year, closing N% of the gap. Focus energy and FOLU, 2030 as quantified horizon; cost only (no financing schemes); official data first, unofficial layers labelled.

## 2. Standing user rules (ALWAYS)
- NEVER freeze panes (user was angry; base generator sets them, so strip `<pane>` and `<selection>` from xl/worksheets/*.xml after every build).
- No em or en dashes anywhere. Workbook text professional Indonesian (PUEBI). Unit MtCO2e. Status labels T/P/R/D/E/AC/A.
- No silent estimates; flag assumptions. Never modify D_Model_v21. Never mention "Pak Azis".
- Send the latest xlsx after each step plus a readable summary. No slides wanted. Do not duplicate existing charts; reuse data.
- Third-party claims never summed with official CM1/CM2. Conversation in English (user writes Indonesian/English mix). Act fast, plan briefly.

## 3. Current state (master: out/Indonesia_NZE_Data_Grafik_v2.xlsx)
- 93 sheets, 128 charts, 0 formula errors, Q_Cek 0 of 44, 0 freeze panes.
- Tab order: Presentasi (1), P_Ringkasan_Utama (2), Indeks (3, has "No" column), audit, P_, C_, M_, R_, G_, D_.
- Formal titles: "Lembar n.", tables "Tabel n.X." (letter kept so "bagian X" references stay valid), notes "Catatan n.X.", charts "Gambar n.m.". Tab colours by type.
- Key new sheets: Presentasi (7-part story with live messages and chart list), P_Ringkasan_Utama (Tabel 2.A to 2.G), C_Solusi_2030 (all energy and FOLU options, layer A in CM1 baseline vs layer B closing gap), G_Solusi_2030 (Gambar 40.1 to 40.6), C_Cofiring_Biaya, C_Portofolio_FOLU_2030, C_Portofolio_2030, C_Kartu_Opsi.

## 4. Key results (2030)
- Gap CPOS to LCCP_L: total 434,7; energy 239,1; FOLU 186,9. 2060: total 1.967,8, energy 1.432,8, nothing officially quantified.
- Energy layer B: official CM2 (pensiun dini 36, gas suar 1,7, CM2 tidak dirinci 50,3) closes 36,8%; + pensiun lanjutan 57,5 and CCS TJB 13 to 66,3%; + panas bumi 19,2 and surya about 37,5 GW (unofficial) to 100%. Costed options about USD 8,5 bn per year. Coal energy cap check 171 of 269 TWh.
- Energy layer A (CM1 358): EBT 97,0; efisiensi 132,2; B40 41,5 and co-firing 11 assumed inside CM1 (A); sisa 76,3.
- FOLU: per-action derived CM1 327 to 383 of official 497; CM2 increments 93,6 to 162,2 close 50 to 87% of 186,9 for about USD 0,22 bn per year; official CM2 increment 195 (not itemised) closes 104%.
- CORRECTION made: earlier FOLU result compared all removals incl. CM1 with the gap (wrong). Now only CM2 increments count, same as energy.
- Implementation problem: efisiensi 22,7%, co-firing 14,3%, restorasi gambut 10% (2018), HTI tertanam 14% (2017); RUPTL 2030 power emissions 104 Mt above JETP cap.
- Co-firing cost (C_Cofiring_Biaya): USD 1,0 (ideal) / 16,0 realised mix (used as low) to 48,9 per tCO2; fuel-price difference only.

## 5. Open items (user's last questions, UNANSWERED)
1. User says "many charts missing": all 128 charts exist with data in the xlsx. Ask which sheet/app (LibreOffice-made charts may not show in some viewers; freeze panes may have hidden them).
2. "Grafik per solusi": likely wants ONE chart per option (removal and cost per option) for every energy and FOLU option. Build if confirmed.
3. Pasted factor note (K113 to K124): logged as status E, not used. B40 cost, nuclear cost, efficiency Indonesian cost still missing.

## 6. Pipeline
Generator `build/build_nze_data_v2.py` (inputs in uploads/ and reg/, nze_extract/, ruptl/, new_in/) reproduces only the pre-digest base. Then apply UNO scripts in order (each reads out/ master, writes outN/, copy back to out/):
add_four_papers, add_blockK, fmt_blockK, add_kartu, idx_kartu, add_porto, idx_porto, add_layer2, add_folu, idx_folu, add_cofiring, add_solusi, tidy, then strip freeze panes (XML edit, see section 2).
UNO notes: `pkill -f soffice` before each run; formulas use `$Sheet.Cell` and `;`; in XY charts getDataRowProperties index 0 is the X column; dashed lines via UNO render invisible (use solid).
Register data: reg/reg_13_cofiring.py (latest), reg/reg_12_four_papers.py, tek_12_four_papers.py.

## 7. File map in this zip
- out/: master xlsx, this handoff, previous handoff v2.
- scripts/: all UNO scripts and render helpers.
- build/: generator and blocks. reg/: register inputs. fig/: earlier PNGs (FOLU PNG title is from the old wrong framing).
- inputs/: nze_extract, ruptl, new_in, uploads (source PDFs, CSVs, JSON, user model v2.1).

## Addendum (23 Nov 2026, 15:40 WIB)
- Presentasi tab deleted. New first tab G_Per_Solusi (Lembar 1): Tabel 1.A flow, 1.B energy and 1.C FOLU per option (removal, % of gap, cost, remaining), Gambar 1.1/1.2 sector line charts (emission after each option vs CPOS and LCCP_L), Gambar 1.3 to 1.20 one card plus ONE LINE CHART per layer-B option (energy B1-B7, FOLU B1-B11), Tabel 1.D layer A (in CM1), Tabel 1.E chart data.
- User rule: LINE CHARTS ONLY (no waterfall, no stacked bars). Script: scripts/add_persolusi.py (UNO; reads out/, writes out14/). 148 charts, 0 formula errors, 0 panes.

## Addendum 2 (23 Nov 2026, 15:50 WIB)
- FIXED: 414 chart series had legend names pointing at Indeks!B1 (UNO round trip); names restored from base build by data range (scripts/fix_charts.py, run LAST on every build). Same script converts all chart anchors to oneCellAnchor with fixed size (aspect ratio stable).
- New G_Opsi_Detail (Lembar 94, tab 2) + C_Deret_Opsi (Lembar 95): detailed year-based multi-source line charts per option (style of G_Perbandingan 47.1), headline in yellow cell. Script scripts/add_detail.py (out14 -> out15), then fix_charts.py. Row heights are locked (OptimalHeight False) so charts do not drift.
- C_Deret_Opsi uses NA() on purpose for chart gaps (about 1,080 #N/A cells). Options without yearly series (gas suar, CM2 tidak dirinci, CCS, efisiensi, B40) are noted, not charted.
- Pipeline order now: ... add_persolusi.py -> add_detail.py -> fix_charts.py -> strip panes. User rule: line charts only.

## Addendum 3: perbaikan grafik (24 Nov 2026)
- Penyebab: setiap simpan penuh lewat LibreOffice menulis ulang grafik (legenda jadi rujukan Indeks!$B$1, grouping dan smooth berubah) dan membuang freeze pane.
- Perbaikan: `scripts/graft.py` mencangkokkan definisi grafik asli dari `build/` (hasil generator) ke 122 grafik asli pada master, memakai rujukan data dan judul master. Hasil `cmp.py`: 0 grafik berbeda dari referensi unggahan (grouping, smooth, dash, marker, legenda). Nama seri rusak: 0 dari 595.
- 70 freeze pane dipulihkan dari `build/` (tanpa tabSelected).
- Urutan pipeline: build_nze -> UNO (add_persolusi, add_detail) -> fix_charts.py -> graft.py (terakhir, jangan simpan ulang lewat LibreOffice sesudahnya).
- #N/A sebanyak 1.083 sel di C_Deret_Opsi disengaja (celah garis XY).

## Addendum 4: aturan repo dan keadaan terbaru (24 Nov 2026)
- Berkas kerja terbaru selalu bernama `Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx` (nama lama "(4)" dihapus). Pengembangan spreadsheet dikerjakan di repo ini, skrip di `scripts/`, PDF di `sources/`, daftar riset di `RESEARCH_TODO.md`.
- Alur untuk setiap berkas baru: baca seluruhnya, ekstrak semua data, catat di `D_Register_Sumber`, proses ke lembar hitung atau `K_Konflik`, lalu tulis usulan pengembangan di `RESEARCH_TODO.md`.
- Edit workbook lewat XML langsung (jangan simpan ulang lewat LibreOffice atau openpyxl: grafik rusak). Tanpa freeze pane, satu tab terpilih, tanpa tanda pisah panjang.
- Keadaan: 96 lembar, 173 grafik, register 809 butir dari 24 dokumen, K_Konflik 107 butir (K25 sampai K132), lembar baru C_Biaya_Teknologi (Lembar 96).
- Hyperlink Indeks kini internal; sebelumnya menunjuk ke berkas "../Indonesia_NZE_Data_Grafik_v2.xlsx".

## Addendum 5 (24 Nov 2026)
- Lima PDF dari main dibaca dan dicatat; register 836 butir dari 28 dokumen; K_Konflik 116 butir (K25 sampai K141); A_Kesiapan_Solusi (Lembar 97): siap 19, siap setelah hitung ulang 1, kurang masukan 17, belum bisa 7.
- Skrip: scripts/06_audit_kesiapan.py, 07_log_five_new_pdfs.py, xlsxkit.py (tambah lembar lewat XML). Urutan: jalankan 06 lalu 07 bila membangun ulang dari keadaan sebelum audit.

## Addendum 6 (24 Nov 2026): model portofolio dibangun
- Workbook LATEST kini 127 lembar dan 249 grafik (173 lama tidak diubah, 76 baru). Dua tab pertama: P_Portofolio (Lembar 102) dan G_Portofolio (Lembar 103).
- Blok B (Lembar 98 sampai 101): garis pembangunan dari rencana (B_Pendorong), garis dan selisih SNDC (B_Garis_Pembangunan, B_Garis_NZE), selisih menurut penyebab dan CM1 belum terkirim (B_Selisih_Penyebab).
- Lembar solusi S_ (104 sampai 125): tujuh teknologi terbarukan dari RUPTL (RE Base dan ARED), rekap, sepuluh aksi FOLU, pensiun dini, CCS TJB, co-firing, B40. Setiap lembar: tabel teknis (tautan D_Teknis_Opsi), rantai hitung sederhana, biaya, investasi, pelaksanaan (kosong untuk tim), dan grafik dengan area berarsir, label titik, legenda sesuai sel, dan sumbu sekunder.
- K_Studi (126): JETP dibanding RUPTL (surya 29,2 GW JETP dibanding 4,5 GW RE Base dan 7,6 GW ARED pada 2030) dan angka per solusi menurut studi. Q_Portofolio (127): 8 dari 8 pemeriksaan lulus.
- Hasil utama 2030: energi resmi 37 persen, dengan turunan 66, dengan pihak ketiga 74 persen; sisa 61 MtCO2e belum punya solusi bersumber (B7 surya hanya sisa selisih). FOLU: turunan per aksi 50 sampai 87 persen, CM2 resmi 104 persen. Sisa CM1 yang harus dikirim menambah 157 sampai 207 MtCO2e.
- Pendorong terukur (PLTU on-grid dan PLTGU baru) baru menjelaskan 22 persen emisi energi CPOS 2030; minyak dan gas, transportasi, industri, gedung, captive (proyeksi), dan fugitive belum terukur (WP-A, C, E, I).
- Terbarukan RUPTL: ARED di atas RE Base hanya meningkatkan penggantian batubara sekitar 9 Mt pada 2030 (hitung sederhana), sedangkan RUPTL melaporkan selisih emisi batubara hanya 4 Mt (S_EBT_Rekap).
- Grafik dibuat lewat XML dan diuji hanya di LibreOffice; perlu satu putaran pemeriksaan di Excel.
- Register kini 842 butir dari 29 dokumen (tambah LCA biodiesel sawit, No 837 sampai 842). Urutan rakit: base git 41dafa7, lalu scripts/14_log_lca_biodiesel.py pada base, lalu scripts/13_assemble_model.py.

## Addendum 7 (24 Nov 2026): phase-down PLTU dan rice cooker
- Base rakit: git 41dafa7, lalu scripts/14, scripts/15, lalu scripts/13. Workbook 128 lembar dan 252 grafik. K_Konflik K25 sampai K146 (121 butir); A_Kesiapan: siap 20, siap setelah hitung ulang 1, kurang masukan 17, belum bisa 6.
- Phase-down: enam PLTU Fadiilah dan Dye (93,52 Mt; 14.310 MW) berbeda dari workbook GEM 16.735 MW (Suralaya 6.025 dibanding 4.025); intensitas 6,4 sampai 6,6 MtCO2 per GW pada tiga sumber, sehingga pensiun resmi 36 Mt setara sekitar 5,5 GW, dekat sensitivitas JETP 5,2 GW; semua jalur workbook (6,9 sampai 11,2 GW sampai 2030) lebih agresif daripada skenario utama JETP (nol). TJB (24,01 Mt) tumpang tindih dengan CCS TJB (13 Mt) bila dipensiunkan penuh.
- Rice cooker: LPG dihindari 21,9 sampai 48,9 ktCO2 dikurangi listrik 7,4 sampai 25,4 kt; netto -3,5 sampai 41,4 kt per tahun. Faktor LPG 3,16 menggantikan asumsi 2,98.
- Berkas serah terima tim dan template terisi yang disebut pengguna tidak ditemukan di repo.
