import json
import argparse

def generate_ir(input_json, output_json):
    """
    生成中间表示层 (IR)。
    目前只是简单的结构化转换，为后续特征提取打基础。
    """
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    ir_data = {
        "version": "2.0",
        "total_families": len(data),
        "patents": []
    }
    
    for item in data:
        ir_data["patents"].append({
            "id": item["canonical_id"],
            "latest_pub": item["publication_number"],
            "source_file": item["original_filename"],
            "audit_status": "pending",
            "features": {}
        })
        
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(ir_data, f, indent=4, ensure_ascii=False)
    
    print(f"IR generated: {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IR Generation Tool")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--output", required=True, help="Output IR JSON file")
    
    args = parser.parse_args()
    generate_ir(args.input, args.output)
