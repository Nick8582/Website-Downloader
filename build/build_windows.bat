@echo off
pyinstaller --onefile --windowed --name WebsiteDownloader --icon=../assets/icon.ico --add-data "../assets/icon.ico;assets" ../main.py
pause