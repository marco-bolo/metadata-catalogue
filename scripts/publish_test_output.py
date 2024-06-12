import os
import shutil
from datetime import date


folders = [x for x in os.listdir(os.path.join("scripts", "tests", "output"))]
urls = []

for folder in folders:

    output_dir = os.path.join("datasets", folder)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = [x for x in os.listdir(os.path.join("scripts", "tests", "output", folder))]
    for file in files:
        urls.append(f"https://raw.githubusercontent.com/marco-bolo/dataset-catalogue/main/datasets/{folder}/{file}")
        shutil.copyfile(os.path.join("scripts", "tests", "output", folder, file), os.path.join(output_dir, file))

today = date.today().strftime("%Y-%m-%d")

with open(os.path.join("datasets", "sitemap.xml"), "w") as f:
    f.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\" xmlns:xhtml=\"http://www.w3.org/1999/xhtml\">\n")
    for url in urls:
        f.write(f"<url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq></url>\n")
    f.write("</urlset>")
