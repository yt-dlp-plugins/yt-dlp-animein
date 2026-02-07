
[![Python 3.11+](https://img.shields.io/badge/Python-3.13.11+-blue?logo=python)](https://python.org)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-2025.12.08+-red)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-GPLv3-green)](LICENSE)
[![Issues](https://img.shields.io/github/issues/Asep5K/asepplugins?color=orange)](https://github.com/Asep5K/asepplugins/issues)
[![Piracy Level](https://img.shields.io/badge/Piracy-100%25-black)](https://en.wikipedia.org/wiki/Piracy)
<!-- [![Piracy](https://img.shields.io/badge/Content-100%25_Pirated-black)](https://www.dmca.com/) -->
[![DMCA Shield](https://img.shields.io/badge/DMCA-Proof-red)](https://www.dmca.com/)
[![Wibu Level](https://img.shields.io/badge/Wibu-Maximum-orange)](https://knowyourmeme.com/memes/wibu)

# yt-dlp animein Extractor
YA INI BUAT DOWNLOAD & NONTON ANIME SUB INDO!

Note:
1. Jangan jual kontennya  
2. Tetap dukung industri legit
3. I use arch btw 🤓

Dosa tanggung sendiri ya wibu! 🙏
>⚠️ Use at your own risk!


## INSTALASI
### Manual (lebih wibu)
```bash
mkdir -p ~/.config/yt-dlp/plugins

git clone https://github.com/Asep5K/wibu-downloader.git ~/.config/yt-dlp/plugins/wibu-downloader
```

### Atau pake pip (kurang wibu)
```bash
python -m pip install -U https://github.com/Asep5K/wibu-downloader/archive/main.zip
# Atau:
python -m pip install git+https://github.com/Asep5K/wibu-downloader.git
```

## CARA PENGGUNAAN

### ⚠️ sangat di sarankan menggunakan --output '%(playlist_title)s/%(title)s'
```bash
# Download anime bajakan
yt-dlp 'animein:Kaifuku Jutsushi no Yarinaoshi' --output '%(playlist_title)s/%(title)s'

# Pilih kualitas bajakan
yt-dlp -f '[height<=1080]' 'animein:Kaifuku Jutsushi no Yarinaoshi' --output '%(playlist_title)s/%(title)s'

# Menggunakan link
yt-dlp 'https://animeinweb.com/anime/1280' --output '%(playlist_title)s/%(title)s'

# Pake flag ini biar skip episode yang error:
yt-dlp --ignore-no-formats-error 'https://animeinweb.com/anime/1280'
```

## TONTON LANGSUNG MENGGUNAKAN MPV!!
### Download [mpv disini](https://github.com/mpv-player/mpv)

**Good news!** Ga perlu pake script [animein.lua](./mpv-scripts/animein.lua) lagi. Bisa di-uninstall/deleted!    
**Sangat di sarankan di delete saja!**

**Contoh penggunaan:**
```bash
mpv 'https://animeinweb.com/anime/4347'

# Ambil hanya resolusi kurang dari atau sama dengan 720p
mpv --ytdl-format='[height<=720]' 'https://animeinweb.com/anime/4347'
```

### Jika mengalami error
**Contoh error:**
```
$ mpv 'https://animeinweb.com/anime/6222'
    Playing: https://storages.animein.net/Kizoku%20Tensei%3A%20Megumareta%20Umare%20kara%20Saikyou%20no%20Chikara%20wo%20Eru%2F1-1080p-1767541103168.mp4
    [ffmpeg] https: HTTP error 403 Forbidden
    Failed to open https://storages.animein.net/Kizoku%20Tensei%3A%20Megumareta%20Umare%20kara%20Saikyou%20no%20Chikara%20wo%20Eru%2F1-1080p-1767541103168.mp4.
    Playing: https://storages.animein.net/Kizoku%20Tensei%3A%20Megumareta%20Umare%20kara%20Saikyou%20no%20Chikara%20wo%20Eru%2F2-1080p-1768145495797.mp4
    [ffmpeg] https: HTTP error 403 Forbidden
    Failed to open https://storages.animein.net/Kizoku%20Tensei%3A%20Megumareta%20Umare%20kara%20Saikyou%20no%20Chikara%20wo%20Eru%2F2-1080p-1768145495797.mp4.
    Exiting... (Quit)
```
### Gunakan user-agent
```
$ mpv --user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36' 'https://animeinweb.com/anime/6222'
    Playing: https://storages.animein.net/Kizoku%20Tensei%3A%20Megumareta%20Umare%20kara%20Saikyou%20no%20Chikara%20wo%20Eru%2F1-1080p-1767541103168.mp4
     ● Video  --vid=1  (h264 1920x1080 23.976 fps) [default]
     ● Audio  --aid=1  (aac 2ch 48000 Hz 192 kbps) [default]
    [modernz] URL detected.
    [modernz] Fetching file size...
    Using hardware decoding (vaapi).
    [autoconvert] Converting vaapi[nv12] -> vaapi[rgb0]
    AO: [pipewire] 48000Hz stereo 2ch floatp
    VO: [dmabuf-wayland] 1920x1080 vaapi[rgb0]
    [modernz] Download size: 258.588 MiB
    AV: 00:00:02 / 00:23:42 (0%) A-V:  0.007 DS: 2.5938/1 Cache: 18s/2MB
    Exiting... (Quit)
```

### Error "No video formats found!"
```
[ytdl_hook] ERROR: [animeinweb] 7138: No video formats found!; please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the appropriate issue template. Confirm you are on the latest version using  yt-dlp -U
[ytdl_hook] youtube-dl failed: unexpected error occurred
[cplayer] finished playback, unrecognized file format (reason 4)
[cplayer] Failed to recognize file format.
```
### Gunakan flag  --ytdl-raw-options-set='ignore-no-formats-error='
```
mpv --ytdl-raw-options-append='ignore-no-formats-error=' 'https://animeinweb.com/anime/426'
```


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
