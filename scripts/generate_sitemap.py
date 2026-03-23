import os
from datetime import datetime

BASE_URL = "https://minna-map.github.io"

def generate():
    urls = []
    lastmod = datetime.now().strftime('%Y-%m-%d')
    for root, dirs, files in os.walk("sites"):
        if "index.md" in files:
            path = os.path.relpath(root, "sites").replace(os.sep, "/")
            urls.append(f"<url><loc>{BASE_URL}/sites/{path}/</loc><lastmod>{lastmod}</lastmod></url>")

    with open("sitemap.xml", "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{"".join(urls)}</urlset>')

if __name__ == "__main__":
    generate()
