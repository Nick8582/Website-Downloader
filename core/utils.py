import os
import re
from urllib.parse import urlparse

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def make_valid_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
    filename = filename.strip(". ")
    return filename[:100] if filename else "file"

def ensure_directory(path):
    os.makedirs(path, exist_ok=True)
    return path