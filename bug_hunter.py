import os
import re

root_dir = 'c:/Users/Utente/Desktop/achiko10'
html_files = []
for subdir, dirs, files in os.walk(root_dir):
    if '.git' in subdir: continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.relpath(os.path.join(subdir, file), root_dir).replace('\\', '/'))

bugs = {
    'broken_internal_links': [],
    'duplicate_ids': [],
    'broken_local_images': []
}

for subdir, dirs, files in os.walk(root_dir):
    if '.git' in subdir: continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(subdir, file)
            rel_subdir = os.path.relpath(subdir, root_dir).replace('\\', '/')
            if rel_subdir == '.': rel_subdir = ''
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # 1. Broken Internal Links
                    links = re.findall(r'href=["\'](?!http|https|javascript|#)(.*?)["\']', content)
                    for link in links:
                        link_clean = link.split('#')[0].split('?')[0]
                        if not link_clean: continue
                        
                        # Resolve path
                        target_path = os.path.normpath(os.path.join(subdir, link_clean)).replace('\\', '/')
                        target_rel = os.path.relpath(target_path, root_dir).replace('\\', '/')
                        
                        if target_rel not in html_files and not os.path.exists(target_path):
                            bugs['broken_internal_links'].append(f"{os.path.relpath(filepath, root_dir)} -> {link}")

                    # 2. Duplicate IDs
                    ids = re.findall(r'id=["\'](.*?)["\']', content)
                    seen_ids = set()
                    for id_val in ids:
                        if id_val in seen_ids:
                            bugs['duplicate_ids'].append(f"{os.path.relpath(filepath, root_dir)}: Duplicate ID '{id_val}'")
                        seen_ids.add(id_val)

                    # 3. Broken Local Images (src points to local file that doesn't exist)
                    images = re.findall(r'src=["\'](?!http|https|data:)(.*?)["\']', content)
                    for img in images:
                        img_path = os.path.normpath(os.path.join(subdir, img))
                        if not os.path.exists(img_path):
                             bugs['broken_local_images'].append(f"{os.path.relpath(filepath, root_dir)}: Missing image {img}")

            except Exception:
                pass

for key, val in bugs.items():
    print(f"\n--- {key.upper()} ---")
    for v in val[:15]:
        print(v)
    if len(val) > 15:
        print(f"... and {len(val) - 15} more")
