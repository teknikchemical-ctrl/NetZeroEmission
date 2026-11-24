# scripts: pipeline pembangunan workbook (edit XML langsung, bukan simpan ulang LibreOffice atau openpyxl)

Urutan (tiap skrip memakai pustaka xlsxkit, modelkit, chartkit, src):
- 01 sampai 08: perbaikan grafik dan pane, pencatatan sumber, audit (lihat nama berkas).
- 09_build_model_B.py: Lembar 98 sampai 101 (B_Pendorong, B_Garis_Pembangunan, B_Garis_NZE, B_Selisih_Penyebab).
- 10_build_model_P.py: Lembar 102 dan 103 (P_Portofolio, G_Portofolio).
- 11_build_model_S.py: Lembar 104 sampai 121 (tujuh teknologi terbarukan, rekap, sepuluh aksi FOLU).
- 12_build_model_X.py: Lembar 122 sampai 127 (pensiun dini, CCS TJB, co-firing, B40, K_Studi, Q_Portofolio).
- 14_log_lca_biodiesel.py: catat LCA biodiesel ke register pada berkas base SEBELUM 13 dijalankan (`python3 scripts/14_log_lca_biodiesel.py /tmp/claude-0/base_model.xlsx`).
- 15_patch_phasedown_audit.py: tambah K142 sampai K146 dan perbarui audit rice cooker dan LPG pada berkas base SEBELUM 13.
- 13_assemble_model.py: merakit semuanya: `python3 scripts/13_assemble_model.py /path/Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx`. Base: lihat baris pertama berkas (git show <commit>:...). LibreOffice hanya dipakai untuk MENGHITUNG nilai cache rumus (dua putaran); berkas tidak disimpan oleh LibreOffice.

Pustaka: `xlsxkit.py` (tambah lembar, grafik, Indeks lewat XML), `modelkit.py` (DSL lembar dan hitung cache), `chartkit.py` (grafik garis dengan area berarsir, label titik, sumbu sekunder), `src.py` (pencari sel sumber).
Alat uji: `audit_charts.py`, `render_charts_libreoffice.py`, `check_formulas_libreoffice.py`.

`verify_all_sources.py`: pencocokan semua angka register dengan teks PDF di sources/ (ekstrak teks ke /tmp/claude-0/alltxt dahulu dengan pdftotext).
