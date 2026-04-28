import os
import re
import argparse
import json

def canonicalize_patent_number(patent_str):
    """
    将专利号标准化，移除类型代码 (A1, B2 等) 和非数字字符。
    例如: US20220015832A1 -> US2022015832
          US9283050B2 -> US9283050
    """
    # 转换为大写并移除空格/下划线/短横线
    clean = re.sub(r'[\s\-_]', '', patent_str.upper())
    
    # 匹配模式: [国家代码][数字][类型代码]
    # 类型代码通常是 A1, B1, B2, S1 等 (字母+数字)
    match = re.match(r'^([A-Z]{2})(\d+)([A-Z]\d+)?$', clean)
    if match:
        country = match.group(1)
        number = match.group(2)
        # 对于公开号 (20220015832)，有时会包含年份。
        # 我们主要关心数字部分。
        return f"{country}{number}"
    
    # 如果不匹配标准模式，尝试简单移除结尾的字母+数字
    return re.sub(r'[A-Z]\d+$', '', clean)

def deduplicate_patents(input_dir):
    """
    扫描目录下的专利文件并按家族(标准号)去重。
    """
    files = os.listdir(input_dir)
    families = {}
    
    for filename in files:
        if not filename.endswith('.md') and not filename.endswith('.json'):
            continue
            
        # 从文件名提取专利号
        # 假设文件名格式如: us_9283050_b2.md
        name_part = os.path.splitext(filename)[0]
        canonical = canonicalize_patent_number(name_part)
        
        if canonical not in families:
            families[canonical] = []
        
        families[canonical].append({
            "original_filename": filename,
            "canonical_id": canonical,
            "publication_number": name_part.upper()
        })
    
    # 选择逻辑: 如果同一个家族有多个文件 (如 A1 和 B2)，优先保留 B2 (授权文本)
    unique_patents = []
    for canonical, versions in families.items():
        if len(versions) == 1:
            unique_patents.append(versions[0])
        else:
            # 简单排序：B2 > B1 > A1
            sorted_versions = sorted(versions, key=lambda x: x['publication_number'], reverse=True)
            unique_patents.append(sorted_versions[0])
            
    return unique_patents

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patent Family Deduplication Tool")
    parser.add_argument("--input", required=True, help="Input directory containing patent files")
    parser.add_argument("--output", help="Output JSON file path")
    
    args = parser.parse_args()
    
    results = deduplicate_patents(args.input)
    
    print(f"Original files: {len(os.listdir(args.input))}")
    print(f"Unique families: {len(results)}")
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=4))
