#!/usr/bin/env python3
"""
scripts/mine-threat-intel.py
======================================================================================================================
Automated Threat Intelligence & Wordlist Audit Utility for Jay's WordPress .htaccess
======================================================================================================================
Mines and audits candidate scan paths from SecLists, Nuclei templates, or custom wordlists against Section 6.3 of
.htaccess. Identifies unhandled exploit paths, checks for WordPress false-positive risks, and suggests optimized
Apache regex groupings.

Usage:
  python3 scripts/mine-threat-intel.py --file wordlist.txt
  python3 scripts/mine-threat-intel.py --fetch-seclists
  python3 scripts/mine-threat-intel.py --url https://raw.githubusercontent.com/...
======================================================================================================================
"""

import sys
import os
import re
import argparse
import urllib.request
from pathlib import Path
from collections import defaultdict

DEFAULT_SECLISTS_URLS = [
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/quickhits.txt",
    "https://raw.githubusercontent.com/Bo0oM/fuzz.txt/master/fuzz.txt",
]

# Standard WordPress core slugs, routes, and common legitimate e-commerce / blog terms
WP_SAFE_TOKENS = {
    "wp-admin", "wp-login.php", "admin-ajax.php", "wp-cron.php", "xmlrpc.php",
    "wp-content", "wp-includes", "wp-json", "index.php", "readme.html",
    "license.txt", "robots.txt", "sitemap.xml", "sitemap_index.xml",
    "favicon.ico", "apple-touch-icon.png", ".well-known",
    "feed", "comments", "author", "category", "tag", "search", "page",
    "cart", "checkout", "my-account", "shop", "product", "products",
    "sample-page", "privacy-policy", "terms-of-service", "contact",
    "about", "services", "pricing", "blog", "news", "portfolio",
}

def extract_section_6_rules(htaccess_path: Path):
    """Parses Section 6.3 RewriteRule patterns from .htaccess."""
    if not htaccess_path.exists():
        print(f"❌ Error: .htaccess not found at {htaccess_path}", file=sys.stderr)
        sys.exit(1)

    rules = []
    in_section_63 = False
    current_rule_id = "Rule 6.3"

    with open(htaccess_path, "r", encoding="utf-8") as f:
        pending_conds = []
        for line in f:
            stripped = line.strip()

            if "6.3 ADVANCED EARLY-DROP PROTECTION" in stripped:
                in_section_63 = True
                continue
            if in_section_63 and "6.4 BLOCK ACCESS TO HIDDEN" in stripped:
                break

            if not in_section_63 or not stripped:
                continue

            # Capture rule comment headers like "# 3. Block Developer Manifests..."
            m_header = re.match(r"^#\s*([0-9]+[a-z]?)\.\s*(.*)", stripped)
            if m_header:
                current_rule_id = f"Rule {m_header.group(1)}: {m_header.group(2)[:40]}"
                pending_conds = []
                continue

            # Skip comments
            if stripped.startswith("#"):
                continue

            if stripped.startswith("RewriteCond"):
                parts = stripped.split()
                if len(parts) >= 3:
                    test_str = parts[1]
                    cond_pat = parts[2].strip('"')
                    flags = parts[3].strip("[]") if len(parts) >= 4 else ""
                    pending_conds.append((test_str, cond_pat, flags))
                continue

            # Extract pattern: RewriteRule <Pattern> <Substitution> [Flags]
            if stripped.startswith("RewriteRule"):
                parts = stripped.split()
                if len(parts) >= 4:
                    raw_pattern = parts[1]
                    if raw_pattern.startswith('"') and raw_pattern.endswith('"'):
                        raw_pattern = raw_pattern[1:-1]

                    flags = parts[3].strip("[]")
                    is_case_insensitive = "NC" in flags

                    # If the pattern is purely '.*' or '.?', it depends on RewriteCond
                    if raw_pattern in (".*", ".?"):
                        # Extract URI/REQUEST conditions if applicable (e.g. Rule 10 REST endpoints)
                        uri_conds = [c for c in pending_conds if "%{REQUEST_URI}" in c[0] and not c[1].startswith("!")]
                        for test_str, cond_pat, cflags in uri_conds:
                            clean_pat = cond_pat.lstrip("^").lstrip("/").lstrip("(^|/)")
                            clean_pat = cond_pat
                            re_flags = re.IGNORECASE if ("NC" in cflags or is_case_insensitive) else 0
                            try:
                                compiled = re.compile(clean_pat, re_flags)
                                rules.append((current_rule_id, clean_pat, compiled))
                            except re.error:
                                pass
                        pending_conds = []
                        continue

                    pending_conds = []

                    # Convert inline (?i) to re.IGNORECASE
                    re_pattern = raw_pattern
                    if "(?i)" in re_pattern:
                        re_pattern = re_pattern.replace("(?i)", "")
                        is_case_insensitive = True

                    try:
                        re_flags = re.IGNORECASE if is_case_insensitive else 0
                        compiled = re.compile(re_pattern, re_flags)
                        rules.append((current_rule_id, raw_pattern, compiled))
                    except re.error as e:
                        print(f"⚠️ Warning: Could not compile regex '{raw_pattern}': {e}", file=sys.stderr)

    return rules


def is_wp_false_positive(candidate: str) -> bool:
    """Checks if a candidate path poses a false-positive risk for standard WordPress routes."""
    normalized = candidate.lower().strip("/")
    parts = normalized.split("/")

    # Check root tokens
    if parts[0] in WP_SAFE_TOKENS:
        return True

    return False


def test_candidate(candidate: str, rules):
    """Tests a candidate path against compiled .htaccess rules."""
    path = candidate.lstrip("/")
    for rule_id, raw_pattern, compiled in rules:
        if compiled.search(path):
            return rule_id
    return None


def main():
    parser = argparse.ArgumentParser(description="Mine threat intelligence wordlists against Section 6.3 rules in .htaccess")
    parser.add_argument("--file", "-f", type=Path, help="Path to local wordlist file")
    parser.add_argument("--url", "-u", type=str, help="Custom URL to download wordlist from")
    parser.add_argument("--fetch-seclists", action="store_true", help="Download and test curated SecLists & FuzzDB quickhits")
    parser.add_argument("--max-candidates", type=int, default=1000, help="Maximum candidates to evaluate (default: 1000)")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent
    htaccess_path = root_dir / ".htaccess"

    print("🔍 Parsing active Section 6.3 rules from .htaccess...")
    rules = extract_section_6_rules(htaccess_path)
    print(f"✅ Loaded {len(rules)} compiled early-drop RewriteRules.\n")

    candidates = set()

    if args.file:
        if not args.file.exists():
            print(f"❌ Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        print(f"📖 Reading candidates from {args.file}...")
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                item = line.strip()
                if item and not item.startswith("#"):
                    candidates.add(item)

    elif args.fetch_seclists or args.url:
        urls = [args.url] if args.url else DEFAULT_SECLISTS_URLS
        for u in urls:
            print(f"🌐 Fetching wordlist from {u}...")
            try:
                req = urllib.request.Request(u, headers={"User-Agent": "WP-Htaccess-Threat-Miner/1.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    text = resp.read().decode("utf-8", errors="ignore")
                    for line in text.splitlines():
                        item = line.strip()
                        if item and not item.startswith("#"):
                            candidates.add(item)
            except Exception as e:
                print(f"⚠️ Failed to fetch {u}: {e}", file=sys.stderr)
    else:
        print("💡 No input specified. Running with sample high-frequency probe dictionary...")
        sample_probes = [
            "/mcp", "/sse", "/appsettings.json", "/aws-exports.js", "/turbo.json",
            "/.env", "/wp-config.php.bak", "/server-status", "/phpinfo.php",
            "/h2-console", "/jolokia", "/actuator/health", "/heapdump",
            "/.next/routes-manifest.json", "/install/index.php", "/www.zip",
            "/local.settings.json", "/.vault-token", "/swagger.json",
            "/wp-json/wc/v3/customers", "/wp-json/ldlms/v2/users",
            "/about", "/contact-us", "/wp-login.php", "/cart",
            "/api/unknown/scanner-endpoint", "/rogue-backdoor.php",
        ]
        candidates.update(sample_probes)

    total_loaded = len(candidates)
    eval_list = list(candidates)[:args.max_candidates]
    print(f"\n📊 Evaluating {len(eval_list)} candidate paths (out of {total_loaded} total loaded)...\n")

    dropped_count = 0
    safe_count = 0
    unhandled = []

    rule_drop_stats = defaultdict(int)

    for item in eval_list:
        clean_path = item.strip().lstrip("/")
        if not clean_path:
            continue

        matched_rule = test_candidate(clean_path, rules)
        if matched_rule:
            dropped_count += 1
            rule_drop_stats[matched_rule] += 1
        elif is_wp_false_positive(clean_path):
            safe_count += 1
        else:
            unhandled.append(clean_path)

    print("=" * 90)
    print("🎯 AUDIT SUMMARY RESULTS")
    print("=" * 90)
    print(f"Total Evaluated:       {len(eval_list)}")
    print(f"✅ Dropped by Rules:   {dropped_count} ({(dropped_count/len(eval_list))*100:.1f}%)")
    print(f"🛡️ Legitimate WP Safe: {safe_count}")
    print(f"⚡ Unhandled Probes:   {len(unhandled)}")
    print("-" * 90)

    print("\n📈 Drop Distribution by Rule:")
    for rule_id, count in sorted(rule_drop_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {rule_id:<50}: {count} hits")

    if unhandled:
        print(f"\n⚠️ Top Unhandled Probe Candidates (First {min(len(unhandled), 25)}):")
        for u in sorted(unhandled)[:25]:
            print(f"  - /{u}")

    print("\n🎉 Threat intelligence audit completed cleanly.")


if __name__ == "__main__":
    main()
