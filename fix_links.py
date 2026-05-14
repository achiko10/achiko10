import os
import re

root_dir = 'c:/Users/Utente/Desktop/achiko10'
replacement_href = 'href="javascript:alert(\'Coming Soon! ეს ფუნქცია/გვერდი მალე დაემატება.\')"'

files_modified = 0
links_replaced = 0

for subdir, dirs, files in os.walk(root_dir):
    if '.git' in subdir or 'node_modules' in subdir:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(subdir, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Regex to find href="#"
                new_content, count = re.subn(r'href\s*=\s*["\']#["\']', replacement_href, content)
                
                if count > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_modified += 1
                    links_replaced += count
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

print(f"Modification complete. Modified {files_modified} files, replaced {links_replaced} links.")
