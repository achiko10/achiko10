import os
import re
from collections import defaultdict

root_dir = 'c:/Users/Utente/Desktop/achiko10'

issues = defaultdict(list)

for subdir, dirs, files in os.walk(root_dir):
    if '.git' in subdir:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(subdir, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Check for empty or hash links
                hash_links = len(re.findall(r'href=[\"\'\']#[\"\'\']', content))
                if hash_links > 0:
                    issues['hash_links'].append(f"{os.path.relpath(filepath, root_dir)}: {hash_links} hash links")
                
                empty_links = len(re.findall(r'href=[\"\'\'][\"\'\']', content))
                if empty_links > 0:
                    issues['empty_links'].append(f"{os.path.relpath(filepath, root_dir)}: {empty_links} empty links")
                
                # Check for empty src
                empty_src = len(re.findall(r'src=[\"\'\'][\"\'\']', content))
                if empty_src > 0:
                    issues['empty_src'].append(f"{os.path.relpath(filepath, root_dir)}: {empty_src} empty src attributes")

                # Placeholder text
                lorem = len(re.findall(r'lorem ipsum', content, re.IGNORECASE))
                if lorem > 0:
                    issues['lorem_ipsum'].append(f"{os.path.relpath(filepath, root_dir)}: {lorem} placeholder texts")
                    
                # Missing title
                if '<title>' not in content.lower():
                    issues['missing_title'].append(os.path.relpath(filepath, root_dir))

for key, val in issues.items():
    print(f"\n--- {key.upper()} ---")
    for v in val[:10]:
        print(v)
    if len(val) > 10:
        print(f"... and {len(val) - 10} more")
