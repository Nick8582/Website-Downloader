from setuptools import setup, find_packages

setup(
    name="website-downloader",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests", "beautifulsoup4", "tqdm"],
    entry_points={
        'console_scripts': [
            'website-downloader=website_downloader.cli:main',
        ],
    }
)