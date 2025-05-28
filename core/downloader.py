import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import hashlib
import re
from .utils import validate_url, make_valid_filename

class WebsiteDownloader:
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def update_progress(self, value, message):
        if self.progress_callback:
            self.progress_callback(value, message)
    
    def download(self, url, output_folder="downloaded_site"):
        try:
            if not validate_url(url):
                raise ValueError("Invalid URL format")

            self.update_progress(0, "Initializing download...")
            result = self._download_site(url, output_folder)
            self.update_progress(100, "Download complete!")
            return True, f"Website saved to {output_folder}"
        except Exception as e:
            self.update_progress(0, f"Error: {str(e)}")
            return False, str(e)
    
    def _download_site(self, url, output_folder):
        assets_folder = os.path.join(output_folder, "static")
        os.makedirs(assets_folder, exist_ok=True)

        self.update_progress(10, f"Downloading HTML from {url}")
        html = self._download_html(url)
        
        original_path = os.path.join(output_folder, "original_index.html")
        with open(original_path, "w", encoding="utf-8") as f:
            f.write(html)

        self.update_progress(20, "Analyzing page resources...")
        soup = BeautifulSoup(html, "html.parser")
        resources = self._parse_resources(url, soup)
        
        self.update_progress(30, "Downloading assets...")
        url_mapping = self._download_resources(resources, assets_folder)
        
        self.update_progress(70, "Updating file references...")
        html = self._update_resource_paths(html, url_mapping)
        
        self._process_css_files(url_mapping, assets_folder, output_folder)
        
        self.update_progress(90, "Saving results...")
        final_path = os.path.join(output_folder, "index.html")
        with open(final_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        return True

    def _download_html(self, url):
        response = requests.get(url, headers=self.headers, timeout=15)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text

    def _parse_resources(self, base_url, soup):
        resource_tags = soup.find_all(['img', 'link', 'script', 'source', 'style'])
        urls = set()

        for tag in resource_tags:
            if tag.name == 'img' and tag.get('src'):
                urls.add(urljoin(base_url, tag['src']))
            elif tag.name == 'link' and tag.get('href'):
                href = tag['href']
                urls.add(urljoin(base_url, href))
                if href.endswith('.css'):
                    try:
                        css_urls = self._parse_css_resources(urljoin(base_url, href))
                        urls.update(css_urls)
                    except Exception as e:
                        print(f"CSS processing error: {e}")
            elif tag.name == 'script' and tag.get('src'):
                urls.add(urljoin(base_url, tag['src']))
            elif tag.name == 'source' and tag.get('src'):
                urls.add(urljoin(base_url, tag['src']))
            elif tag.name == 'style':
                style_content = tag.string or ""
                urls.update(self._parse_inline_css(base_url, style_content))

        return urls

    def _parse_css_resources(self, css_url):
        response = requests.get(css_url, headers=self.headers)
        response.raise_for_status()
        css_content = response.text
        return self._parse_inline_css(css_url, css_content)

    def _parse_inline_css(self, base_url, css_content):
        urls = set()
        font_urls = re.findall(r'url\(([^)]+)\)', css_content)
        for font_url in font_urls:
            font_url = font_url.strip('"\'').split('?')[0].split('#')[0]
            if font_url.startswith(('http://', 'https://')):
                urls.add(font_url)
            else:
                urls.add(urljoin(base_url, font_url))
        return urls

    def _download_resources(self, resources, assets_folder):
        url_mapping = {}
        font_extensions = ('.woff', '.woff2', '.ttf', '.otf', '.eot')
        
        for i, url in enumerate(resources):
            try:
                self.update_progress(30 + int(50 * i/len(resources)), f"Downloading {url}")
                
                path = urlparse(url).path
                is_font = url.lower().endswith(font_extensions)
                filename = make_valid_filename(os.path.basename(path) or "resource.bin")
                
                if filename in url_mapping.values():
                    filename_hash = hashlib.md5(url.encode()).hexdigest()[:6]
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}_{filename_hash}{ext}"
                
                local_path = os.path.join(assets_folder, filename)
                
                if not os.path.exists(local_path):
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    with open(local_path, "wb") as f:
                        f.write(response.content)
                
                url_mapping[url] = f"static/{filename}"
            except Exception as e:
                print(f"Failed to download {url}: {e}")
        
        return url_mapping

    def _update_resource_paths(self, html, url_mapping):
        for url, local_path in url_mapping.items():
            html = html.replace(url, local_path)
        return html

    def _process_css_files(self, url_mapping, assets_folder, output_folder):
        for url, local_path in url_mapping.items():
            if url.endswith('.css'):
                css_path = os.path.join(output_folder, local_path.replace('static/', ''))
                if os.path.exists(css_path):
                    with open(css_path, 'r', encoding='utf-8') as f:
                        css_content = f.read()
                    
                    for font_url, font_local_path in url_mapping.items():
                        if any(font_url.lower().endswith(ext) for ext in ('.woff', '.woff2', '.ttf', '.otf', '.eot')):
                            css_content = css_content.replace(font_url, font_local_path)
                    
                    with open(css_path, 'w', encoding='utf-8') as f:
                        f.write(css_content)