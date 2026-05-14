#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACHIKO10 — P1 Global Bug Fix Script
- P1-A: Remove duplicate tafti back bar from all CSS-based projects
- P1-B: Fix filter data-t mismatches (AutoImport, RealEstate, EdTech)
- P1-C: Remove javascript:alert() from all footer links
"""

import os
import re

ROOT = r"c:\Users\Utente\Desktop\achiko10"

CSS_PROJECTS = [
    "AutoImport_Premium",
    "B2B_Bioluminescent",
    "EdTech_DaVinci",
    "HoReCa_Anime",
    "Logistics_AR",
    "RealEstate_Crystal",
    "Detailing_Clay",
    "Export_Editorial",
    "Clay_Toy_Store",
]

fixed_files = []
errors = []

# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def fix_file(path):
    original = read(path)
    content = original
    changes = []

    # ── P1-A: Remove the duplicate sticky tafti back bar ──
    # Pattern: <div style="...sticky..."> ... tafti ... </div>
    # This block always starts with rgba(0,0,0,0.8) sticky and links to ../tafti/
    tafti_pattern = re.compile(
        r'<div\s+style="background:\s*rgba\(0,0,0,0\.8\)[^"]*position:\s*sticky[^"]*">'
        r'.*?</div>',
        re.DOTALL
    )
    new_content = tafti_pattern.sub('', content)
    if new_content != content:
        content = new_content
        changes.append("P1-A: ორმაგი back bar ამოშლა")

    # ── P1-C: Remove javascript:alert() from footer links ──
    # Pattern 1: href="javascript:alert(...)" onclick="alert(...)"
    # Replace entire <a ...>text</a> with just <span>text</span>
    
    # Remove onclick that fires alerts
    content_new = re.sub(
        r'\s+onclick="[^"]*alert\([^)]*\)[^"]*"',
        '',
        content
    )
    
    # Replace href="javascript:alert(...)..." with href="#"
    content_new = re.sub(
        r'href="javascript:alert\([^)]*\)[^"]*"',
        'href="#" style="pointer-events:none;opacity:0.5;cursor:default;"',
        content_new
    )
    
    if content_new != content:
        content = content_new
        changes.append("P1-C: javascript:alert() links გამოსწორდა")

    # ── P1-B: Fix filter data-t mismatches ──
    basename = os.path.basename(os.path.dirname(path))
    
    if basename == "AutoImport_Premium":
        # Fix filter buttons: use Georgian to match card data-t
        replacements = [
            ("onclick=\"flt('sedan',this)\"", "onclick=\"flt('სედანი',this)\""),
            ("onclick=\"flt('coupe',this)\"", "onclick=\"flt('კუპე',this)\""),
            ("onclick=\"flt('electric',this)\"", "onclick=\"flt('ელ.',this)\""),
            ("onclick=\"flt('suv',this)\"", "onclick=\"flt('suv',this)\""),  # SUV stays
        ]
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                changes.append(f"P1-B AutoImport: '{old}' → '{new}'")

    if basename == "RealEstate_Crystal":
        replacements = [
            ("onclick=\"flt('sale',this)\"", "onclick=\"flt('იყიდება',this)\""),
            ("onclick=\"flt('rent',this)\"", "onclick=\"flt('ქირავდება',this)\""),
        ]
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                changes.append(f"P1-B RealEstate: '{old}' → '{new}'")

    if basename == "EdTech_DaVinci":
        replacements = [
            ("onclick=\"flt('prog',this)\"", "onclick=\"flt('პროგრამირება',this)\""),
            ("onclick=\"flt('design',this)\"", "onclick=\"flt('დიზაინი',this)\""),
        ]
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                changes.append(f"P1-B EdTech: '{old}' → '{new}'")

    # ── P3: Fix Cyrillic letter in AutoImport navigation ──
    if basename == "AutoImport_Premium":
        # "კალკуলатори" has Cyrillic 'у' — fix to Georgian
        cyrillic_fix = content.replace("კალკ\u0443ლ\u0430тори", "კალკულატორი")
        cyrillic_fix = cyrillic_fix.replace("კალკ\u0443\u043b\u0430\u0442\u043e\u0440\u0438", "კალკულატორი")
        # Also catch any mixed encoding
        cyrillic_fix = re.sub(r'კალკ[уu]ла[тt]ор[иi]', 'კალკულატორი', cyrillic_fix)
        if cyrillic_fix != content:
            content = cyrillic_fix
            changes.append("P3: კირილური ასო გასწორდა (კალკулатори → კალკულატორი)")

    if content != original:
        write(path, content)
        fixed_files.append((path, changes))
        return True
    return False

# ─────────────────────────────────────────────────────────
# MAIN RUN
# ─────────────────────────────────────────────────────────

print("=" * 60)
print("ACHIKO10 — P1 GLOBAL BUG FIX")
print("=" * 60)

for project in CSS_PROJECTS:
    project_path = os.path.join(ROOT, project)
    if not os.path.isdir(project_path):
        print(f"  ⚠️  {project} — დირექტორია ვერ მოიძებნა")
        continue
    
    html_files = [
        os.path.join(project_path, f)
        for f in os.listdir(project_path)
        if f.endswith(".html")
    ]
    
    print(f"\n📁 {project} ({len(html_files)} HTML ფაილი):")
    for fpath in html_files:
        try:
            changed = fix_file(fpath)
            fname = os.path.basename(fpath)
            if changed:
                entry = next(e for e in fixed_files if e[0] == fpath)
                for ch in entry[1]:
                    print(f"  ✅ {fname} — {ch}")
            else:
                print(f"  ⚪ {fname} — ცვლილება საჭირო არ იყო")
        except Exception as e:
            errors.append((fpath, str(e)))
            print(f"  ❌ {os.path.basename(fpath)} — შეცდომა: {e}")

print("\n" + "=" * 60)
print(f"✅ გასწორებული ფაილები: {len(fixed_files)}")
print(f"❌ შეცდომები: {len(errors)}")
print("=" * 60)

if errors:
    print("\nSHECDOMEBI:")
    for path, err in errors:
        print(f"  {path}: {err}")
