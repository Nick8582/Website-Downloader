# Website Downloader

![GitHub stars](https://img.shields.io/github/stars/Nick8582/Website-Downloader?style=social)
![GitHub forks](https://img.shields.io/github/forks/Nick8582/Website-Downloader?style=social)
![GitHub license](https://img.shields.io/github/license/Nick8582/Website-Downloader)

Website Downloader - это инструмент для скачивания веб-сайтов целиком с сохранением структуры и содержимого.

## 📌 Возможности

- Скачивание всего сайта или отдельных страниц
- Сохранение структуры директорий и файлов
- Поддержка рекурсивного скачивания
- Настройка глубины скачивания
- Фильтрация по типам файлов
- Поддержка пользовательских заголовков HTTP

## 🚀 Установка

### Требования

- Python 3.6+
- Установленные зависимости (см. раздел "Зависимости")

### Установка из репозитория

```bash
git clone https://github.com/Nick8582/Website-Downloader.git
cd Website-Downloader
pip install -r requirements.txt
```

## 🛠 Использование

### Базовое использование

```bash
python website_downloader.py [URL] [OPTIONS]
```

### Примеры

```bash
# Скачать сайт с глубиной 2
python website_downloader.py https://example.com --depth 2

# Скачать только HTML-страницы
python website_downloader.py https://example.com --filter html
```

### Доступные параметры

```
--depth N          Установить глубину скачивания (по умолчанию: 1)
--output DIR       Указать директорию для сохранения (по умолчанию: ./downloads)
--filter TYPE      Фильтровать по типу файлов (html, css, js, img)
--user-agent STR   Установить пользовательский User-Agent
--delay SEC        Задержка между запросами (в секундах)
--help             Показать справку
```

## 📂 Структура проекта

```
Website-Downloader/
├── website_downloader.py  # Основной скрипт
├── config.py              # Конфигурационные параметры
├── utils/                 # Вспомогательные модули
│   ├── downloader.py      # Логика скачивания
│   ├── parser.py          # Парсинг HTML
│   └── file_utils.py      # Работа с файлами
├── requirements.txt       # Зависимости
└── README.md              # Этот файл
```

## 📦 Зависимости

Основные зависимости:

- `requests` - для HTTP-запросов
- `beautifulsoup4` - для парсинга HTML
- `urllib3` - для работы с URL

Установить все зависимости:

```bash
pip install -r requirements.txt
```

## 🤝 Как внести вклад

1. Форкните репозиторий
2. Создайте ветку с вашими изменениями (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте изменения (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📜 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

## ✉️ Контакты

Автор: Nick8582  
Вопросы и предложения: [открыть issue](https://github.com/Nick8582/Website-Downloader/issues)
