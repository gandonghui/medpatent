import json
import argparse
import sys

def verify_baselines(input_json, baselines):
    """
    检查去重后的结果中是否包含所有必选专利。
    """
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取所有出现的专利号和标准 ID
    found_numbers = set()
    for item in data:
        found_numbers.add(item['publication_number'].replace('_', '').upper())
        found_numbers.add(item['canonical_id'].upper())

    missing = []
    for baseline in baselines:
        clean_baseline = baseline.replace('_', '').replace('-', '').upper()
        # 检查是否以标准 ID 或原始号形式存在
        if not any(clean_baseline in f or f in clean_baseline for f in found_numbers):
            missing.append(baseline)
            
    return missing

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Baseline Verification Tool")
    parser.add_argument("--input", required=True, help="Input JSON file from deduplication")
    parser.add_argument("--baselines", required=True, help="Comma-separated list of required patent numbers")
    
    args = parser.parse_args()
    
    baseline_list = [b.strip() for b in args.baselines.split(',')]
    missing = verify_baselines(args.input, baseline_list)
    
    if missing:
        print(f"CRITICAL ERROR: Missing baseline patents: {', '.join(missing)}")
        sys.exit(1)
    else:
        print("SUCCESS: All baseline patents verified.")
        sys.exit(0)
