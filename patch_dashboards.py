import os
import re

directories = [
    r'c:\Users\Utente\Desktop\achiko10\Architecture_Editorial',
    r'c:\Users\Utente\Desktop\achiko10\Fitness_Bento_Neon',
    r'c:\Users\Utente\Desktop\achiko10\Furniture_Clay',
    r'c:\Users\Utente\Desktop\achiko10\Vet_Clinic_Toy'
]

portfolio_bar_html = """
    <div class="portfolio-bar shrink-0" style="background: rgba(0,0,0,0.8); backdrop-filter: blur(15px); padding: 12px 0; text-align: center; position: sticky; top: 0; z-index: 10000; border-bottom: 1px solid rgba(255,255,255,0.1); width: 100%;">
        <a href="../tafti/index.html" style="display: inline-flex; align-items: center; gap: 10px; padding: 8px 24px; background: rgba(255, 255, 255, 0.05); border: 2px solid rgba(0, 242, 255, 0.3); border-radius: 50px; color: #fff; text-decoration: none; font-weight: 800; font-size: 10px; text-transform: uppercase; box-shadow: 0 10px 25px rgba(0,0,0,0.3); animation: holo-float 4s infinite ease-in-out;">✦ ACHIKO10 პორტფოლიოზე დაბრუნება</a>
    </div>
"""

def patch_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Patch body class to make it One-Screen
    body_match = re.search(r'<body[^>]*class="([^"]*)"[^>]*>', content)
    if body_match:
        old_classes = body_match.group(1)
        # Remove any existing overflow/h-screen
        classes_list = [c for c in old_classes.split() if c not in ('h-screen', 'w-screen', 'overflow-hidden', 'overflow-x-hidden', 'flex', 'flex-col')]
        classes_list.extend(['h-screen', 'w-screen', 'overflow-hidden', 'flex', 'flex-col'])
        new_classes = " ".join(classes_list)
        content = content[:body_match.start(1)] + new_classes + content[body_match.end(1):]
    else:
        # If body has no class
        content = re.sub(r'<body([^>]*)>', r'<body\1 class="h-screen w-screen overflow-hidden flex flex-col">', content)

    # 2. Make header shrink-0
    header_match = re.search(r'<header[^>]*class="([^"]*)"[^>]*>', content)
    if header_match:
        old_classes = header_match.group(1)
        if 'shrink-0' not in old_classes:
            new_classes = old_classes + ' shrink-0'
            content = content[:header_match.start(1)] + new_classes + content[header_match.end(1):]
    else:
        content = re.sub(r'<header([^>]*)>', r'<header\1 class="shrink-0">', content)

    # 3. Make footer shrink-0
    footer_match = re.search(r'<footer[^>]*class="([^"]*)"[^>]*>', content)
    if footer_match:
        old_classes = footer_match.group(1)
        if 'shrink-0' not in old_classes:
            new_classes = old_classes + ' shrink-0'
            content = content[:footer_match.start(1)] + new_classes + content[footer_match.end(1):]
    else:
        content = re.sub(r'<footer([^>]*)>', r'<footer\1 class="shrink-0">', content)

    # 4. Make main flex-1 overflow-y-auto
    main_match = re.search(r'<main[^>]*class="([^"]*)"[^>]*>', content)
    if main_match:
        old_classes = main_match.group(1)
        classes_list = [c for c in old_classes.split() if c not in ('flex-1', 'overflow-y-auto')]
        classes_list.extend(['flex-1', 'overflow-y-auto'])
        new_classes = " ".join(classes_list)
        content = content[:main_match.start(1)] + new_classes + content[main_match.end(1):]
    else:
        content = re.sub(r'<main([^>]*)>', r'<main\1 class="flex-1 overflow-y-auto">', content)

    # 5. Ensure the portfolio-bar is there right after body
    # Remove existing back-bar or portfolio-bar
    content = re.sub(r'<div class="(back-bar|portfolio-bar)".*?</div>', '', content, flags=re.DOTALL)
    
    # Inject the exact global portfolio bar
    body_tag_end = content.find('>', content.find('<body')) + 1
    content = content[:body_tag_end] + portfolio_bar_html + content[body_tag_end:]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched: {filepath}")

for d in directories:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.html'):
                patch_html_file(os.path.join(root, file))

print("All 4 projects patched successfully.")
