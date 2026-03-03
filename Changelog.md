# Changelog

## [2.2.4] - 2026-03-04

### Fixed
- **Playlist extraction logic**
  - Sebelumnya: `--playlist-items N` tetap mengekstrak SEMUA episode (boros resource dan kelamaan)
  - Sekarang: Berhenti setelah episode ke-N, dan langsung memulai download
  
- **Urutan episode terbalik**
  - Episode terakhir malah diekstrak pertama
  - Diperbaiki dengan **menghitung jumlah halaman berdasarkan total episode**

### Changed
- **Yuk naikin versi** dari 2.1.4 ke 2.2.4 (karena bug fix minor)

---
