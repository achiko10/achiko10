import os
import re

badge_pattern = re.compile(r'<div id="platinum-badge".*?</div>', re.DOTALL)
root_dir = r'c:\Users\Utente\Desktop\achiko10'

count = 0
for root, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '<div id="platinum-badge"' in content:
                new_content = badge_pattern.sub('', content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1

print(f"Removed badge from {count} files.")
