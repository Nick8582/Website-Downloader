import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import hashlib
import re
import argparse
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def download_site(url, output_folder="downloaded_site", depth=1, ignore_ssl=False, user_agent=None):
    """
    Download a website with all its resources.
    
    Args:
        url: Website URL to download
        output_folder: Output directory name
        depth: How many levels deep to crawl (not fully implemented in this version)
        ignore_ssl: Whether to ignore SSL certificate verification
        user_agent: Custom user agent string
    """
    assets_folder = os.path.join(output_folder, "static")
    os.makedirs(assets_folder, exist_ok=True)

    print(f"🔽 Downloading HTML from {url}")
    
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1)
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    headers = {"User-Agent": user_agent or "Mozilla/5.0"}
    verify_ssl = not ignore_ssl
    
    try:
        if ignore_ssl:
            requests.packages.urllib3.disable_warnings()
            ssl._create_default_https_context = ssl._create_unverified_context

        response = session.get(url, headers=headers, timeout=15, verify=verify_ssl)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.text
    except Exception as e:
        print(f"❌ Error downloading HTML: {e}")
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
                    css_response = session.get(urljoin(url, href), headers=headers, verify=verify_ssl)
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
                    print(f" ❌ Error processing CSS {href}: {e}")
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

    print(f"🔍 Found {len(urls)} resources (including {len(font_urls)} fonts)")

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
                print(f" → Downloading: {res_url}")
                r = session.get(res_url, timeout=15, headers=headers, verify=verify_ssl)
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    f.write(r.content)
            
            return f"static/{filename}"
        except Exception as e:
            print(f" ❌ Error processing {res_url}: {e}")
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

    print(f"\n✅ Done! Files saved to: {output_folder}")
    print(f"Main page: {final_path}")
    print(f"Resources: {assets_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Website Downloader')
    parser.add_argument('url', help='URL of the website to download')
    parser.add_argument('-o', '--output', default='downloaded_site', 
                       help='Output directory (default: downloaded_site)')
    parser.add_argument('-d', '--depth', type=int, default=1,
                       help='Crawl depth (default: 1)')
    parser.add_argument('--ignore-ssl', action='store_true',
                       help='Ignore SSL certificate verification')
    parser.add_argument('-u', '--user-agent', 
                       help='Custom user agent string')
    args = parser.parse_args()
    
    if not args.url:
        print("⚠️ URL is required")
    else:
        download_site(
            args.url,
            output_folder=args.output,
            depth=args.depth,
            ignore_ssl=args.ignore_ssl,
            user_agent=args.user_agent
        )