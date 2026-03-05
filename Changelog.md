# Changelog

## [2.2.5] - 2026-03-06

### Features
- **Penambahan fitur caching** 🚀
  - Sebelumnya: setiap request (play/download/cek format) harus download info JSON dari server → boros request & lama
  - Sekarang: info JSON otomatis tersimpan di `$XDG_CACHE_HOME/yt-dlp/animein/`
  - Manfaat: 
    - ✅ 500 episode Naruto langsung play tanpa nunggu **jika sudah adda cache JSON nya!**
    - ✅ Hemat bandwidth server
    - ✅ Cepet kayak jet

### Note
  - Hapus cache: `yt-dlp --rm-cache-dir`
  - caching tidak berlaku jika menggunakan flag `--no-cache-dir`

### Changed
- **Bump version** dari 2.2.4 ke 2.2.5 (biar makin wuz wuz wuz)

---

## [2.2.4] - 2026-03-03

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
