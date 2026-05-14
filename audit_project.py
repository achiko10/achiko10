import os
import re

root_dir = 'c:/Users/Utente/Desktop/achiko10'
stats = {
    'total_html_files': 0,
    'missing_title': [],
    'missing_meta_desc': [],
    'empty_images': [],
    'placeholder_texts': []
}

for subdir, dirs, files in os.walk(root_dir):
    if '.git' in subdir or 'node_modules' in subdir:
        continue
    for file in files:
        if file.endswith('.html'):
            stats['total_html_files'] += 1
            filepath = os.path.join(subdir, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    if '<title>' not in content.lower() or not re.search(r'<title>.*?</title>', content, re.IGNORECASE | re.DOTALL):
                        stats['missing_title'].append(os.path.relpath(filepath, root_dir))
                    
                    if '<meta name="description"' not in content.lower():
                        stats['missing_meta_desc'].append(os.path.relpath(filepath, root_dir))
                        
                    if re.search(r'src=["\']["\']', content):
                        stats['empty_images'].append(os.path.relpath(filepath, root_dir))
                        
                    if re.search(r'lorem ipsum', content, re.IGNORECASE):
                        stats['placeholder_texts'].append(os.path.relpath(filepath, root_dir))
                        
            except Exception as e:
                pass

print(f"Total HTML files: {stats['total_html_files']}")
print(f"Files missing title: {len(stats['missing_title'])}")
print(f"Files missing meta description: {len(stats['missing_meta_desc'])}")
print(f"Files with empty image src: {len(stats['empty_images'])}")
print(f"Files with placeholder text: {len(stats['placeholder_texts'])}")

if stats['missing_title']:
    print("\n--- Missing Title Example ---")
    print(stats['missing_title'][0])
