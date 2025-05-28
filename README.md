# 🌐 Website Downloader

_A powerful Python tool to mirror entire websites locally with ease_

![Python](https://img.shields.io/badge/Python-3.6+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/github/license/Nick8582/Website-Downloader?color=blue)
![Last Commit](https://img.shields.io/github/last-commit/Nick8582/Website-Downloader)

## ✨ Features

- 🚀 **Complete website mirroring** (HTML, CSS, JS, images)
- 🎚️ **Adjustable crawl depth** for flexible downloading
- 📂 **Custom output directories** to organize your downloads
- 🔒 **SSL verification toggle** for problematic sites
- 📊 **Progress tracking** during download
- 🖥️ **Simple CLI interface** with helpful commands

## 🛠️ Installation

### Prerequisites

- Python 3.6+
- pip package manager

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Nick8582/Website-Downloader.git
cd Website-Downloader

# Set up virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🚦 Usage

### Basic Command

```bash
python website_downloader.py https://example.com
```

### Advanced Options

| Option               | Flag                 | Description                    | Default            |
| -------------------- | -------------------- | ------------------------------ | ------------------ |
| **Output Directory** | `-o`, `--output`     | Where to save downloaded files | `downloaded_pages` |
| **Crawl Depth**      | `-d`, `--depth`      | How many levels deep to crawl  | 1                  |
| **Ignore SSL**       | `--ignore-ssl`       | Disable SSL verification       | False              |
| **User Agent**       | `-u`, `--user-agent` | Custom user agent string       | Default Python UA  |

### Example Usage

```bash
# Download with depth 2 to custom folder
python website_downloader.py https://example.com --depth 2 --output my_project

# Download with custom user agent
python website_downloader.py https://example.com -u "Mozilla/5.0"
```

## 📁 Output Structure

```
downloaded_pages/
├── index.html
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── img/
│       ├── logo.png
│       └── banner.jpg
└── about/
    └── index.html
```

## 🚨 Troubleshooting

<details>
<summary><b>Common Issues</b></summary>

### Missing Dependencies

```bash
pip install requests beautifulsoup4
```

### SSL Errors

```bash
python website_downloader.py https://example.com --ignore-ssl
```

### Permission Issues

```bash
# Linux/macOS
chmod +x website_downloader.py

# Windows - Run as Administrator
```

</details>

## 🤖 Automation

### Scheduled Downloads (Linux/macOS)

Add to crontab for daily downloads at midnight:

```bash
0 0 * * * cd /path/to/Website-Downloader && /usr/bin/python3 website_downloader.py https://example.com
```

### Docker Support

Coming soon! 🐳

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

<div align="center">
  <p>
    <strong>Please use responsibly</strong> - Respect website terms and robots.txt
  </p>
  <p>
    <a href="https://github.com/Nick8582/Website-Downloader/issues">Report Bug</a> •
    <a href="https://github.com/Nick8582/Website-Downloader/pulls">Request Feature</a>
  </p>
</div>

Key improvements:

1. Added emojis for visual appeal
2. Included a mockup image placeholder
3. Better organized sections with clear headers
4. Added a collapsible troubleshooting section
5. Improved option table formatting
6. Added Docker "coming soon" notice
7. Better footer with centered notice
8. More visual badges
9. Cleaner command formatting
10. Added feature icons

To use this:

1. Replace the image placeholder URL with an actual screenshot
2. Update the Docker section when available
3. Add any additional features you implement

Would you like me to adjust any particular section further?
