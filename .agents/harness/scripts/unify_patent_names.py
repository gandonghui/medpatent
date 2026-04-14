import os
import re
from pathlib import Path

def normalize_name(country, number, kind):
    # Standard format: us_8281670_b2
    country = country.strip().lower() if country else "us"
    number = re.sub(r'[^a-zA-Z0-9]', '', str(number)).lower()
    kind = kind.strip().lower() if kind else ""
    
    # Remove redundant country prefix if number already starts with it
    if number.startswith(country):
        number = number[len(country):]
        
    parts = [country, number]
    if kind:
        parts.append(kind)
        
    return "_".join(parts) + ".md"

def process_file(file_path, review_dir):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to find Patent Number / Publication Number
        # Matching styles like:
        # **Patent Number:** US 08281670 B2
        # - **Patent Number**: N/A
        # # Patent: US-12114939-B2
        
        num_match = re.search(r'(?:Patent|Publication)\s+Number[:*]*\s*([A-Z0-9\s-]+)', content, re.IGNORECASE)
        header_match = re.search(r'# Patent:\s*([A-Z0-9\s-]+)', content, re.IGNORECASE)
        
        raw_num = None
        if num_match:
            raw_num = num_match.group(1).strip()
        elif header_match:
            raw_num = header_match.group(1).strip()

        if not raw_num or raw_num.upper() in ["N/A", "UNKNOWN", "N / A"]:
            print(f"REVIEW REQUIRED: {file_path.name}")
            os.rename(file_path, review_dir / file_path.name)
            return

        # Simple split for US-12114939-B2 or US 08281670 B2
        # Or just use raw if it's already structured
        parts = re.split(r'[-\s]+', raw_num)
        
        if len(parts) >= 3:
            country, num, kind = parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            country, num, kind = parts[0], parts[1], ""
        else:
            # Fallback for "08281670"
            country, num, kind = "us", parts[0], ""

        new_name = normalize_name(country, num, kind)
        new_path = file_path.parent / new_name

        if file_path.name == new_name:
            # print(f"ALREADY OK: {file_name}")
            return

        if new_path.exists():
            print(f"CONFLICT: {new_name} already exists. Appending suffix.")
            new_name = new_name.replace(".md", "_dup.md")
            new_path = file_path.parent / new_name

        print(f"RENAME: {file_path.name} -> {new_name}")
        os.rename(file_path, new_path)

    except Exception as e:
        print(f"ERROR processing {file_path.name}: {e}")

def main():
    target_dir = Path(r"c:\Users\gan\medpatent\downloaded_patents")
    review_dir = target_dir / "review_required"
    review_dir.mkdir(exist_ok=True)

    files = [f for f in target_dir.glob("*.md")]
    print(f"Found {len(files)} files to check.")
    
    for f in files:
        process_file(f, review_dir)

if __name__ == "__main__":
    main()
