<div align="center">

[![Python 3.11+](https://img.shields.io/badge/Python-3.13.11+-blue?logo=python?&style=for-the-badge)](https://python.org "Python")
[![PyPI](https://img.shields.io/badge/-PyPI-blue.svg?logo=pypi&labelColor=555555&style=for-the-badge)](https://pypi.org/project/wibu-downloader/ "PyPI")
[![yt-dlp](https://img.shields.io/badge/yt--dlp-2025.12.08+-red?&style=for-the-badge)](https://github.com/yt-dlp/yt-dlp "yt-dlp")
[![License](https://img.shields.io/badge/License-GPLv3-green?&style=for-the-badge)](LICENSE)
[![Issues](https://img.shields.io/github/issues/Asep5K/asepplugins?color=orange&style=for-the-badge)](https://github.com/Asep5K/asepplugins/issues)
[![Piracy Level](https://img.shields.io/badge/Piracy-100%25-black?label=piracy&style=for-the-badge)](https://en.wikipedia.org/wiki/Piracy "Bajakan njir")
[![DMCA Shield](https://img.shields.io/badge/DMCA-Proof-red?label=dmca&style=for-the-badge)](https://www.dmca.com/)

</div>

# yt-dlp animein Extractor

## INSTALASI
**Via PyPI**

    pip install -U wibu-downloader

**Atau**

    python -m pip install -U https://github.com/Asep5K/wibu-downloader/archive/main.zip


## CARA PENGGUNAAN

### ⚠️ sangat di sarankan menggunakan --output '%(playlist_title)s/%(title)s.%(ext)s'

    # Download anime bajakan
    yt-dlp 'animein:Kaifuku Jutsushi no Yarinaoshi' --output '%(playlist_title)s/%(title)s.%(ext)s'

    # Pilih kualitas bajakan
    yt-dlp -f '[height<=1080]' 'animein:Kaifuku Jutsushi no Yarinaoshi' --output '%(playlist_title)s/%(title)s.%(ext)s'

    # Menggunakan link
    yt-dlp 'https://animeinweb.com/anime/1280' --output '%(playlist_title)s/%(title)s.%(ext)s'

    # Pake flag ini biar skip episode yang error:
    yt-dlp --ignore-no-formats-error 'https://animeinweb.com/anime/1280' --output '%(playlist_title)s/%(title)s.%(ext)s'

**Pemilihan resolusi bisa menggunakan format berikut**:

* `18`: `360p` 
* `35`: `480p` 
* `22`: `720p` 
* `37`: `1080p` 


## TONTON LANGSUNG MENGGUNAKAN MPV!!
### Download [mpv disini](https://github.com/mpv-player/mpv)
**Contoh penggunaan:**

    mpv --referrer=https://animeinweb.com/ 'https://animeinweb.com/anime/4347'

### Error `"No video formats found!"`

    [ytdl_hook] ERROR: [animeinweb] 7138: No video formats found!; please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the appropriate issue template. Confirm you are on the latest version using  yt-dlp -U
    [ytdl_hook] youtube-dl failed: unexpected error occurred
    [cplayer] finished playback, unrecognized file format (reason 4)
    [cplayer] Failed to recognize file format.

### Gunakan flag  `--ytdl-raw-options-append='ignore-no-formats-error='`

    mpv --ytdl-raw-options-append='ignore-no-formats-error=' 'https://animeinweb.com/anime/426'



## ❓ FAQ (Frequently Asked "Gimana nih?!")
Q: Kok masih error "No video formats found"?   
A: [Report bug langsung di sini](https://github.com/Asep5K/wibu-downloader/issues/new) (Kasih URL yang error + log yt-dlp/mpv)

Q: Playlist urutannya aneh?  
A: Udah gw reverse biar episode 1 dulu, kalo masih aneh ya namanya juga API-nya random

Q: Bisa download batch semua episode?  
A: Bisa! Tapi siapin storage & kuota yang banyak ya

## Educational Purpose Only
Code ini dibuat untuk pembelajaran:
- HTTP requests handling
- JSON parsing
- Video format extraction
- Web technology study

## Profit! (for you, not for me 😂)
