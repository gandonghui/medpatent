#!/usr/bin/env python3
"""
lens_download.py — Lens.org 专利全文下载脚本
medpatent harness 集成版

将专利全文保存为 Markdown 文件，遵循项目命名规范：
  downloaded_patents/{jurisdiction}/{JUR}_{number}_{kind}.md

用法:
  # 下载单个专利（用 lens_id）
  python lens_download.py 031-720-013-543-533

  # 下载多个
  python lens_download.py 031-720-013-543-533 086-163-927-682-451

  # 从检索结果 JSON 批量下载（取前 N 条）
  python lens_download.py --from-results lens_20260419_103000.json --top 10

  # 指定输出目录（默认: downloaded_patents/）
  python lens_download.py <id> --output-dir doc/downloaded_patents

输出文件自动按管辖区分子目录，命名如:
  US_10123456_B2.md
  EP_2470089_A1.md
  CN_102596062_B.md
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# ── 路径配置 ──────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
SKILL_ROOT   = SCRIPT_DIR.parent
PROJECT_ROOT  = SKILL_ROOT.parents[2]
DOWNLOAD_DIR  = PROJECT_ROOT / "downloaded_patents"
RESULTS_DIR   = PROJECT_ROOT / ".agents" / "harness" / "data" / "search_results"

LENS_API_URL  = "https://api.lens.org/patent/search"


# ── API 密钥读取（与 lens_search.py 保持一致） ────────────────────────────────
def get_api_key() -> str:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("LENS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    return key
    key = os.environ.get("LENS_API_KEY", "")
    if key:
        return key
    print("[ERROR] 未找到 LENS_API_KEY，请在 .env 文件中配置。")
    sys.exit(1)


# ── 通过 lens_id 批量拉取专利详情 ─────────────────────────────────────────────
def fetch_by_lens_ids(lens_ids: list[str]) -> list[dict]:
    """
    用 lens_id 批量查询 Lens.org，每次最多 50 个。
    """
    api_key = get_api_key()
    all_patents = []

    # 分批：Lens.org terms 查询最多 100 个值
    batch_size = 50
    for i in range(0, len(lens_ids), batch_size):
        batch = lens_ids[i:i + batch_size]
        payload = {
            "query": {"terms": {"lens_id": batch}},
            "size": len(batch),
            "include": [
                "lens_id", "biblio", "abstract", "claims", "description", "families", "legal_status"
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        req  = Request(
            LENS_API_URL,
            data=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                all_patents.extend(result.get("data", []))
        except HTTPError as e:
            print(f"[HTTP {e.code}] 批次 {i//batch_size+1} 失败: {e.read().decode()[:200]}")
        time.sleep(0.5)   # 礼貌性延迟

    return all_patents


# ── 标准化文件名 ──────────────────────────────────────────────────────────────
def normalize_filename(patent: dict) -> tuple[str, str]:
    """
    将专利元数据转换为项目标准命名：JUR_number_kind.md
    返回 (subdirectory_name, filename)

    规则（与 unify_patent_names.py 保持一致）:
      - jurisdiction: US / EP / CN / WO / JP
      - pub_key: "US_10123456_B2" → US_10123456_B2
    """
    biblio = patent.get("biblio", {})
    pub_ref = biblio.get("publication_reference", {})
    
    jur  = (pub_ref.get("jurisdiction") or patent.get("jurisdiction") or "XX").upper()
    num  = pub_ref.get("doc_number") or ""
    kind = pub_ref.get("kind") or ""
    
    if num:
        basename = f"{jur}_{num}"
        if kind:
            basename += f"_{kind}"
        filename = f"{basename.lower()}.md"
    else:
        lens_id_safe = patent.get("lens_id", "unknown").replace("-", "_")
        filename = f"{jur.lower()}_{lens_id_safe}.md"

    return jur, filename


# ── 渲染 Markdown ─────────────────────────────────────────────────────────────
def render_markdown(patent: dict) -> str:
    """
    将专利 JSON 渲染为 medpatent 项目标准 Markdown 格式，
    与 downloaded_patents/ 目录中现有文件风格一致。
    """
    lens_id  = patent.get("lens_id", "N/A")
    biblio   = patent.get("biblio", {})
    pub_ref  = biblio.get("publication_reference", {})
    pub_key = pub_ref.get("pub_key") or f"{pub_ref.get('jurisdiction','')}{pub_ref.get('doc_number','')}{pub_ref.get('kind','')}"
    jur      = pub_ref.get("jurisdiction", "N/A")
    pub_date = pub_ref.get("date", "N/A")
    pub_type = pub_ref.get("type", "N/A")

    # 标题（优先英文）
    title_list = biblio.get("title", [])
    if isinstance(title_list, dict): title_list = [title_list]
    title_en   = next((t.get("text","") for t in title_list if t.get("lang")=="en"), "")
    if not title_en and title_list:
        title_en = title_list[0].get("text", "No Title")
    title_zh   = next((t.get("text","") for t in title_list if t.get("lang")=="zh"), "")

    # 摘要
    abstract_list = patent.get("abstract", []) or []
    if isinstance(abstract_list, dict): abstract_list = [abstract_list]
    abstract_en   = next((a.get("text","") for a in abstract_list if a.get("lang")=="en"), "")
    if not abstract_en and abstract_list:
        abstract_en = abstract_list[0].get("text","")
    abstract_zh   = next((a.get("text","") for a in abstract_list if a.get("lang")=="zh"), "")

    # 申请人
    parties = biblio.get("parties", {})
    applicants = parties.get("applicants", []) or []
    if isinstance(applicants, dict): applicants = [applicants]
    names = []
    for a in applicants:
        ext_name = a.get("extracted_name", "")
        if isinstance(ext_name, dict):
            names.append(f"{ext_name.get('value', 'N/A')} ({a.get('residence','?')})")
        else:
            names.append(f"{ext_name or 'N/A'} ({a.get('residence','?')})")
    applicant_str = "\n".join(f"- {name}" for name in names) or "N/A"

    # 发明人
    inventors = parties.get("inventors", []) or []
    if isinstance(inventors, dict): inventors = [inventors]
    inventor_str = ", ".join(i.get("extracted_name", {}).get("value", "") 
                            if isinstance(i.get("extracted_name"), dict) 
                            else i.get("extracted_name", "") 
                            for i in inventors) or "N/A"

    # CPC / IPC
    classifications = biblio.get("classifications", {})
    cpcs = classifications.get("cpc", []) or []
    if isinstance(cpcs, dict): cpcs = [cpcs]
    cpc_str = " | ".join(c.get("symbol","") for c in cpcs[:10]) or "N/A"
    ipcs = classifications.get("ipc", []) or []
    if isinstance(ipcs, dict): ipcs = [ipcs]
    ipc_str = " | ".join(i.get("symbol","") for i in ipcs[:5]) or "N/A"

    # 权利要求
    claims_sections = patent.get("claims", []) or []
    if isinstance(claims_sections, dict): claims_sections = [claims_sections]
    claims_md_parts = []
    for section in claims_sections:
        lang = section.get("lang", "")
        section_claims = section.get("claims", []) or []
        if isinstance(section_claims, dict): section_claims = [section_claims]
        for claim in section_claims:
            num   = claim.get("claim_sequence", "?")
            text  = claim.get("claim_text", "")
            if isinstance(text, list):
                text = " ".join(str(t) for t in text)
            text = text.strip() if text else ""
            
            type_ = claim.get("claim_type", "")
            label = f"**权利要求 {num}**" if lang == "zh" else f"**Claim {num}**"
            if type_:
                label += f" *[{type_}]*"
            claims_md_parts.append(f"{label}\n\n{text}")

    claims_md = "\n\n---\n\n".join(claims_md_parts) if claims_md_parts else "*（全文权利要求未收录）*"

    # 说明书
    desc_sections = patent.get("description", []) or []
    if isinstance(desc_sections, dict): desc_sections = [desc_sections]
    desc_en = next((d.get("text","") for d in desc_sections if d.get("lang")=="en"), "")
    if not desc_en and desc_sections:
        desc_en = desc_sections[0].get("text","")
    desc_md = desc_en.strip() if desc_en else "*（说明书全文未收录）*"

    # 法律状态
    legal = patent.get("legal_status", {})
    legal_str = legal.get("patent_status", "N/A") if isinstance(legal, dict) else "N/A"

    # 专利族id
    family_id = "N/A"
    families = patent.get("families", []) or []
    if isinstance(families, dict): families = [families]
    if families and isinstance(families, list):
        family_id = families[0].get("family_id", "N/A")
    elif isinstance(families, dict): # redundant but safe
        family_id = families.get("family_id", "N/A")

    # 下载时间戳
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 预计算含换行符的条件字段（f-string 内 {} 不允许 \n）
    title_zh_line    = ("**（中文标题）** " + title_zh) if title_zh else ""
    abstract_zh_block = ("**（中文摘要）**\n\n" + abstract_zh) if abstract_zh else ""

    md = f"""# {title_en}
{title_zh_line}

---

## 📋 基本信息

| 字段 | 值 |
|------|----|
| **Lens ID** | `{lens_id}` |
| **公开号** | `{pub_key}` |
| **管辖区** | {jur} |
| **公开类型** | {pub_type} |
| **公开日** | {pub_date} |
| **法律状态** | {legal_str} |
| **专利族 ID** | {family_id} |
| **下载时间** | {ts} |

---

## 👥 申请人 / 权利人

{applicant_str}

**发明人**: {inventor_str}

---

## 🏷️ 分类代码

- **CPC**: `{cpc_str}`
- **IPC**: `{ipc_str}`

---

## 📝 摘要

{abstract_en}

{abstract_zh_block}

---

## ⚖️ 权利要求

{claims_md}

---

## 📖 说明书（Description）

{desc_md}

---
*来源: Lens.org — {lens_id}*
*下载于: {ts}*
"""
    return md.strip()


# ── 主下载流程 ────────────────────────────────────────────────────────────────
def download_patents(
    lens_ids: list[str],
    output_dir: Path,
    skip_existing: bool = True,
) -> list[dict]:
    """
    批量下载专利全文并保存到 output_dir。
    返回下载摘要列表（每条含 lens_id、文件路径、状态）。
    """
    print(f"[下载] 共 {len(lens_ids)} 个专利，获取元数据中…")
    patents = fetch_by_lens_ids(lens_ids)
    print(f"[下载] API 返回 {len(patents)} 条记录")

    summary = []
    for pat in patents:
        lens_id = pat.get("lens_id", "unknown")
        jur, filename = normalize_filename(pat)

        # 按管辖区分子目录（与现有 downloaded_patents/ 结构一致）
        sub_dir = output_dir / jur
        sub_dir.mkdir(parents=True, exist_ok=True)
        out_path = sub_dir / filename

        if skip_existing and out_path.exists():
            print(f"  [跳过] {filename}（已存在）")
            summary.append({"lens_id": lens_id, "path": str(out_path), "status": "skipped"})
            continue

        md_content = render_markdown(pat)
        out_path.write_text(md_content, encoding="utf-8")
        print(f"  [OK] {filename}  ->  {out_path.relative_to(PROJECT_ROOT)}")
        summary.append({"lens_id": lens_id, "path": str(out_path), "status": "downloaded"})

    return summary


# ── CLI 入口 ──────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Lens.org 专利全文下载 — medpatent harness 集成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "lens_ids", nargs="*",
        help="Lens ID 列表，如 031-720-013-543-533"
    )
    parser.add_argument(
        "--from-results", metavar="JSON",
        help="从 lens_search.py 生成的结果 JSON 中读取 lens_id"
    )
    parser.add_argument(
        "--top", type=int, default=0,
        help="配合 --from-results，只取前 N 条（0=全部）"
    )
    parser.add_argument(
        "--output-dir", default=str(DOWNLOAD_DIR),
        help=f"输出目录（默认: {DOWNLOAD_DIR}）"
    )
    parser.add_argument(
        "--no-skip", action="store_true",
        help="强制重新下载（即使文件已存在）"
    )

    args = parser.parse_args()

    # 收集 lens_id
    ids_to_download = list(args.lens_ids)

    if args.from_results:
        json_path = Path(args.from_results)
        if not json_path.exists():
            # 尝试从 results 目录找
            candidates = sorted(RESULTS_DIR.glob("lens_*.json"), reverse=True)
            matched = [p for p in candidates if args.from_results in p.name]
            json_path = matched[0] if matched else json_path

        data = json.loads(json_path.read_text(encoding="utf-8"))
        # 支持两种格式：envelope（含 meta）或 raw API 返回
        patents_raw = data.get("raw", data).get("data", [])
        if args.top > 0:
            patents_raw = patents_raw[:args.top]
        extracted = [p.get("lens_id") for p in patents_raw if p.get("lens_id")]
        ids_to_download.extend(extracted)
        print(f"[从JSON] 读取到 {len(extracted)} 个 Lens ID（文件: {json_path.name}）")

    if not ids_to_download:
        print("[错误] 未提供任何 Lens ID。请直接传入 ID 或使用 --from-results。")
        parser.print_help()
        sys.exit(1)

    # 去重
    ids_to_download = list(dict.fromkeys(ids_to_download))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = download_patents(
        ids_to_download,
        output_dir=output_dir,
        skip_existing=not args.no_skip,
    )

    # 打印摘要
    downloaded = [s for s in summary if s["status"] == "downloaded"]
    skipped    = [s for s in summary if s["status"] == "skipped"]
    print(f"\n[完成] 下载 {len(downloaded)} 个 | 跳过 {len(skipped)} 个")
    print(f"[目录] {output_dir}")
    if downloaded:
        print("\n[下一步] 运行分析脚本:")
        print(f"  python scripts/lens_analyze.py --from-dir {output_dir}")


if __name__ == "__main__":
    main()
