import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import hashlib
import re

def download_site(url, output_folder="downloaded_site"):
    assets_folder = os.path.join(output_folder, "static")
    os.makedirs(assets_folder, exist_ok=True)

    print(f"🔽 Скачиваю HTML с {url}")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.text
    except Exception as e:
        print(f"❌ Ошибка при загрузке HTML: {e}")
        return

    original_path = os.path.join(output_folder, "original_index.html")
    with open(original_path, "w", encoding="utf-8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")

    resource_tags = soup.find_all(['img', 'link', 'script', 'source', 'style'])
    urls = set()

    for tag in resource_tags:
        if tag.name == 'img' and tag.get('src'):
            urls.add(urljoin(url, tag['src']))
        elif tag.name == 'link' and tag.get('href'):
            href = tag['href']
            urls.add(urljoin(url, href))
            if href.endswith('.css'):
                try:
                    css_response = requests.get(urljoin(url, href), headers=headers)
                    css_response.raise_for_status()
                    css_content = css_response.text
                    font_urls = re.findall(r'url\(([^)]+)\)', css_content)
                    for font_url in font_urls:
                        font_url = font_url.strip('"\'').split('?')[0].split('#')[0]
                        if font_url.startswith(('http://', 'https://')):
                            urls.add(font_url)
                        else:
                            urls.add(urljoin(urljoin(url, href), font_url))
                except Exception as e:
                    print(f" ❌ Ошибка при обработке CSS {href}: {e}")
        elif tag.name == 'script' and tag.get('src'):
            urls.add(urljoin(url, tag['src']))
        elif tag.name == 'source' and tag.get('src'):
            urls.add(urljoin(url, tag['src']))
        elif tag.name == 'style':
            style_content = tag.string or ""
            font_urls = re.findall(r'url\(([^)]+)\)', style_content)
            for font_url in font_urls:
                font_url = font_url.strip('"\'').split('?')[0].split('#')[0]
                if font_url.startswith(('http://', 'https://')):
                    urls.add(font_url)
                else:
                    urls.add(urljoin(url, font_url))

    font_extensions = ('.woff', '.woff2', '.ttf', '.otf', '.eot')
    other_resources = [u for u in urls if not u.lower().endswith(font_extensions)]
    font_urls = [u for u in urls if u.lower().endswith(font_extensions)]

    print(f"🔍 Найдено {len(urls)} ресурсов (включая {len(font_urls)} шрифтов)")

    url_to_local = {}
    
    def download_resource(res_url, is_font=False):
        try:
            path = urlparse(res_url).path
            original_filename = os.path.basename(path) or "resource.bin"
            
            if is_font:
                filename = original_filename
            else:
                if original_filename in url_to_local.values():
                    filename_hash = hashlib.md5(res_url.encode()).hexdigest()[:8]
                    filename, ext = os.path.splitext(original_filename)
                    filename = f"{filename}_{filename_hash}{ext}"
                else:
                    filename = original_filename
            
            local_path = os.path.join(assets_folder, filename)
            
            if not os.path.exists(local_path):
                print(f" → Скачиваю: {res_url}")
                r = requests.get(res_url, timeout=15, headers=headers)
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    f.write(r.content)
            
            return f"static/{filename}"
        except Exception as e:
            print(f" ❌ Ошибка при обработке {res_url}: {e}")
            return None

    for font_url in font_urls:
        local_path = download_resource(font_url, is_font=True)
        if local_path:
            url_to_local[font_url] = local_path

    for res_url in other_resources:
        local_path = download_resource(res_url)
        if local_path:
            url_to_local[res_url] = local_path

    for res_url, local_path in url_to_local.items():
        html = html.replace(res_url, local_path)

    css_files = [u for u in url_to_local if u.endswith('.css')]
    for css_url in css_files:
        local_css_path = os.path.join(output_folder, url_to_local[css_url].replace('static/', ''))
        if os.path.exists(local_css_path):
            with open(local_css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            for font_url, local_font_path in url_to_local.items():
                if font_url in font_urls:
                    css_content = css_content.replace(font_url, local_font_path)
            
            with open(local_css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)

    final_path = os.path.join(output_folder, "index.html")
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Готово! Файлы сохранены в папку: {output_folder}")
    print(f"Главная страница: {final_path}")
    print(f"Ресурсы: {assets_folder}")

if __name__ == "__main__":
    input_url = input("Введите URL сайта: ").strip()
    folder_name = input("Введите имя папки для сохранения (по умолчанию 'downloaded_site'): ").strip()
    
    if not input_url:
        print("⚠️ Не указана ссылка.")
    else:
        download_site(input_url, folder_name if folder_name else "downloaded_site")