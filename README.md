<div align="center">
<!--makasih bang gemini---> 
    <img src="./assets/logo.png" 
       width="250" 
       alt="wibu-downloader logo"
       style="border-radius: 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">

[![Python 3.11+](https://img.shields.io/badge/Python-3.13.11+-blue?logo=python?&style=for-the-badge)](https://python.org "Python blyad")
[![PyPI](https://img.shields.io/badge/-PyPI-blue.svg?logo=pypi&labelColor=555555&style=for-the-badge)](https://pypi.org/project/wibu-downloader/ "PyPI")
[![yt-dlp](https://img.shields.io/badge/yt--dlp-2025.12.08+-red?&style=for-the-badge)](https://github.com/yt-dlp/yt-dlp "yt-dlp")
[![License](https://img.shields.io/badge/License-GPLv3-green?&style=for-the-badge)](LICENSE "LICENSE")
[![Issues](https://img.shields.io/github/issues/Asep5K/asepplugins?color=orange&style=for-the-badge)](https://github.com/Asep5K/asepplugins/issues "issues")
[![Piracy Level](https://img.shields.io/badge/Piracy-100%25-black?label=piracy&style=for-the-badge)](https://en.wikipedia.org/wiki/Piracy "Bajakan njir")
[![DMCA Shield](https://img.shields.io/badge/DMCA-Proof-red?label=dmca&style=for-the-badge)](https://www.dmca.com/ "DMCA")

# **wibu-downloader, custom extractor yt-dlp**
## **Custom extractor untuk mendownload/menonton anime**
</div>

## **INSTALASI**
**Via PyPI**

    pip install -U wibu-downloader

**Atau**

    python -m pip install -U https://github.com/Asep5K/wibu-downloader/archive/main.zip

## **Cara penggunaan**
### ⚠️ Sangat disarankan menggunakan `--output '%(playlist_title)s/%(title)s.%(ext)s'`

    # Download anime (pake keyword)
    yt-dlp 'animein:Kaifuku Jutsushi no Yarinaoshi' --output '%(playlist_title)s/%(title)s.%(ext)s'

    # Download pake link langsung
    yt-dlp 'https://animeinweb.com/anime/1280' --output '%(playlist_title)s/%(title)s.%(ext)s'

    # Skip episode yang error
    yt-dlp --ignore-no-formats-error 'https://animeinweb.com/anime/1280' --output '%(playlist_title)s/%(title)s.%(ext)s'


## 🎯 **Pemilihan Resolusi**

### **Cara 1: Pake Filter (Rekomendasi)**
Pilih resolusi berdasarkan tinggi, otomatis ambil yang terbaik:

    # Maksimal 1080p (kalo ada)
    yt-dlp -f '[height<=1080]' <URL>

    # Maksimal 720p (hemat kuota)
    yt-dlp -f '[height<=720]' <URL>

### **Cara 2: Pake Format ID (Kontrol Manual)**
| Kode | Resolusi | Cocok buat |
|------|----------|------------|
| `18` | 360p     | Kuota tipis, streaming lancar |
| `35` | 480p     | DVD quality, middle ground |
| `22` | 720p     | HD, keseimbangan kualitas & ukuran |
| `37` | 1080p    | Full HD, buat yang mau bening |

    # Ambil resolusi 720p aja (kalo gak ada ya error)
    yt-dlp -f 22 <URL>

    # Prioritaskan 1080p, kalo gak ada turun ke 720p, terakhir 480p
    yt-dlp -f 37/22/35 <URL>

    # Ambil yang terbaik (biasanya 1080p)
    yt-dlp -f best <URL>


## **TONTON LANGSUNG MENGGUNAKAN [MPV](https://github.com/mpv-player/mpv)**
### **Contoh penggunaan:**

    mpv --referrer=https://animeinweb.com/ 'https://animeinweb.com/anime/4347'

### **Error `"No video formats found!"`**

    [ytdl_hook] ERROR: [animeinweb] 7138: No video formats found!; please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the appropriate issue template. Confirm you are on the latest version using  yt-dlp -U
    [ytdl_hook] youtube-dl failed: unexpected error occurred
    [cplayer] finished playback, unrecognized file format (reason 4)
    [cplayer] Failed to recognize file format.

### **Gunakan flag  `--ytdl-raw-options-append='ignore-no-formats-error='`**

    mpv --ytdl-raw-options-append='ignore-no-formats-error=' 'https://animeinweb.com/anime/426'

## **❓ FAQ (Frequently Asked "Gimana nih?!")**
Q: Kok masih error "No video formats found"?    
A: [Report bug langsung di sini](https://github.com/Asep5K/wibu-downloader/issues/new) (Kasih URL yang error + log yt-dlp/mpv)


Q: Episode urutannya aneh?  
A: Udah gw reverse biar episode 1 dulu, kalo masih aneh ya namanya juga API-nya random

Q: Bisa download batch semua episode?   
A: Bisa! Tapi siapin storage & kuota yang banyak ya

## **Educational Purpose Only**
Code ini dibuat untuk pembelajaran:
- HTTP requests handling
- JSON parsing
- Video format extraction
- Web technology study

## **Profit! (for you, not for me 😂)**
