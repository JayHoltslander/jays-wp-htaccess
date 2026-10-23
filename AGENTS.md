# Agent Guidelines & Repository Directives

This document provides mandatory operational instructions for AI assistants (Antigravity, Claude Code, Cursor, Copilot, etc.) working within this repository.

---

## 🚨 MANDATORY SESSION STARTUP DIRECTIVE
At the beginning of **every new conversation** or before starting any new work in this repository, the AI assistant **MUST immediately check the repository's open issues** (using `list_issues` or GitHub tools).
- Check for open issues, scanner pattern reports, or triage requests.
- Identify and summarize any open items that need action, reporting them to the user as step 1.
- Prioritize real-world exploit observations and fleet telemetry reports (`[Bot Intelligence] Proposed early-drop rules for active scanner patterns...`).

---

## 🚨 MANDATORY VERSIONING PROTOCOL
Every single change or commit that modifies `.htaccess` **MUST** bump the version number and update the release date in the `.htaccess` header banner:

```apache
# Version:      X.Y.Z
# Released:     YYYY-MM-DD
```

### Versioning Rules:
- **Patch (`X.Y.Z+1`):** Expanding existing signature lists (e.g. adding new bot User-Agents, exploit paths, file/directory probe names, diagnostic aliases, or credential extensions), regex bugfixes, small directive tweaks, or documentation updates.
- **Minor (`X.Y+1.0`):** Adding brand-new security sections/categories, new functional modules (e.g. CORS/CORP, Brotli, marker systems), or major architectural directive additions.
- **Major (`X+1.0.0`):** Breaking structural overhauls, fundamental reorganization, or core architecture changes.

---

## 🛡️ Architectural & Compatibility Standards

1. **Dual Apache 2.4 & 2.2 Compatibility:**
   - Always wrap authorization and access control directives with dual `<IfModule mod_authz_core.c>` (Apache 2.4+ `Require all denied`) and fallback `<IfModule !mod_authz_core.c>` (`Order allow,deny` / `Deny from all`).
   - Never write naked `Order/Deny` or `Require` directives that could trigger HTTP 500 errors on differing host modules.

2. **PHP-FPM & Reverse Proxy Safety:**
   - Never uncomment `php_value` directives by default (causes HTTP 500 on PHP-FPM / FastCGI hosts).
   - Maintain reverse-proxy compatibility (`SetEnvIf X-Forwarded-Proto https HTTPS=on` and `%{ENV:REAL_IP}` normalization).

3. **Front Controller Ordering:**
   - The `# BEGIN WordPress ... # END WordPress` front controller block **MUST** remain at the absolute bottom of `.htaccess` so that custom security rewrites and early-drop protections execute before WordPress intercepts requests.

4. **Zero-Downtime Safe Defaults:**
   - Keep domain-specific, IP-specific, and SSL-forcing rules commented out by default with clear educational caveats to avoid locking users out or breaking local dev environments.

---

## 🧪 Mandatory Pre-Commit Syntax Validation Protocol

Before staging or committing any change to `.htaccess`, you **MUST** run the automated syntax test suite:

```bash
./scripts/test-syntax.sh
```

### Critical Verification Rules:
1. **Never Rely on Static `httpd -t` Without `mod_rewrite` Loaded:**
   - Default Apache installations (such as macOS `/etc/apache2/httpd.conf`) have `mod_rewrite` disabled by default. Running `httpd -t` against a default config will silently skip all `<IfModule mod_rewrite.c>` blocks and output a false-positive `Syntax OK`.
   - Always run `./scripts/test-syntax.sh`, which explicitly loads `mod_rewrite`, sets up an authentic `<Directory>` context with `AllowOverride All`, and tests actual runtime directive evaluation.

2. **Strict Quoting of Whitespace in Directives:**
   - Apache `.htaccess` directives tokenize on unquoted whitespace before parsing regex patterns. Any `RewriteCond` or `RewriteRule` pattern containing literal spaces, escaped spaces `\s`, or character classes with spaces `[ ]` **MUST** be enclosed in double quotes (e.g., `RewriteCond %{THE_REQUEST} "^[A-Z]+[ ]+..." [NC]`). Failure to quote patterns with spaces causes Apache to misparse arguments and throw fatal `RewriteCond: bad flag delimiters` HTTP 500 errors.

3. **Strict Flag Delimiters:**
   - Never place spaces between flags inside brackets (e.g. `[NC,OR]`, never `[NC, OR]`). Every opening bracket `[` must have a matching closing bracket `]`.

---

## 📖 README & Documentation Synchronization Protocol

Every change or commit **MUST** evaluate whether modifications to `README.md` are justified:

1. **Feature & Protection Highlights:**
   - When expanding Section 6.3 early-drop protections, security headers, Fast-404 handling, MIME types, or compression directives, verify if `README.md` (specifically the **⚡ Highlights & Key Features** bullet points) should be updated to mention newly covered categories, manifests, tools, or threat vectors.

2. **Table of Contents Line Anchors:**
   - If line additions, deletions, or structural changes in `.htaccess` shift the starting line number of any of the 8 major numbered sections, update the corresponding markdown anchor links under **📑 Table of Contents** in `README.md` (e.g. `[URL Canonicalization, HTTPS & Redirects](.htaccess#L1337)`).

3. **Usage Guidance & Configuration Toggles:**
   - If optional toggles, directive syntax, server requirements, or recommended configurations change, ensure that setup instructions and examples in `README.md` remain fully accurate and synchronized with `.htaccess`.

4. **Credits & Attributions ("Credit Where Credit is Due"):**
   - Always give credit where credit is due: When directives, regex patterns, firewall rules, or optimization techniques are adapted from, inspired by, or based upon external research, articles, tools, or open-source repositories (e.g. Perishable Press, HTML5 Boilerplate, Sucuri, HackRepair, etc.), ensure explicit attribution and links are included under **📜 Credits & Attributions** in `README.md` as well as within the relevant `.htaccess` section comments.

---

## 🔒 Git & Security Protocols

1. **Commit Authorship:**
   - Ensure all commits are authored by the repository maintainer (`Jay Holtslander <j.holtslander@gmail.com>`).

2. **Explicit Push Authorization:**
   - Never execute `git push` autonomously. Always commit locally, present the changes to the user, and wait for the user's explicit `"push to git"` confirmation before pushing to remote.

## 🛡️ Issue Triage & Fleet Bot Intelligence Protocol

### Standing Directive: Proactive Issue Monitoring
* **Proactively Check Open Issues:** Regularly check for any filed issues in this repo that may have been submitted and need triaging (using GitHub tools or `list_issues`). Action on them if appropriate for this project.
* **Prioritize Fleet Telemetry:** Issues titled `[Bot Intelligence] Proposed early-drop rules for active scanner patterns (YYYY-MM-DD)` originate from production fleet log telemetry across dozens of live WordPress sites. Treat these as high-priority real-world exploit observations.

---

### 🧰 Repository Intelligence & Validation Tooling
* **Syntax & Token Validation:** `./scripts/test-syntax.sh` — Validates static tokens, quoted whitespace, flag delimiters, and tests runtime Apache parsing with `mod_rewrite`.
* **Threat Intelligence Miner:** `./scripts/mine-threat-intel.py` — Audits wordlists (SecLists, FuzzDB, or custom files) against Section 6.3 rules, identifies coverage gaps, and flags false-positive risks.
* **Fleet Log Telemetry Analyzer:** `./scripts/analyze-fleet-logs.py` — Ingests raw server access logs across fleet WordPress sites, identifies 404 fall-throughs that bypass `.htaccess`, and outputs structured markdown tables.

### Intake & Action Workflow:
When triaging open issues or incoming bot reports, follow this procedure:

1. **Threat Classification:**
   Classify each candidate path into the appropriate Section 6 submodule in `.htaccess`:
   * **Rule 1:** Non-WordPress executable extensions (`.jsp`, `.asp`, `.do`, `.action`).
   * **Rule 2:** Environment, config, and cloud metadata (`.env.*`, `.aws`, `.kube`, `.git`).
   * **Rule 3:** Developer manifests, cloud credentials, tokens, lockfiles, and private keys (`id_rsa`, `private-key`, `firebase.json`, `dist/manifest.json`).
   * **Rule 4:** Database dumps, backups, archives, and editor backups (`.sql`, `.bak`, `.save`, `~`).
   * **Rule 5:** Web shells, diagnostic endpoints, arbitrary file reads (`api/fs/read`, `api/system/fileView`, `phpinfo`).
   * **Rule 5b:** GraphQL unauthenticated introspection (`/graphql`, `/api/graphql`, `/v1/graphql` - enabled by default, commented out for WPGraphQL/headless).
   * **Rule 6:** Enterprise appliances, profilers, Swagger/OpenAPI, Next.js/Nuxt (`swagger`, `openapi.json`, `_next`, `console(/.*)?`).
   * **Rule 6b:** Generic CMS / SaaS auth endpoints (`admin/login`, `signin`, `signup`, `backoffice`, `dashboard/...` - enabled by default, commented out for WooCommerce/membership front-end login pages).
   * **Rule 7b:** Encoded slashes, double-encoded dots, and traversal (`%2e%2e%2f`, `%2F.env`).
   * **Rule 8:** Malware staging and rogue `.php` files directly in `wp-content/` (`^wp-content/[^/]+\.php`).

2. **False-Positive Safety Bounds:**
   Before adopting any rule, verify it does **NOT** break legitimate WordPress functionality:
   * **Core & Standard Routes:** Ensure standard routes are never matched (`/wp-admin/*`, `/wp-login.php`, `admin-ajax.php`, `wp-cron.php`, `xmlrpc.php`, `sitemap.xml`, `robots.txt`, `.well-known/*`).
   * **WooCommerce & Popular Plugins:** Keep digital product downloads (`/downloads/*`, `/cart/*`, `/checkout/*`), payment webhooks (PayPal, Stripe IPN), and form plugins (Gravity Forms, WPForms) unblocked.
   * **Architecture Caveats:** For endpoints that may conflict with special WordPress architectures (such as WPGraphQL for headless sites, or custom front-end account pages in membership plugins), clearly document them in `.htaccess` and `README.md` with instructions for site operators on how to comment them out.

3. **Release & Issue Resolution:**
   Every adopted change **MUST** execute the standard repository release cycle:
   * **Patch Version Bump:** Increment the Patch version (`X.Y.Z+1`) in `.htaccess` and update the release date (`Released: YYYY-MM-DD`).
   * **Syntax Suite:** Run `./scripts/test-syntax.sh` to ensure Apache 2.4/2.2 dual-compatibility, proper bracket matching, and double-quoting of any pattern containing whitespace or character classes.
   * **TOC Sync:** Update `README.md` Table of Contents anchor line numbers if section starting lines shifted.
   * **Issue Resolution:** Commit referencing the issue (e.g. `feat(early-drop): add bare private keys and openapi probes (closes #1)`), and reply on the GitHub issue detailing which patterns were adopted, any patterns intentionally excluded (with false-positive reasoning), and the resulting release version.
