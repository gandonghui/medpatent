#!/usr/bin/env python3
"""
lens_search.py — Lens.org Patent Search API 检索脚本
medpatent harness 集成版

用法:
  python lens_search.py "surgical robot haptic feedback" --limit 20
  python lens_search.py "endoscope imaging" --cpc A61B1/00 --jurisdiction US,EP
  python lens_search.py --query-file my_query.json --limit 50
  python lens_search.py "robotic surgery" --date-from 2018-01-01 --date-to 2024-12-31 --output results.json

搜索结果自动保存至:
  .agents/harness/data/search_results/lens_YYYYMMDD_HHMMSS.json
  (遵循 search_playbook.md Rule 1: 查询可追溯性)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# ── 路径配置 ──────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
SKILL_ROOT  = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_ROOT.parents[2]          # medpatent/
RESULTS_DIR  = PROJECT_ROOT / ".agents" / "harness" / "data" / "search_results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

LENS_API_URL = "https://api.lens.org/patent/search"


# ── API 密钥读取 ───────────────────────────────────────────────────────────────
def get_api_key() -> str:
    """
    优先读取 .env 文件中的 LENS_API_KEY，
    其次尝试环境变量，都没有则提示用户。
    """
    # 1. 尝试 .env 文件
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("LENS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    return key

    # 2. 尝试环境变量
    key = os.environ.get("LENS_API_KEY", "")
    if key:
        return key

    # 3. 提示用户
    print("[ERROR] 未找到 LENS_API_KEY。")
    print("请在项目根目录的 .env 文件中添加：")
    print("  LENS_API_KEY=your_token_here")
    print("（申请地址: https://www.lens.org/lens/user/subscriptions）")
    sys.exit(1)


# ── 构建检索体 ─────────────────────────────────────────────────────────────────
def build_query(
    keyword: str | None,
    cpc: list[str] | None,
    jurisdiction: list[str] | None,
    date_from: str | None,
    date_to: str | None,
    assignee: str | None,
    query_file: str | None,
) -> dict:
    """
    构建 Lens.org Boolean Query DSL。
    支持关键词全文、CPC代码、管辖区、日期范围、申请人过滤。
    """
    # 直接使用外部 JSON 查询体
    if query_file:
        with open(query_file) as f:
            return json.load(f)

    must_clauses = []

    # 关键词 → query_string（支持 AND/OR/NOT 操作符）
    if keyword:
        must_clauses.append({
            "query_string": {
                "query": keyword,
                "fields": ["title", "abstract", "claims.text", "description.text"],
                "default_operator": "AND"
            }
        })

    # CPC 分类代码
    if cpc:
        cpc_clauses = [{"prefix": {"classifications.cpc.symbol": c}} for c in cpc]
        if len(cpc_clauses) == 1:
            must_clauses.append(cpc_clauses[0])
        else:
            must_clauses.append({"bool": {"should": cpc_clauses}})

    # 管辖区/国家
    if jurisdiction:
        must_clauses.append({
            "terms": {"jurisdiction": [j.upper() for j in jurisdiction]}
        })

    # 申请人
    if assignee:
        must_clauses.append({
            "match": {"applicants.name": assignee}
        })

    # 日期范围（申请日）
    if date_from or date_to:
        date_range: dict = {}
        if date_from:
            date_range["gte"] = date_from
        if date_to:
            date_range["lte"] = date_to
        must_clauses.append({"range": {"date_published": date_range}})

    if not must_clauses:
        raise ValueError("至少需要提供一个检索条件（关键词、CPC代码或申请人）。")

    query = (
        must_clauses[0]
        if len(must_clauses) == 1
        else {"bool": {"must": must_clauses}}
    )
    return {"query": query}


# ── 执行检索 ──────────────────────────────────────────────────────────────────
def search_patents(
    query_body: dict,
    limit: int = 20,
    offset: int = 0,
    sort_field: str = "date_published",
    sort_order: str = "desc",
) -> dict:
    """
    调用 Lens.org Patent Search API，返回原始 JSON 结果。
    """
    api_key = get_api_key()

    payload = {
        **query_body,
        "size": min(limit, 100),   # Lens.org 单次最多 100 条
        "from": offset,
        "sort": [{"relevance": "desc"}],
        "include": [
            "lens_id",
            "biblio",
            "abstract",
            "claims",
            "description",
            "families",
            "legal_status"
        ],
    }

    body = json.dumps(payload).encode("utf-8")
    req = Request(
        LENS_API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        print(f"[HTTP {e.code}] Lens.org API 错误: {body_text}")
        sys.exit(1)
    except URLError as e:
        print(f"[网络错误] 无法连接到 Lens.org: {e.reason}")
        sys.exit(1)


# ── 结果格式化 ────────────────────────────────────────────────────────────────
def format_results(data: dict, keyword: str = "") -> str:
    """
    按 search_playbook.md 的 Search Log Template 格式化输出。
    """
    total = data.get("total", 0)
    if isinstance(total, dict):
        total = total.get("value", 0)
    hits  = data.get("data", [])

    lines = [
        "=" * 60,
        "LENS.ORG PATENT SEARCH RESULTS",
        "=" * 60,
        f"查询: {keyword or '(自定义查询体)'}",
        f"总计匹配: {total}  |  本次返回: {len(hits)}",
        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    for i, pat in enumerate(hits, 1):
        biblio = pat.get("biblio", {})
        title_list = biblio.get("title", [])
        title_en = next((t.get("text", "") for t in title_list if t.get("lang") == "en"), "")
        if not title_en and title_list:
            title_en = title_list[0].get("text", "N/A")

        lens_id  = pat.get("lens_id", "N/A")
        pub_key  = biblio.get("publication_reference", {}).get("pub_key", "N/A")
        jur      = biblio.get("publication_reference", {}).get("jurisdiction", "")
        pub_date = biblio.get("publication_reference", {}).get("date", "N/A")
        pub_type = biblio.get("publication_reference", {}).get("type", "")

        applicants = biblio.get("parties", {}).get("applicants", [])
        names = []
        for a in applicants[:3]:
            ext_name = a.get("extracted_name", "")
            if isinstance(ext_name, dict):
                names.append(ext_name.get("value", ""))
            elif isinstance(ext_name, str):
                names.append(ext_name)
        assignee_names = ", ".join(filter(None, names)) or "N/A"

        cpc_list = biblio.get("classifications", {}).get("cpc", [])
        cpc_str  = " | ".join(c.get("symbol", "") for c in cpc_list[:5]) or "N/A"

        abstract_list = pat.get("abstract", [])
        abstract_en   = next(
            (a.get("text", "") for a in abstract_list if a.get("lang") == "en"), ""
        )
        if not abstract_en and abstract_list:
            abstract_en = abstract_list[0].get("text", "")
        abstract_short = (abstract_en[:280] + "…") if len(abstract_en) > 280 else abstract_en

        claims_sections = pat.get("claims", [])
        claim_count = 0
        if claims_sections:
            claim_count = len(claims_sections[0].get("claims", []))

        lines += [
            f"[{i}] {pub_key}  ({jur} · {pub_type})",
            f"    Lens ID : {lens_id}",
            f"    申请人  : {assignee_names}",
            f"    公开日  : {pub_date}",
            f"    CPC     : {cpc_str}",
            f"    权利要求: {claim_count} 项",
            f"    摘要    : {abstract_short}",
            "",
        ]

    lines += [
        "─" * 60,
        f"[下载全文] python scripts/lens_download.py <lens_id> [lens_id ...]",
        f"[分析摘要] python scripts/lens_analyze.py <results_json>",
        "=" * 60,
    ]
    return "\n".join(lines)


# ── 保存结果 ──────────────────────────────────────────────────────────────────
def save_results(data: dict, keyword: str, extra_meta: dict) -> Path:
    """
    将原始 JSON 结果保存到 harness data 目录，并附带检索元数据（可追溯性）。
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = RESULTS_DIR / f"lens_{ts}.json"

    total = data.get("total", 0)
    if isinstance(total, dict):
        total = total.get("value", 0)
    
    envelope = {
        "meta": {
            "source": "lens.org",
            "query": keyword,
            "timestamp": datetime.now().isoformat(),
            "total_hits": total,
            "returned": len(data.get("data", [])),
            **extra_meta,
        },
        "raw": data,
    }

    out_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


# ── CLI 入口 ──────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Lens.org 专利检索 — medpatent harness 集成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("keyword", nargs="?", help="关键词查询（支持 AND/OR/NOT）")
    parser.add_argument("--cpc",          nargs="+", help="CPC 代码，如 A61B34/30")
    parser.add_argument("--jurisdiction", nargs="+", help="管辖区代码，如 US EP CN")
    parser.add_argument("--assignee",     help="申请人/机构名称（模糊匹配）")
    parser.add_argument("--date-from",    help="公开日起始，如 2018-01-01")
    parser.add_argument("--date-to",      help="公开日截止，如 2024-12-31")
    parser.add_argument("--limit",        type=int, default=20, help="返回条数（默认20，最多100）")
    parser.add_argument("--offset",       type=int, default=0,  help="分页偏移")
    parser.add_argument("--query-file",   help="直接提供 Lens.org DSL JSON 文件路径")
    parser.add_argument("--output",       help="额外指定输出 JSON 路径（可选）")
    parser.add_argument("--ids-only",     action="store_true", help="只输出 lens_id 列表（用于批量下载）")

    args = parser.parse_args()

    # 构建查询
    query_body = build_query(
        keyword     = args.keyword,
        cpc         = args.cpc,
        jurisdiction= args.jurisdiction,
        date_from   = args.date_from,
        date_to     = args.date_to,
        assignee    = args.assignee,
        query_file  = args.query_file,
    )

    # 执行检索
    print(f"[Lens.org] 正在检索… 关键词: {args.keyword or '(DSL模式)'}")
    t0 = time.time()
    data = search_patents(query_body, limit=args.limit, offset=args.offset)
    elapsed = time.time() - t0
    total = data.get("total", 0)
    if isinstance(total, dict):
        total = total.get("value", 0)
    print(f"[Lens.org] 完成，耗时 {elapsed:.1f}s，命中 {total} 条")

    # 保存结果
    extra = {
        "cpc": args.cpc,
        "jurisdiction": args.jurisdiction,
        "assignee": args.assignee,
        "date_from": args.date_from,
        "date_to": args.date_to,
        "limit": args.limit,
    }
    saved_path = save_results(data, args.keyword or "", extra)
    print(f"[保存] {saved_path}")

    # 额外输出路径
    if args.output:
        Path(args.output).write_text(
            json.dumps({"meta": extra, "raw": data}, ensure_ascii=False, indent=2)
        )
        print(f"[额外保存] {args.output}")

    # 仅输出 lens_id 列表
    if args.ids_only:
        ids = [p.get("lens_id") for p in data.get("data", []) if p.get("lens_id")]
        print("\n".join(ids))
        return

    # 格式化打印
    print()
    print(format_results(data, args.keyword or ""))
    print(f"\n[提示] 结果文件: {saved_path}")


if __name__ == "__main__":
    main()
