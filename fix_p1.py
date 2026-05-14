import os
import re

ROOT = r"c:\Users\Utente\Desktop\achiko10"
CSS_PROJECTS = [
    "AutoImport_Premium", "B2B_Bioluminescent", "EdTech_DaVinci",
    "HoReCa_Anime", "Logistics_AR", "RealEstate_Crystal",
    "Detailing_Clay", "Export_Editorial", "Clay_Toy_Store"
]

fixed_files = 0

def read_utf8(path):
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read(), enc
        except Exception:
            continue
    return None, None

def write_utf8(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def fix_file(path, project_name):
    content, enc = read_utf8(path)
    if content is None:
        print("  ERR: cannot read " + path)
        return 0
    
    original = content
    changes = []

    # ── P1-A: Remove tafti sticky back bar ──────────────────
    # The second bar starts with: <div style="background: rgba(0,0,0,0.8);
    # and contains: ../tafti/index.html
    # We find it as: <div style="...sticky..."> ... </div>
    # Strategy: find the <div> block that has tafti in it
    
    # Find all occurrences of the second sticky div
    idx = 0
    while True:
        start = content.find('<div style="background: rgba(0,0,0,0.8)', idx)
        if start == -1:
            break
        # Find the matching </div>
        # Count nested divs
        search_from = start + 10
        depth = 1
        pos = start + 10
        while pos < len(content) and depth > 0:
            next_open = content.find('<div', pos)
            next_close = content.find('</div>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                if depth == 0:
                    end = next_close + 6  # len('</div>')
                    block = content[start:end]
                    if 'tafti' in block or 'back-btn-holo' in block:
                        content = content[:start] + content[end:]
                        changes.append("P1-A: tafti bar removed")
                        idx = start
                    else:
                        idx = end
                    break
                pos = next_close + 6
        else:
            break

    # ── P1-C: Remove javascript:alert onclick handlers ──────
    before = content
    content = re.sub(r'\s+onclick="[^"]*alert\([^)]*\)[^"]*"', '', content)
    if content != before:
        changes.append("P1-C: onclick alerts removed")

    # ── P1-C: Replace javascript:alert() hrefs ──────────────
    before = content
    content = re.sub(
        r'href="javascript:alert\([^)]*\)"',
        'href="#" style="pointer-events:none;opacity:0.55;cursor:not-allowed;"',
        content
    )
    if content != before:
        changes.append("P1-C: href alerts fixed")

    # ── P1-B: Fix filter mismatches ─────────────────────────
    if project_name == "AutoImport_Premium":
        reps = [
            ("flt('sedan',this)", "flt('\u10e1\u10d4\u10d3\u10d0\u10dc\u10d8',this)"),
            ("flt('coupe',this)", "flt('\u10d9\u10e3\u10de\u10d4',this)"),
            ("flt('electric',this)", "flt('\u10d4\u10da.',this)"),
        ]
        for old, new in reps:
            if old in content:
                content = content.replace(old, new)
                changes.append("P1-B: filter " + old + " fixed")

    if project_name == "RealEstate_Crystal":
        reps = [
            ("flt('sale',this)", "flt('\u10d8\u10e7\u10d8\u10d3\u10d4\u10d1\u10d0',this)"),
            ("flt('rent',this)", "flt('\u10e5\u10d8\u10e0\u10d0\u10d5\u10d3\u10d4\u10d1\u10d0',this)"),
        ]
        for old, new in reps:
            if old in content:
                content = content.replace(old, new)
                changes.append("P1-B: filter " + old + " fixed")

    if project_name == "EdTech_DaVinci":
        reps = [
            ("flt('prog',this)", "flt('\u10de\u10e0\u10dd\u10d2\u10e0\u10d0\u10db\u10d8\u10e0\u10d4\u10d1\u10d0',this)"),
            ("flt('design',this)", "flt('\u10d3\u10d8\u10d6\u10d0\u10d8\u10dc\u10d8',this)"),
        ]
        for old, new in reps:
            if old in content:
                content = content.replace(old, new)
                changes.append("P1-B: filter " + old + " fixed")

    if content != original:
        write_utf8(path, content)
        return changes
    return []

total = 0
for project in CSS_PROJECTS:
    pp = os.path.join(ROOT, project)
    if not os.path.isdir(pp):
        print("SKIP: " + project + " not found")
        continue
    
    files = sorted([f for f in os.listdir(pp) if f.endswith(".html")])
    print("\n[" + project + "]")
    for fname in files:
        fpath = os.path.join(pp, fname)
        ch = fix_file(fpath, project)
        if ch:
            total += 1
            for c in ch:
                print("  OK " + fname + " -- " + c)
        else:
            print("  -- " + fname + " (no change needed)")

print("\n\nSUMMARY: " + str(total) + " files fixed")
