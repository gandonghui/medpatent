#!/usr/bin/env python3
"""
lens_analyze.py — 专利元数据分析与摘要生成脚本
medpatent harness 集成版

从 Lens.org 检索结果 JSON 或已下载的 Markdown 文件生成结构化分析摘要：
  - 申请人分布 TOP N
  - CPC 分类热力分布
  - 年份趋势
  - 独立权利要求 / 从属权利要求统计
  - 输出适合 patent-claims-analyzer 使用的 CSV

用法:
  # 分析检索结果 JSON（lens_search.py 输出）
  python lens_analyze.py --from-results .agents/harness/data/search_results/lens_20260419.json

  # 分析已下载目录中的 Markdown 文件
  python lens_analyze.py --from-dir downloaded_patents/

  # 输出分析报告 Markdown + CSV（用于 patent-claims-analyzer）
  python lens_analyze.py --from-results lens_xxx.json --output-report analysis_report.md --output-csv claims.csv
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# ── 路径配置 ──────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT  = SCRIPT_DIR.parents[3]
RESULTS_DIR   = PROJECT_ROOT / ".agents" / "harness" / "data" / "search_results"
DOWNLOAD_DIR  = PROJECT_ROOT / "downloaded_patents"


# ── 从 JSON 结果中提取专利列表 ────────────────────────────────────────────────
def load_from_json(json_path: Path) -> list[dict]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    # 支持 lens_search.py 的 envelope 格式
    raw = data.get("raw", data)
    return raw.get("data", [])


# ── 从 Markdown 文件中提取关键字段 ───────────────────────────────────────────
def parse_markdown_patent(md_path: Path) -> dict | None:
    """
    解析 lens_download.py 生成的 Markdown 文件，提取结构化字段。
    """
    text = md_path.read_text(encoding="utf-8", errors="replace")

    def extract(pattern, default="N/A"):
        m = re.search(pattern, text)
        return m.group(1).strip() if m else default

    lens_id  = extract(r"\*\*Lens ID\*\*\s*\|\s*`([^`]+)`")
    pub_key  = extract(r"\*\*公开号\*\*\s*\|\s*`([^`]+)`")
    jur      = extract(r"\*\*管辖区\*\*\s*\|\s*(\S+)")
    pub_date = extract(r"\*\*公开日\*\*\s*\|\s*(\S+)")
    cpc_str  = extract(r"\*\*CPC\*\*\s*:\s*`([^`]+)`")

    # 标题 = 第一行 # 标题
    title_m = re.match(r"^#\s+(.+)", text)
    title   = title_m.group(1).strip() if title_m else md_path.stem

    # 申请人
    applicant_m = re.search(r"## 👥 申请人.*?\n(.*?)(?=##|\Z)", text, re.DOTALL)
    applicants  = []
    if applicant_m:
        for line in applicant_m.group(1).splitlines():
            m2 = re.match(r"^-\s+(.+)\s+\(", line)
            if m2:
                applicants.append(m2.group(1).strip())

    # 权利要求数量
    claims_m = re.findall(r"\*\*(Claim|权利要求)\s+(\d+)\*\*", text)
    claim_count = len(claims_m)
    indep_count = len(re.findall(r"\*independent\*|\*独立\*|\[independent\]|\[独立权利要求\]", text, re.I))

    return {
        "lens_id": lens_id,
        "pub_key": pub_key,
        "jurisdiction": jur,
        "date_published": pub_date,
        "title": title,
        "applicants": applicants,
        "cpc_codes": [c.strip() for c in cpc_str.split("|") if c.strip() and c.strip() != "N/A"],
        "claim_count": claim_count,
        "independent_claim_count": indep_count,
        "source_file": str(md_path),
    }


# ── 从 JSON 结果中提取统计字段 ────────────────────────────────────────────────
def extract_stats_from_json_patent(pat: dict) -> dict:
    biblio = pat.get("biblio", {})
    lens_id  = pat.get("lens_id", "N/A")
    
    pub_ref = biblio.get("publication_reference", {})
    pub_key  = pub_ref.get("pub_key", "N/A")
    jur      = pub_ref.get("jurisdiction", "N/A")
    pub_date = pub_ref.get("date", "")

    title_list = biblio.get("title", [])
    title_en   = next((t.get("text","") for t in title_list if t.get("lang")=="en"), "")
    if not title_en and title_list:
        title_en = title_list[0].get("text","N/A")

    applicants = [a.get("extracted_name", {}).get("value", "") if isinstance(a.get("extracted_name"), dict) else a.get("extracted_name", "") 
                  for a in biblio.get("parties", {}).get("applicants", [])]
    applicants = [name for name in applicants if name]
    
    # CPC / IPC 统计 (Lens API 现代格式: classifications_cpc / classifications_ipcr)
    cpc_raw = biblio.get("classifications_cpc", [])
    if isinstance(cpc_raw, dict): cpc_raw = cpc_raw.get("classifications", [])
    cpcs = [c.get("symbol","") for c in (cpc_raw if isinstance(cpc_raw, list) else []) if isinstance(c, dict) and c.get("symbol")]

    ipc_raw = biblio.get("classifications_ipcr", [])
    if isinstance(ipc_raw, dict): ipc_raw = ipc_raw.get("classifications", [])
    ipcs = [i.get("symbol","") for i in (ipc_raw if isinstance(ipc_raw, list) else []) if isinstance(i, dict) and i.get("symbol")]

    # 权利要求统计
    all_claims = []
    for section in pat.get("claims", []):
        if isinstance(section, dict):
            all_claims.extend(section.get("claims", []) or [])
    claim_count = len(all_claims)
    indep_count = sum(
        1 for c in all_claims
        if isinstance(c, dict) and (
            c.get("claim_type","").lower() in ("independent", "独立")
            or not c.get("claim_refs", [])
        )
    )

    year = pub_date[:4] if pub_date and len(pub_date) >= 4 else "N/A"

    return {
        "lens_id": lens_id,
        "pub_key": pub_key,
        "jurisdiction": jur,
        "year": year,
        "date_published": pub_date,
        "title": title_en,
        "applicants": applicants,
        "cpc_codes": cpcs[:5],
        "claim_count": claim_count,
        "independent_claim_count": indep_count,
        "source": "json",
    }


# ── 统计聚合 ──────────────────────────────────────────────────────────────────
def aggregate(records: list[dict]) -> dict:
    applicant_counter = Counter()
    cpc_counter       = Counter()
    year_counter      = Counter()
    jur_counter       = Counter()
    total_claims      = 0
    total_indep       = 0

    for r in records:
        for a in r.get("applicants", []):
            if a:
                applicant_counter[a] += 1
        for c in r.get("cpc_codes", []):
            if c:
                # 只取到4位主分组
                main = c[:4] if len(c) >= 4 else c
                cpc_counter[main] += 1
        yr = r.get("year") or (r.get("date_published","")[:4] if r.get("date_published") else "N/A")
        if yr and yr != "N/A":
            year_counter[yr] += 1
        jur = r.get("jurisdiction","N/A")
        if jur:
            jur_counter[jur] += 1
        total_claims += r.get("claim_count", 0)
        total_indep  += r.get("independent_claim_count", 0)

    return {
        "top_applicants": applicant_counter.most_common(15),
        "top_cpc": cpc_counter.most_common(15),
        "year_trend": sorted(year_counter.items()),
        "jurisdiction_dist": jur_counter.most_common(),
        "total_patents": len(records),
        "total_claims": total_claims,
        "total_independent_claims": total_indep,
        "avg_claims": total_claims / len(records) if records else 0,
    }


# ── 生成分析报告 Markdown ─────────────────────────────────────────────────────
def render_report(records: list[dict], stats: dict, query_info: str = "") -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    n  = stats["total_patents"]

    def bar(count, max_count, width=20):
        ratio = count / max_count if max_count else 0
        filled = int(ratio * width)
        return "█" * filled + "░" * (width - filled)

    # 申请人分布
    top_a  = stats["top_applicants"]
    max_a  = top_a[0][1] if top_a else 1
    app_rows = "\n".join(
        f"| {name[:40]:<40} | {cnt:>5} | {bar(cnt, max_a)} |"
        for name, cnt in top_a
    )

    # CPC 分布
    top_c  = stats["top_cpc"]
    max_c  = top_c[0][1] if top_c else 1
    cpc_rows = "\n".join(
        f"| `{code}`  | {cnt:>5} | {bar(cnt, max_c)} |"
        for code, cnt in top_c
    )

    # 年份趋势
    year_rows = "\n".join(
        f"| {yr} | {cnt:>5} | {bar(cnt, max(c for _,c in stats['year_trend']) if stats['year_trend'] else 1)} |"
        for yr, cnt in stats["year_trend"]
    )

    # 管辖区分布
    jur_rows = "\n".join(
        f"| {jur} | {cnt} |"
        for jur, cnt in stats["jurisdiction_dist"]
    )

    # 专利明细表
    detail_rows = "\n".join(
        f"| `{r.get('pub_key','N/A')}` | {r.get('date_published','N/A')[:4]} | "
        f"{(r.get('applicants',[]) or ['N/A'])[0][:35]} | "
        f"{' '.join(r.get('cpc_codes',[])[:2])} | "
        f"{r.get('claim_count',0)} | {r.get('independent_claim_count',0)} |"
        for r in records
    )

    return f"""# Lens.org 专利检索分析报告

**生成时间**: {ts}
**检索/分析对象**: {query_info or "（见来源文件）"}
**专利总数**: {n}

---

## 📊 统计摘要

| 指标 | 数值 |
|------|------|
| 专利总数 | {n} |
| 权利要求总计 | {stats['total_claims']} |
| 独立权利要求 | {stats['total_independent_claims']} |
| 平均权利要求数 | {stats['avg_claims']:.1f} |

---

## 🏢 申请人分布 TOP 15

| 申请人 | 数量 | 占比图 |
|--------|------|--------|
{app_rows}

---

## 🏷️ CPC 主分组分布 TOP 15

| CPC 代码 | 数量 | 占比图 |
|----------|------|--------|
{cpc_rows}

---

## 📅 年份申请趋势

| 年份 | 数量 | 趋势 |
|------|------|------|
{year_rows}

---

## 🌍 管辖区分布

| 管辖区 | 数量 |
|--------|------|
{jur_rows}

---

## 📋 专利明细（前50条）

| 公开号 | 年份 | 主要申请人 | CPC | 权利要求数 | 独立项数 |
|--------|------|----------|-----|-----------|---------|
{detail_rows}

---

## 🔗 下一步操作

```bash
# 批量下载全文
python scripts/lens_download.py --from-results <results_json> --top 20

# 权利要求深度分析（接入 patent-claims-analyzer）
# 将生成的 CSV 拖入 patent-claims-analyzer skill
```

*报告由 lens_analyze.py 生成 | medpatent harness*
"""


# ── 输出 CSV（兼容 patent-claims-analyzer） ───────────────────────────────────
def write_csv(records: list[dict], csv_path: Path):
    """
    输出 CSV 格式，字段与 patent-claims-analyzer skill 兼容。
    """
    fieldnames = [
        "lens_id", "pub_key", "jurisdiction", "date_published",
        "title", "applicants", "cpc_codes",
        "claim_count", "independent_claim_count",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            row = dict(r)
            row["applicants"] = "; ".join(r.get("applicants", []))
            row["cpc_codes"]  = " | ".join(r.get("cpc_codes", []))
            writer.writerow({k: row.get(k, "") for k in fieldnames})
    print(f"[CSV] 写出 {len(records)} 行 → {csv_path}")


# ── CLI 入口 ──────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Lens.org 专利分析摘要生成 — medpatent harness 集成",
    )
    parser.add_argument("--from-results", metavar="JSON",
                        help="lens_search.py 输出的 JSON 结果文件")
    parser.add_argument("--from-dir", metavar="DIR",
                        help="lens_download.py 下载的 Markdown 目录")
    parser.add_argument("--output-report", metavar="MD",
                        help="分析报告输出路径（.md）")
    parser.add_argument("--output-csv", metavar="CSV",
                        help="CSV 输出路径（兼容 patent-claims-analyzer）")
    parser.add_argument("--top", type=int, default=0,
                        help="只分析前 N 条（0=全部）")

    args = parser.parse_args()

    records   = []
    query_info = ""

    # 从 JSON 加载
    if args.from_results:
        json_path  = Path(args.from_results)
        if not json_path.exists():
            # 自动在 results 目录查找
            candidates = sorted(RESULTS_DIR.glob("lens_*.json"), reverse=True)
            matched    = [p for p in candidates if args.from_results in p.name]
            json_path  = matched[0] if matched else json_path

        patents = load_from_json(json_path)
        if args.top > 0:
            patents = patents[:args.top]
        records = [extract_stats_from_json_patent(p) for p in patents]
        # 读取 query 信息
        raw = json.loads(json_path.read_text(encoding="utf-8"))
        query_info = raw.get("meta", {}).get("query", json_path.name)
        print(f"[分析] 从 JSON 加载 {len(records)} 条专利（{json_path.name}）")

    # 从下载目录加载
    elif args.from_dir:
        md_dir = Path(args.from_dir)
        md_files = sorted(md_dir.rglob("*.md"))
        if args.top > 0:
            md_files = md_files[:args.top]
        for md_path in md_files:
            parsed = parse_markdown_patent(md_path)
            if parsed:
                records.append(parsed)
        query_info = f"目录: {md_dir}"
        print(f"[分析] 从目录加载 {len(records)} 个 Markdown 文件")

    else:
        print("[错误] 请指定 --from-results 或 --from-dir")
        parser.print_help()
        sys.exit(1)

    if not records:
        print("[警告] 没有找到可分析的专利记录")
        sys.exit(0)

    # 聚合统计
    stats = aggregate(records)

    # 生成报告
    report_md = render_report(records, stats, query_info)

    # 输出报告
    if args.output_report:
        out = Path(args.output_report)
        out.write_text(report_md, encoding="utf-8")
        print(f"[报告] → {out}")
    else:
        print(report_md)

    # 输出 CSV
    if args.output_csv:
        write_csv(records, Path(args.output_csv))

    # 打印简要统计
    print(f"\n[摘要] {stats['total_patents']} 个专利 | "
          f"平均 {stats['avg_claims']:.1f} 项权利要求 | "
          f"TOP申请人: {stats['top_applicants'][0][0] if stats['top_applicants'] else 'N/A'}")


if __name__ == "__main__":
    main()
