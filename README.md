## **Plugin ekstraktor [yt-dlp](https://github.com/yt-dlp/yt-dlp) untuk [animeinweb](https://animeinweb.com/). Mendukung pengunduhan episode tunggal, playlist lengkap, dan fitur pencarian langsung dari terminal.**

## **Instalasi**
```bash
python -m pip install -U https://github.com/yt-dlp-plugins/yt-dlp-animein/archive/main.zip
```

### **ARCH LINUX ONLY (Fast Way)**
```bash
git clone https://github.com/yt-dlp-plugins/yt-dlp-animein.git --depth=1 /tmp/yt-dlp-animein && cd /tmp/yt-dlp-animein && makepkg -sif
```
### **Uninstall**
**Gunakan pacman,jangan gunakan ~~sudo rm -rf / --no-preserve-root~~**
```bash
sudo pacman -Rns yt-dlp-animein --noconfirm
```
---

## **Cara penggunaan**
**Menggunakan kata kunci (Search):**
```bash
yt-dlp "animein:Kaifuku Jutsushi" -o "%(playlist_title)s/%(title)s.%(ext)s"
```

**Menggunakan URL langsung:**
```bash
yt-dlp "https://animeinweb.com/anime/1280" -o "%(playlist_title)s/%(title)s.%(ext)s"
```

**Mengabaikan episode yang tidak memiliki format video:**
```bash
yt-dlp --ignore-no-formats-error "https://animeinweb.com/anime/1280"
```
---

## **Streaming dengan [MPV](https://github.com/mpv-player/mpv)**
**Kamu bisa menonton langsung tanpa perlu mengunduh file:**
```bash
mpv --referrer="https://animeinweb.com/" "https://animeinweb.com/anime/4347"
```
### **Solusi Error `"No video formats found!"`**
**Jika menemukan error tersebut, gunakan flag tambahan berikut:**
```bash
mpv "https://animeinweb.com/anime/426" --ytdl-raw-options-append="ignore-no-formats-error=" --referrer="https://animeinweb.com/"
```
---
## **Tips: Automasi Referrer di mpv.conf**
**Tambahkan ini ke config MPV kamu agar tidak perlu mengetik referrer setiap saat:**
```conf
[animein]
profile-cond=path:find('storages%.animein%.net')
referrer="https://animeinweb.com/"

# opsional auto skip format yang error
ytdl-raw-options-append="ignore-no-formats-error="
```
**Cara Cepat (Copy-Paste ke Terminal):**
```bash
tee -a <<EOF >> ~/.config/mpv/mpv.conf
[animein]
profile-cond=path:find('storages%.animein%.net')
referrer="https://animeinweb.com/"
ytdl-raw-options-append="ignore-no-formats-error="
EOF
```
---

## **Dukung Proyek Ini ☕**
**Kalau ekstraktor ini ngebantu kamu hemat waktu, pertimbangkan buat traktir kopi biar saya semangat maintenance terus:** <!--tapi boong-->

<div align="left">

[![Trakteer](https://img.shields.io/badge/Trakteer-asep5k-red?style=for-the-badge&logo=trakteer&logoColor=white "Trakteer")](https://trakteer.id/asep5k) [![PayPal](https://img.shields.io/badge/PayPal-Donate-blue?style=for-the-badge&logo=paypal "PayPal")](https://paypal.me/rezaoctavian496) [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg "Ko-fi")](https://ko-fi.com/aspe)

</div>
