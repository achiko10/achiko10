
import os
import re

root_dir = os.getcwd()

platinum_badge = """
<div id="platinum-badge" style="position: fixed; top: 10px; right: 10px; z-index: 99999; background: linear-gradient(45deg, #00f2ff, #0066ff); color: white; padding: 5px 15px; border-radius: 20px; font-family: sans-serif; font-size: 10px; font-weight: bold; text-transform: uppercase; box-shadow: 0 0 20px rgba(0, 242, 255, 0.5); pointer-events: none; letter-spacing: 1px; border: 1px solid rgba(255,255,255,0.3);">
    💎 Platinum Edition
</div>
"""

def inject_badge(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'id="platinum-badge"' in content:
        return
    
    if '</body>' in content:
        new_content = content.replace('</body>', f'{platinum_badge}</body>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected badge into {filepath}")

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            inject_badge(os.path.join(subdir, file))
