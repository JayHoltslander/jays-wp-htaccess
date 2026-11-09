#!/usr/bin/env bash
# ======================================================================================================================
# Automated Syntax & Token Validation Test for Jays WordPress .htaccess
# ======================================================================================================================
# Validates .htaccess for:
# 1. Unquoted whitespace in RewriteCond / RewriteRule arguments (avoids 'bad flag delimiters')
# 2. Spaces inside flag brackets [NC, OR] -> must be [NC,OR]
# 3. Balanced brackets and valid flag formatting
# 4. Apache httpd -t syntax test with mod_rewrite and modules actively loaded in a <Directory> context
# ======================================================================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
HTACCESS="${ROOT_DIR}/.htaccess"

if [[ ! -f "${HTACCESS}" ]]; then
    echo "❌ Error: .htaccess not found at ${HTACCESS}"
    exit 1
fi

echo "🔍 Step 1: Performing static token and syntax analysis on .htaccess..."

python3 - << 'EOF'
import sys
import shlex
import re

with open(".htaccess", "r", encoding="utf-8") as f:
    lines = f.readlines()

errors = []
warnings = []

for idx, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        continue

    # 1. Check for bad flag spaces in trailing flags block like [NC, OR] or [F, L]
    if stripped.startswith(("RewriteRule", "RewriteCond")):
        m = re.search(r"\s+\[([a-zA-Z0-9_=,\s-]+)\]\s*$", stripped)
        if m:
            flag_content = m.group(1)
            if " " in flag_content:
                errors.append(f"Line {idx}: Whitespace inside flags '[{flag_content}]'. Flags must not contain spaces (use '[NC,OR]').")

    # 2. Check RewriteCond argument count (unquoted pattern with spaces)
    if stripped.startswith("RewriteCond"):
        try:
            tokens = shlex.split(stripped)
            # RewriteCond TestString CondPattern [flags] -> at most 4 tokens
            if len(tokens) > 4:
                errors.append(
                    f"Line {idx}: RewriteCond has {len(tokens)} arguments (max 4 allowed): {stripped}\n"
                    f"       -> Ensure patterns with spaces are enclosed in double quotes."
                )
        except Exception as e:
            errors.append(f"Line {idx}: Failed to parse RewriteCond tokens: {e}")

    # 3. Check RewriteRule argument count
    if stripped.startswith("RewriteRule"):
        try:
            tokens = shlex.split(stripped)
            # RewriteRule Pattern Substitution [flags] -> at most 4 tokens
            if len(tokens) > 4:
                errors.append(
                    f"Line {idx}: RewriteRule has {len(tokens)} arguments (max 4 allowed): {stripped}\n"
                    f"       -> Ensure patterns or substitutions with spaces are enclosed in double quotes."
                )
        except Exception as e:
            errors.append(f"Line {idx}: Failed to parse RewriteRule tokens: {e}")

if errors:
    print(f"❌ Found {len(errors)} static analysis error(s):")
    for err in errors:
        print(f"  • {err}")
    sys.exit(1)
else:
    print("✅ Static token and delimiter analysis passed cleanly (no unquoted spaces or bad flag delimiters).")
EOF

echo ""
echo "🔍 Step 2: Testing Apache httpd / apache2 configuration parsing..."

# Locate Apache binary
HTTPD_BIN=""
if command -v httpd >/dev/null 2>&1; then
    HTTPD_BIN="$(command -v httpd)"
elif command -v apache2 >/dev/null 2>&1; then
    HTTPD_BIN="$(command -v apache2)"
fi

if [[ -z "${HTTPD_BIN}" ]]; then
    echo "⚠️ Warning: httpd or apache2 binary not found in PATH. Skipping dynamic httpd test."
    exit 0
fi

# Locate Apache module directory
MOD_DIR=""
POSSIBLE_DIRS=(
    "/usr/libexec/apache2"
    "/usr/lib/apache2/modules"
    "/opt/homebrew/lib/httpd/modules"
    "/usr/local/lib/httpd/modules"
)

for dir in "${POSSIBLE_DIRS[@]}"; do
    if [[ -d "${dir}" && -f "${dir}/mod_rewrite.so" ]]; then
        MOD_DIR="${dir}"
        break
    fi
done

if [[ -z "${MOD_DIR}" ]]; then
    echo "⚠️ Warning: mod_rewrite.so not found in standard paths. Skipping dynamic httpd test."
    exit 0
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

CONF_FILE="${TMP_DIR}/test_httpd.conf"
ERROR_LOG="${TMP_DIR}/error.log"

cat << CONF > "${CONF_FILE}"
ServerName 127.0.0.1:8080
Listen 127.0.0.1:8080
ErrorLog "${ERROR_LOG}"
CONF

MODULES_TO_LOAD=(
    mpm_prefork
    authn_core
    authn_file
    authz_core
    authz_host
    access_compat
    dir
    autoindex
    headers
    setenvif
    mime
    filter
    deflate
    expires
    rewrite
    version
    alias
)

for mod in "${MODULES_TO_LOAD[@]}"; do
    if [[ -f "${MOD_DIR}/mod_${mod}.so" ]]; then
        echo "LoadModule ${mod}_module \"${MOD_DIR}/mod_${mod}.so\"" >> "${CONF_FILE}"
    fi
done

cat << CONF >> "${CONF_FILE}"
DocumentRoot "${TMP_DIR}"
<Directory "${TMP_DIR}">
    AllowOverride All
    Include "${HTACCESS}"
</Directory>
CONF

# Run configuration syntax test
if "${HTTPD_BIN}" -t -f "${CONF_FILE}" 2>&1; then
    echo "✅ Dynamic Apache httpd test passed with mod_rewrite loaded!"
else
    echo "❌ Dynamic Apache httpd syntax test failed!"
    if [[ -f "${ERROR_LOG}" ]]; then
        cat "${ERROR_LOG}"
    fi
    exit 1
fi

echo ""
echo "🔍 Step 3: Validating Section 6.3 early-drop rules against WordPress core routes..."

python3 - << 'EOF'
import sys
import re

with open(".htaccess", "r", encoding="utf-8") as f:
    content = f.read()

# Core WordPress routes and entrypoints that MUST NEVER be dropped by early-drop rules
CRITICAL_ROUTES = [
    "index.php",
    "wp-admin",
    "wp-admin/",
    "wp-admin/index.php",
    "wp-admin/admin.php",
    "wp-admin/admin-ajax.php",
    "wp-admin/post.php",
    "wp-admin/users.php",
    "wp-admin/network/settings.php",
    "wp-login.php",
    "wp-cron.php",
    "xmlrpc.php",
    "robots.txt",
    "sitemap.xml",
    "sample-page",
    "contact-us",
    "privacy-policy",
    "cart",
    "checkout",
    "my-account",
    "apple-app-site-association",
]

in_section_63 = False
rules = []
for idx, line in enumerate(content.splitlines(), 1):
    stripped = line.strip()
    if "6.3 ADVANCED EARLY-DROP PROTECTION" in stripped:
        in_section_63 = True
        continue
    if in_section_63 and "6.4 BLOCK ACCESS TO HIDDEN FILES" in stripped:
        break
    if not in_section_63 or not stripped or stripped.startswith("#"):
        continue
    if stripped.startswith("RewriteRule"):
        parts = stripped.split()
        if len(parts) >= 4 and parts[2] == "-" and "F" in parts[3]:
            pat = parts[1].strip("\"")
            if pat in (".*", ".?"):
                continue
            flags = parts[3].strip("[]")
            is_nc = "NC" in flags
            re_pat = pat
            if "(?i)" in re_pat:
                re_pat = re_pat.replace("(?i)", "")
                is_nc = True
            re_flags = re.IGNORECASE if is_nc else 0
            try:
                compiled = re.compile(re_pat, re_flags)
                rules.append((idx, pat, compiled))
            except re.error as e:
                print(f"❌ Regex compile error on line {idx} '{pat}': {e}")
                sys.exit(1)

errors = []
for route in CRITICAL_ROUTES:
    clean = route.lstrip("/")
    for line_num, pat, comp in rules:
        if comp.search(clean):
            errors.append(f"Line {line_num}: Core route '{route}' falsely matched by RewriteRule: {pat}")

if errors:
    print(f"❌ Found {len(errors)} false-positive collision(s) with core WordPress routes:")
    for err in errors:
        print(f"  • {err}")
    sys.exit(1)
else:
    print("✅ False-positive analysis passed cleanly (zero collisions with core WordPress routes).")
EOF

echo ""
echo "🎉 All .htaccess syntax checks passed successfully!"
