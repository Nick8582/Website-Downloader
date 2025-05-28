# Website Downloader

📥 Кроссплатформенное приложение для скачивания веб-сайтов

## 📦 Установка

### Для пользователей

1. Перейдите в [раздел Releases](https://github.com/Nick8582/Website-Downloader/releases)
2. Скачайте версию для вашей ОС:
   - **Windows**: `WebsiteDownloader.exe`
   - **macOS**: `WebsiteDownloader.app.zip`
   - **Linux**: `website-downloader`

### Для разработчиков

```bash
git clone https://github.com/Nick8582/Website-Downloader.git
cd website-downloader
pip install -r requirements.txt
```

## 🚀 Запуск

### Windows

1. Скачайте `WebsiteDownloader.exe`
2. Запустите двойным кликом

### macOS

1. Скачайте `WebsiteDownloader.app.zip`
2. Распакуйте архив
3. Запустите приложение (возможно потребуется: `xattr -cr WebsiteDownloader.app`)

### Linux

```bash
chmod +x website-downloader
./website-downloader
```

## 🛠 Сборка из исходников

```bash
# Windows
cd build
build_windows.bat

# macOS
cd build
chmod +x build_mac.sh
./build_mac.sh

# Linux
cd build
chmod +x build_linux.sh
./build_linux.sh
```
