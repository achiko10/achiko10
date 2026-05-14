
import os
import re

html_path = 'tafti/index.html'
root_dir = os.getcwd()

if not os.path.exists(html_path):
    print(f"Error: {html_path} not found")
    exit(1)

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

links = re.findall(r'href="\.\.\/(.*?)\/index\.html"', content)
missing = []
for link in links:
    full_path = os.path.join(root_dir, link, 'index.html')
    if not os.path.exists(full_path):
        missing.append(link)

print(f"Found {len(links)} links.")
if missing:
    print(f"Missing index.html in: {missing}")
else:
    print("All linked project index.html files exist.")

# Also check for empty images or placeholder sources
images = re.findall(r'src="(.*?)"', content)
placeholders = [img for img in images if 'unsplash.com' in img]
print(f"Found {len(images)} images, {len(placeholders)} are unsplash placeholders.")
