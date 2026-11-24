# Catatan dan data per sumber

- `INVENTARIS_SUMBER.csv`: induk semua sumber (PDF, CSV) dengan ID (S001 dan seterusnya; X001 dan X002 untuk sumber tanpa berkas), jenis, WP, kedalaman baca, jumlah butir register, jalur catatan dan data. Sama dengan lembar `D_Sumber` di workbook.
- `sumber/Sxxx.md`: satu catatan per sumber (metadata, SHA-256, konteks, abstrak dan kesimpulan hasil ekstrak, butir yang tercatat, catatan peninjau).
- `../data/per_sumber/Sxxx.csv`: butir `D_Register_Sumber` untuk sumber itu (satu berkas per sumber yang punya butir).
- Kedalaman baca: A angka diverifikasi pada PDF atau CSV; B abstrak dan kesimpulan ditinjau dan ringkasan tim; C diarsip, konteks dari ringkasan tim. Sumber berkedalaman B atau C belum dibaca penuh; bagian yang tidak tertulis belum dibaca.
- Dibuat ulang oleh `scripts/19_inventaris_sumber.py` lalu `scripts/20_catatan_sumber.py` (jalankan setelah workbook dirakit). Lembar data dan grafik dibuat oleh `scripts/21_build_data_sheets.py`.
