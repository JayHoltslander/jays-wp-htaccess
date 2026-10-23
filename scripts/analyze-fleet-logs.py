#!/usr/bin/env python3
"""
scripts/analyze-fleet-logs.py
======================================================================================================================
Automated Fleet Telemetry & Access Log Analyzer for Jay's WordPress .htaccess
======================================================================================================================
Processes raw web server access logs (Combined, Common, or Nginx format) across fleet WordPress sites.
Simulates Section 6.3 early-drop rules to identify scanner campaigns that fall through to index.php (404s),
causing unnecessary PHP/MySQL worker allocation. Generates GitHub-ready threat intelligence markdown tables.

Usage:
  python3 scripts/analyze-fleet-logs.py access.log
  python3 scripts/analyze-fleet-logs.py /var/log/httpd/*.log --min-breadth 3
  cat access.log | python3 scripts/analyze-fleet-logs.py --format markdown
======================================================================================================================
"""

import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict

# Import the rule extractor from mine-threat-intel
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
try:
    from mine_threat_intel import extract_section_6_rules, is_wp_false_positive
except ImportError:
    # Inline fallback if executed from different context
    import importlib.util
    spec = importlib.util.spec_from_file_location("mine_threat_intel", SCRIPT_DIR / "mine-threat-intel.py")
    mine_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mine_module)
    extract_section_6_rules = mine_module.extract_section_6_rules
    is_wp_false_positive = mine_module.is_wp_false_positive

LOG_REGEX = re.compile(
    r'^(?P<client>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+"(?P<method>[A-Z]+)\s+(?P<uri>\S+)[^"]*"\s+(?P<status>\d{3})\s+(?P<size>\S+)(?:\s+"(?P<referer>[^"]*)"\s+"(?P<ua>[^"]*)")?'
)

def classify_threat(path: str) -> str:
    """Classifies an unhandled probe into an appropriate Section 6 module."""
    lower = path.lower()
    if re.search(r'\.(jsp|asp|aspx|do|action|cgi|pl|dll|exe|zul)$', lower):
        return "Rule 1: Non-WP Executable"
    if re.search(r'(\.env|\.git|\.aws|\.kube|\.s3cfg|web\.config)', lower):
        return "Rule 2: Environment / Metadata"
    if re.search(r'(manifest|\.json|\.ya?ml|key|secret|token|credentials|exports|appsettings)', lower):
        return "Rule 3: Manifests & Credentials"
    if re.search(r'(\.sql|\.bak|\.dump|backup|tar|gz|tgz|zip|rar)$', lower):
        return "Rule 4: Dumps & Backups"
    if re.search(r'(shell|eval|phpinfo|cmd|adminer|upload|wso|c99|alfa|\.php)', lower):
        return "Rule 5: Web Shells & Diagnostics"
    if re.search(r'(mcp|sse)', lower):
        return "Rule 6c: AI Agent & MCP Protocol"
    if re.search(r'(swagger|openapi|actuator|console|api|vpn|portal|login|dana|confluence)', lower):
        return "Rule 6: Enterprise & Appliance Portal"
    if re.search(r'(user|author|member|customer|subscriber)', lower):
        return "Rule 10: User Enumeration"
    return "Section 6: Unclassified Probe"


def main():
    parser = argparse.ArgumentParser(description="Analyze fleet access logs for fall-through scanner probes")
    parser.add_argument("logs", nargs="*", help="Log file paths to analyze (reads stdin if omitted)")
    parser.add_argument("--min-hits", type=int, default=5, help="Minimum total hits to report (default: 5)")
    parser.add_argument("--min-breadth", type=int, default=1, help="Minimum unique client IPs to report (default: 1)")
    parser.add_argument("--format", choices=["table", "markdown"], default="table", help="Output format")
    parser.add_argument("--include-dropped", action="store_true", help="Include requests already dropped by .htaccess")
    args = parser.parse_args()

    root_dir = SCRIPT_DIR.parent
    htaccess_path = root_dir / ".htaccess"

    rules = extract_section_6_rules(htaccess_path)

    stats = defaultdict(lambda: {
        "hits": 0,
        "ips": set(),
        "methods": defaultdict(int),
        "statuses": defaultdict(int),
        "uas": defaultdict(int),
    })

    def process_line(line: str):
        m = LOG_REGEX.match(line.strip())
        if not m:
            return

        client = m.group("client")
        method = m.group("method")
        uri = m.group("uri")
        status = int(m.group("status"))
        ua = m.group("ua") or "Unknown"

        # Separate path and query
        path = uri.split("?")[0]
        query = uri.split("?")[1] if "?" in uri else ""

        stats[path]["hits"] += 1
        stats[path]["ips"].add(client)
        stats[path]["methods"][method] += 1
        stats[path]["statuses"][status] += 1
        stats[path]["uas"][ua] += 1

    if args.logs:
        total_files = len(args.logs)
        for log_path in args.logs:
            p = Path(log_path)
            if not p.exists():
                print(f"⚠️ Warning: Log file not found: {p}", file=sys.stderr)
                continue
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    process_line(line)
    else:
        # Read from stdin
        for line in sys.stdin:
            process_line(line)

    results = []
    for path, data in stats.items():
        clean_path = path.lstrip("/")
        if not clean_path or is_wp_false_positive(clean_path):
            continue

        breadth = len(data["ips"])
        hits = data["hits"]

        if hits < args.min_hits or breadth < args.min_breadth:
            continue

        # Test against .htaccess early-drop rules
        matched_rule = None
        for rule_id, raw_pattern, compiled in rules:
            if compiled.search(clean_path):
                matched_rule = rule_id
                break

        if matched_rule and not args.include_dropped:
            continue

        # Determine dominant method, status, UA
        dom_method = max(data["methods"].items(), key=lambda x: x[1])[0]
        status_summary = ", ".join(f"{s} ({c})" for s, c in sorted(data["statuses"].items(), key=lambda x: x[1], reverse=True))
        top_ua = max(data["uas"].items(), key=lambda x: x[1])[0]
        # Truncate UA for display
        if len(top_ua) > 35:
            top_ua = top_ua[:32] + "..."

        classification = matched_rule or classify_threat(clean_path)

        results.append({
            "path": "/" + clean_path,
            "breadth": breadth,
            "hits": hits,
            "method": dom_method,
            "status": status_summary,
            "ua": top_ua,
            "classification": classification,
            "dropped": bool(matched_rule),
        })

    # Sort results by breadth (descending), then hits (descending)
    results.sort(key=lambda x: (x["breadth"], x["hits"]), reverse=True)

    if args.format == "markdown":
        print("### Candidate Scanner Endpoints (Fleet Log Telemetry)\n")
        print("| Candidate Endpoint | Breadth | Total Hits | Method | Status | Sample User-Agent | Threat Profile / Classification |")
        print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for r in results:
            drop_tag = f" [DROPPED: {r['classification'].split(':')[0]}]" if r["dropped"] else ""
            print(f"| `{r['path']}` | **{r['breadth']} sites** | {r['hits']} | {r['method']} | {r['status']} | `{r['ua']}` | {r['classification']}{drop_tag} |")
    else:
        print("=" * 115)
        print("📊 FLEET ACCESS LOG TELEMETRY AUDIT")
        print("=" * 115)
        print(f"{'Endpoint':<35} {'Breadth':<10} {'Hits':<8} {'Method':<7} {'Status':<16} {'Threat Classification':<32}")
        print("-" * 115)
        for r in results:
            print(f"{r['path']:<35} {r['breadth']:<10} {r['hits']:<8} {r['method']:<7} {r['status']:<16} {r['classification'][:32]:<32}")
        print("-" * 115)
        print(f"Total Unique Endpoints Identified: {len(results)}\n")


if __name__ == "__main__":
    main()
