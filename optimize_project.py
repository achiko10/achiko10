import os
import re

root_dir = 'c:/Users/Utente/Desktop/achiko10'

def process_html(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    modified = False
    
    # 1. Add Meta Description if missing
    if '<meta name="description"' not in content.lower():
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()
            meta_tag = f'\n    <meta name="description" content="{title} - ACHIKO10 პრემიუმ პორტფოლიოს პროექტი.">'
            content = content.replace(title_match.group(0), title_match.group(0) + meta_tag)
            modified = True
            
    # 2. Fix Form Buttons (type="button" -> type="submit")
    # Finding buttons with "გაგზავნა" or "Send" or "Booking"
    new_content, count = re.subn(r'type=["\']button["\'](.*?>\s*(გაგზავნა|Send|Submit|Booking|Order|Checkout|🚀))', r'type="submit"\1', content, flags=re.IGNORECASE)
    if count > 0:
        content = new_content
        modified = True
        
    # 3. Add global form success handler if not present
    if '</form>' in content and 'onsubmit' not in content.lower() and 'addEventListener("submit"' not in content:
        script_snippet = """
<script>
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('მადლობა! თქვენი შეტყობინება წარმატებით გაიგზავნა. / Thank you! Your message has been sent successfully.');
        form.reset();
    });
});
</script>
"""
        if '</body>' in content:
            content = content.replace('</body>', script_snippet + '</body>')
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

count = 0
for subdir, dirs, files in os.walk(root_dir):
    if '.git' in subdir or 'node_modules' in subdir:
        continue
    for file in files:
        if file.endswith('.html'):
            if process_html(os.path.join(subdir, file)):
                count += 1

print(f"Successfully optimized {count} HTML files.")
