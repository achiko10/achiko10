import os
import re

root_dir = r'c:\Users\Utente\Desktop\achiko10'

premium_header_html = """
    <!-- ACHIKO10 GLOBAL PREMIUM BACK BAR -->
    <div class="portfolio-bar-global shrink-0" style="background: linear-gradient(180deg, #050505 0%, rgba(5,5,5,0.9) 100%); backdrop-filter: blur(20px); padding: 16px 24px; display: flex; justify-content: center; align-items: center; position: relative; z-index: 99999; border-bottom: 1px solid rgba(0, 242, 255, 0.15); box-shadow: 0 10px 40px rgba(0,0,0,0.8);">
        <a href="../index.html" style="display: inline-flex; align-items: center; gap: 12px; padding: 12px 32px; background: rgba(0, 242, 255, 0.05); border: 1px solid rgba(0, 242, 255, 0.4); border-radius: 50px; color: #fff; text-decoration: none; font-weight: 900; font-size: 13px; text-transform: uppercase; letter-spacing: 0.15em; transition: all 0.3s ease; box-shadow: 0 0 25px rgba(0, 242, 255, 0.15);">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00f2ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
            ACHIKO10 პორტფოლიო
        </a>
    </div>
"""

# Projects to patch (subdirectories)
for root, dirs, files in os.walk(root_dir):
    # skip root directory HTMLs (the hub itself) and tafti (mirror hub) and assets
    if root == root_dir or 'tafti' in root or 'assets' in root or '.gemini' in root:
        continue
        
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove existing old portfolio bars
            content = re.sub(r'<div class="portfolio-bar[^>]*>.*?</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'<div class="back-bar[^>]*>.*?</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'<!-- GLOBAL PORTFOLIO BAR.*?-->', '', content, flags=re.DOTALL)
            content = re.sub(r'<!-- ACHIKO10 GLOBAL PREMIUM BACK BAR -->\s*<div class="portfolio-bar-global[^>]*>.*?</div>\s*', '', content, flags=re.DOTALL)
            
            # Find body tag and inject the new premium header right after it
            body_match = re.search(r'<body[^>]*>', content)
            if body_match:
                body_end = body_match.end()
                content = content[:body_end] + "\n" + premium_header_html + content[body_end:]
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Patched: {filepath}")
