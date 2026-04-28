import json
import os
import argparse
from pathlib import Path
from collections import defaultdict

def extract_lens_id(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    import re
    m = re.search(r'\*\*Lens ID\*\*\s*\|\s*`([^`]+)`', content)
    return m.group(1).strip() if m else None

def deduplicate_v2(input_dir, output_file, metadata_json):
    # Load metadata to get mapping: Lens ID -> (Jurisdiction + Application Number)
    with open(metadata_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    patents_meta = data.get('raw', {}).get('data', [])
    lens_to_family = {}
    for pat in patents_meta:
        lens_id = pat.get('lens_id')
        biblio = pat.get('biblio', {})
        jur = biblio.get('publication_reference', {}).get('jurisdiction', 'N/A')
        app_ref = biblio.get('application_reference', {})
        app_no = app_ref.get('doc_number')
        if not app_no:
            app_no = lens_id # Fallback
        
        # Family ID is Jurisdiction + Application Number
        family_id = f"{jur}_{app_no}"
        lens_to_family[lens_id] = family_id

    # Scan files and group
    groups = defaultdict(list)
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                lens_id = extract_lens_id(full_path)
                if not lens_id:
                    continue
                
                family_id = lens_to_family.get(lens_id, f"UNKNOWN_{lens_id}")
                groups[family_id].append({
                    "original_filename": file,
                    "full_path": os.path.relpath(full_path, os.getcwd()),
                    "lens_id": lens_id,
                    "family_id": family_id
                })

    # For each group, pick a "canonical" version (prefer B2 over A1, etc.)
    final_list = []
    for family_id, members in groups.items():
        # Prefer granted (B) over published (A)
        # Sort by filename descending (usually B comes after A in lex order, but we can be smarter)
        members.sort(key=lambda x: x['original_filename'], reverse=True)
        # Select the first one as canonical
        canonical = members[0]
        final_list.append(canonical)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=4)
    
    print(f"Original files: {sum(len(v) for v in groups.values())}")
    print(f"Unique families (App-based): {len(final_list)}")

if __name__ == "__main__":
    # Hardcoded for now to fix the issue immediately
    metadata = ".agents/harness/data/search_results/lens_20260428_160654.json"
    deduplicate_v2('downloaded_patents', 'intuitive_unique_families.json', metadata)
