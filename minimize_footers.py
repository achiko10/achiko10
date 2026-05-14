import os
import re

directories = [
    r'c:\Users\Utente\Desktop\achiko10\Architecture_Editorial',
    r'c:\Users\Utente\Desktop\achiko10\Fitness_Bento_Neon',
    r'c:\Users\Utente\Desktop\achiko10\Furniture_Clay',
    r'c:\Users\Utente\Desktop\achiko10\Vet_Clinic_Toy'
]

def patch_footer(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Project Name from title
    title_match = re.search(r'<title>(.*?)</title>', content)
    project_name = title_match.group(1).split('|')[0].strip() if title_match else "PROJECT"

    minimal_footer = f"""
    <footer class="h-12 shrink-0 bg-[#0a0a0a] text-stone-400 border-t border-white/10 flex justify-between items-center px-6 z-50 text-[9px] font-bold uppercase tracking-[0.2em]">
        <div>&copy; 2026 {project_name}</div>
        <div>PLATINUM EDITION BY <span class="text-white">ACHIKO10</span></div>
    </footer>
"""

    # Replace the existing footer block entirely
    content = re.sub(r'<footer[^>]*>.*?</footer>', minimal_footer, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched footer: {filepath}")

for d in directories:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.html'):
                patch_footer(os.path.join(root, file))

print("Footers minimized.")
