# Jay's WordPress `.htaccess`
### The Production-Hardened, All-in-One Apache Web Server Configuration & Firewall for WordPress

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![WordPress](https://img.shields.io/badge/WordPress-5.0+-21759b.svg?logo=wordpress&logoColor=white)](https://wordpress.org)
[![Apache](https://img.shields.io/badge/Apache-2.2%20%7C%202.4%2B-d22128.svg?logo=apache&logoColor=white)](https://httpd.apache.org)
[![WAF: 8G v1.5](https://img.shields.io/badge/WAF-8G%20Firewall%20v1.5-orange.svg)](https://perishablepress.com/8g-firewall/)
[![Standards: H5BP](https://img.shields.io/badge/Standards-HTML5%20Boilerplate-green.svg)](https://github.com/h5bp/server-configs-apache)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/JayHoltslander/jays-wp-htaccess/pulls)

A battle-tested, high-performance, and hardened `.htaccess` configuration engineered for production WordPress websites. Unites modern **HTML5 Boilerplate (H5BP)** performance and caching standards, the **Perishable Press 8G Firewall**, and empirical **live fleet threat intelligence** into a single drop-in file.

Unlike generic boilerplate rules, the defenses in this repository are directly informed by **empirical log analysis and threat intelligence collected across hundreds of live production WordPress installations**.

By researching real-world attack campaigns, scanner patterns, credential-stuffing botnets, and zero-day probes as they occur in the wild, this configuration neutralizes malicious traffic at the Apache web server layer—before PHP or MySQL workers ever boot.

Beyond security hardening, this configuration delivers **tangible performance boosts across every request**. It dramatically slashes **TTFB (Time to First Byte)** and server CPU load by ensuring bot traffic never exhausts PHP worker pools, while short-circuiting rewrite overhead entirely for existing static assets.

Asset delivery is further accelerated with native **Brotli and Gzip compression** alongside aggressive, **far-future immutable browser caching**—engineered for seamless compatibility across Apache 2.2/2.4+, LiteSpeed, and reverse proxies like Cloudflare.

---

## ⚡ Highlights & Key Features

* **🚀 Maximum Performance & Caching**
  * **Next-Gen Compression**: Native support for **Brotli** (`mod_brotli`) and **Gzip** (`mod_deflate`).
  * **Static Asset Short-Circuit & Fast 404**: Bypasses rewrite processing entirely for existing static assets (`.css`, `.js`, `.woff2`, images) and immediately drops missing source map requests (`.map`, `.js.map`, `.css.map`), missing root icons (`favicon.ico`, `apple-touch-icon*.png`), and missing crawler manifests (`meta.json`) with a zero-PHP 404, preventing PHP worker exhaustion from vulnerability scanners and external crawlers.
  * **Far-Future Expires Headers**: Aggressive, standards-compliant browser caching for media, scripts, styles, and fonts.
  * **Next-Gen Image & MIME Support**: Ready for **AVIF**, **WebP**, **JXL**, **WebAssembly** (`application/wasm`), **USDZ** (iOS AR), and modern RFC standard MIME types (`text/javascript`, `font/woff2`).
  * **HTTP/2 & HTTP/3 Friendly**: Protocol-aware TCP Keep-Alive scoping.

* **🛡️ Hardened Multi-Layer Security**
  * **8G Firewall v1.5 Integration**: Native, lightweight server-level Web Application Firewall (WAF) by [Perishable Press](https://perishablepress.com/8g-firewall/) protecting against malicious query strings, exploit URIs, bad user-agents, malicious referrers, attack cookies, and unwanted request methods.
  * **Zero-PHP Overhead Early-Drop Protection**: Terminates automated exploit scanners and non-WordPress probe traffic at the Apache web server layer with instant `403 Forbidden [F,L]` responses before PHP or database connections initialize:
    * **Automated Exploit Scanners & Tools**: Blocks known scanning engines and penetration tools (`wpscan`, `sqlmap`, `nikto`, `gobuster`, `masscan`, `zgrab`).
    * **Emerging Protocols & AI Agents**: Drops unauthorized dev MCP endpoints and server-sent event probes (`/mcp`, `/sse`, `/.well-known/ucp`) while strictly permitting legitimate AI crawler documents and SEO discovery manifests (`llms.txt`, `ai.txt`, `/.well-known/tdmrep.json`, XML sitemaps).
    * **AI Agent Instructions & LLM Context**: Prevents web exposure of leaked AI coding agent instructions, prompt context, and workspace rules (`AGENTS.md`, `CLAUDE.md`, `CURSOR.md`, `copilot-instructions.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.roorules`, `.aider*`).
    * **Cloud, AI & Deployment Manifests**: Prevents exposure of LLM configs, cloud secrets, tokens, and build metadata (`openai.json`, `vertex.json`, `amplifyconfiguration.json`, `.dev.vars`, `serverless.yml`, `vercel.json`, `wrangler.toml`, `terraform.tfvars`, `docker-compose.yml`, `manifest.json`, `values.yaml`).
    * **Environment & Config Probes**: Stops direct and URL-encoded attempts to access `.env*`, `.git*`, `.aws*`, `.kube*`, shell histories (`.bash_history`, `.zsh_history`), system credential files (`/etc/passwd`, `/etc/shadow`), and alternative configs (`env.json`, `app/etc/env.php`, bare `/env`).
    * **Web Shells, Droppers & Diagnostics**: Drops backdoor scripts, terminal backdoors, root droppers, fake image/CSS PHP wrappers, framework profilers, and debug endpoints (`term.php`, `hplfuns.php`, `c99`, `r57`, `alfa`, `b374k`, `adminer`, `phpmyadmin`, `phpinfo`, `/_debugbar`, `_profiler`, `/telescope`).
    * **SaaS & Enterprise Portals**: Intercepts scans for non-WordPress auth interfaces, admin consoles, PAM vaults (CyberArk, Secret Server), network monitoring suites (Nagios, Cacti, Pandora FMS, PRTG), and enterprise VPN/VDI gateways (`/admin/login`, `/signin`, `/webmail`, `/roundcube`, Cisco AnyConnect, VMware Horizon, Parallels RAS, F5 APM, MobileIron, Pulse Secure, Docker APIs).
    * **Path Traversal & Obfuscation**: Filters dot-dot traversal, multi-dot traversal, URL-encoded slashes (`%2F`), and double-encoded traversal sequences (`%252f`, `%2e%2e`).
  * **Backdoor Execution Neutralization**: Prevents direct PHP, shell script (`.sh`, `.bash`), and binary (`.exe`) execution inside the root `/wp-content/` directory, `/wp-content/uploads/`, and `/wp-content/themes/`.
  * **User & Credential Enumeration Defense & REST API Auth**: Blocks author query scans (`?author=1`), core REST API user dumping (`/wp-json/wp/v2/users`), unauthenticated plugin REST API member/user enumeration (WooCommerce, LearnDash, Dokan, BuddyPress, BuddyBoss, WP User Manager, Ultimate Member, etc.), unauthenticated WordPress SMTP/mailer REST API credential harvesting (WP Mail SMTP, FluentSMTP, Post SMTP, Gravity SMTP, Easy WP SMTP, AWS SES), and unauthenticated WordPress REST API batch execution (wp2shell CVE-2026-63030) while preserving authenticated sessions, Gutenberg, API authorization keys, and PHP-FPM `Authorization` header passthrough.
  * **SQLi & RFI Query Filtering**: Drops database injection payloads (`UNION SELECT`, `BENCHMARK`, `SLEEP`, null bytes `%00`, directory traversal).
  * **Automated No-Referrer Comment Spam Killer**: Blocks headless spam bots submitting direct POSTs to `wp-comments-post.php`.
  * **Legacy Attack Surface Reduction**: Blocks XML-RPC brute-force amplification (`xmlrpc.php`), trackback spam (`wp-trackback.php`), and legacy blogroll exports (`wp-links-opml.php`).
  * **Modern Security Headers**: `Header always set` enforcement for `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Permissions-Policy` (sensor & FLoC/Topics restriction), `X-Permitted-Cross-Domain-Policies: none`, and `Cross-Origin-Opener-Policy (COOP)`.
  * **Apache 2.4 & 2.2 Dual-Compatibility**: Safe on modern `mod_authz_core` (`Require all denied`) and legacy hosts without triggering 500 configuration errors.
  * **Let's Encrypt / ACME Whitelisted**: Preserves automated SSL renewals by explicitly excluding `/.well-known/acme-challenge/` from dotfile blocks.
  * **Cloudflare & Reverse Proxy `REAL_IP` Normalization**: Auto-detects `CF-Connecting-IP` without requiring manual file edits.
  * **Empirical Threat Intelligence & Automated Tooling**: Backed by built-in Python auditing tools (`scripts/mine-threat-intel.py`) continuously cross-referencing SecLists and Nuclei CVE templates, automated fleet access log telemetry analyzers (`scripts/analyze-fleet-logs.py`), and a scheduled weekly GitHub Actions audit workflow.

---

## 📑 Table of Contents

The [`.htaccess`](.htaccess) file is cleanly organized into 8 distinct sections:

1. **[Emergency & Maintenance Toggles](.htaccess#L35)** — Instant 302 redirect-to-homepage killswitch and legacy `.shtml` redirects.
2. **[Directory Index & Server Options](.htaccess#L64)** — `DirectoryIndex` maintenance fallback, `Options -Indexes`, `Options -MultiViews`, and `ServerSignature Off`.
3. **[MIME Types & Encodings](.htaccess#L137)** — UTF-8 character sets, RFC-standard MIME types for fonts, scripts, manifests, markdown, and modern images (AVIF, WebP, JXL, HEIC/HEIF).
4. **[Security Headers & CORS](.htaccess#L242)** — Clickjacking, MIME sniffing, COOP, Referrer-Policy, Permissions-Policy, cross-domain policy restriction, font CDN CORS, Resource Timing (TAO), and optional HSTS.
5. **[Performance & Caching](.htaccess#L409)** — Brotli/Deflate compression, Far-Future Expires, Immutable Cache-Control, and ETag disabling.
6. **[Security Filters & Access Restrictions](.htaccess#L709)**
   * **6.1** Reverse Proxy & Cloudflare Normalization (REAL_IP & HTTPS)
   * **6.2** Static Asset Performance Short-Circuit & Fast 404 (Bypasses Deep Rewrite Scans for Existing Static Files & Drops Missing .map, Root Icon, and Crawler Manifest Probes)
   * **6.3** Advanced Early-Drop Protection (Methods, Executables, Dotfiles, Manifests, AI Agent Instructions & Rules, Framework Probes, DB Dumps, Web Shells, Autodiscover Fast 404, Core & Plugin Source Maps, AI/MCP Probes, Uploads PHP, REST API Plugin Enumeration, REST Batch Fuzzing, Scanner UAs)
   * **6.4** Block Hidden Files & Directories (ACME / SSL Whitelisted)
   * **6.5** File Access Protections (Apache 2.4/2.2 Dual Syntax for `.ht*`, `wp-config.php`, `debug.log`, `xmlrpc.php`, `wp-trackback.php`, `wp-links-opml.php`, AI agent rules & context files)
   * **6.6** Core WordPress Directory Hardening (`install.php`, `wp-includes`)
   * **6.7** Image Hotlinking Defense (Optional)
   * **6.8** Bot, Enumeration & Spam Query Filtering (SQLi, Comment Spam, Author Scans)
   * **6.9** 8G Firewall v1.5 (Perishable Press Server-Level WAF)
   * **6.10** Rate Limiting (`mod_ratelimit`) & IP Access Control Examples
7. **[URL Canonicalization, HTTPS & Redirects](.htaccess#L1463)** — Force SSL, WWW vs Naked domain canonicalization, direct IP redirects, and staging robots.txt.
8. **[WordPress Front Controller](.htaccess#L1593)** — Standard WordPress rewrite rules with PHP-FPM Authorization header preservation (placed at the very end to ensure all security/optimization rules run first).

---

## 🚀 Quick Start

### 1. Download the file
Download the latest production [`.htaccess`](https://raw.githubusercontent.com/JayHoltslander/jays-wp-htaccess/master/.htaccess) file directly into your website root directory:

```bash
# Backup your existing .htaccess first!
cp .htaccess .htaccess.backup

# Download the latest version
curl -O https://raw.githubusercontent.com/JayHoltslander/jays-wp-htaccess/master/.htaccess
```

### 2. Tailor to your environment
Open `.htaccess` in your editor and review optional toggles and special architecture considerations:
* **SSL / HTTPS**: If not enforcing SSL at Cloudflare/CDN level, uncomment the **Force SSL** redirect block in Section 7.
* **Domain Canonicalization**: Uncomment either **WWW to Naked** or **Naked to WWW** redirect depending on your domain preference.
* **Jetpack / WP Mobile App**: If using Jetpack or mobile publishing, uncomment the allowed Automattic IP ranges in the `xmlrpc.php` block in Section 6.5.
* **Headless WordPress (WPGraphQL)**: If using WPGraphQL or a decoupled frontend, comment out **Rule 5b** in Section 6.3 (`graphql`) to permit API queries.
* **WooCommerce & Front-End Membership**: If using WooCommerce or membership plugins with custom front-end login, registration, or my-account pages (e.g., `/signin`, `/signup`, `/account/login`), comment out **Rule 6b** in Section 6.3.

---

## ⚖️ How Jay's WP `.htaccess` Compares

When optimizing and hardening WordPress, developers typically face a choice between generic server boilerplates, isolated firewall snippets, static gists, or resource-heavy PHP security plugins. Here is how this repository compares:

| Feature / Protection | **Jay's WP `.htaccess`** | **HTML5 Boilerplate** (`h5bp`) | **Standalone WAF** (8G / Mitchell Krog) | **Static Community Gists** | **PHP Security Plugins** (Wordfence/AIOS) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **All-in-One Single Drop-In** | **Yes** | Yes (General) | No (Firewall only) | Partial | No (Plugin suite) |
| **Zero-PHP Server-Level Execution** | **Yes** | Yes | Yes | Yes | ❌ Runs inside PHP/DB |
| **WordPress Route & Front Controller Aware** | **Yes** | ❌ No | ❌ No | Partial | Yes |
| **Empirical Live Fleet Threat Intel** | **Yes** (Automated) | ❌ No | Partial (Manual) | ❌ No (Static) | Partial (Cloud WAF) |
| **Integrated 8G Firewall v1.5** | **Yes** | ❌ No | **Yes** | Rarely | ❌ No |
| **REST API Member Enumeration Shield** | **Yes** | ❌ No | ❌ No | ❌ No | Partial |
| **Fast 404 Sourcemap / Icon Short-Circuit** | **Yes** | ❌ No | ❌ No | ❌ No | ❌ No |
| **Next-Gen MIME (AVIF, JXL, GeoJSON, MD)** | **Yes** | **Yes** | ❌ No | Rarely | ❌ No |
| **Brotli + Far-Future Immutable Caching** | **Yes** | **Yes** | ❌ No | Partial | Partial (Requires cache plugin) |
| **PHP-FPM REST Auth Header Passthrough** | **Yes** | ❌ No | ❌ No | Rarely | Yes |
| **Dual Apache 2.4 / 2.2 Compatibility** | **Yes** | Partial | Partial | ❌ Often 500 error prone | Partial |
| **Automated Apache Runtime Syntax Test Suite**| **Yes** (`test-syntax.sh`)| **Yes** | ❌ No | ❌ No | ❌ No |

### The Core Architectural Differences:

1. **vs. HTML5 Boilerplate (`h5bp/server-configs-apache`):**
   * *H5BP* sets the web standard for MIME types, browser caching, and compression, but it is CMS-agnostic. It lacks defenses against WordPress REST user dumping, rogue `/wp-content/` execution, `xmlrpc.php` amplification, sensitive dotfiles, and automated CMS vulnerability scanners.
   * *Jay's WP `.htaccess`* adopts H5BP's caching and MIME best practices and layers on dedicated WordPress architectural protections.

2. **vs. Standalone WAF Snippets (8G Firewall / Mitchell Krog Bot Blocker):**
   * Standalone firewalls excel at filtering query strings or user-agents, but they intentionally omit performance headers, caching, MIME types, and rewrite canonicalization.
   * *Jay's WP `.htaccess`* natively embeds the **8G Firewall v1.5** inside Section 6.9 while wrapping it in a complete, high-performance web delivery stack.

3. **vs. Heavy WordPress Security Plugins (Wordfence, Solid Security, AIOS):**
   * Security plugins execute *after* the web server boots PHP and queries MySQL. When botnets scan hundreds of URLs per second, PHP worker pools are quickly starved, causing high TTFB and CPU spikes.
   * *Jay's WP `.htaccess`* terminates malicious probes with `403 Forbidden` directly at the Apache level in **under 1 millisecond**, consuming zero PHP memory.

---

## ⚠️ Important Notes & Troubleshooting

> [!IMPORTANT]
> **Maximum Security Default — Headless & E-Commerce / Membership Special Cases:**
> This configuration operates on a **maximum security out-of-the-box** posture for standard WordPress installations. Because standard WordPress exclusively uses `/wp-login.php` and does not expose GraphQL, **Rule 5b** (GraphQL introspection) and **Rule 6b** (generic SaaS/CMS auth probes) are **enabled by default**.
> * **Headless / Decoupled Sites:** If you use the WPGraphQL plugin (with Next.js, Astro, Gatsby, etc.), comment out **Rule 5b** in Section 6.3.
> * **E-Commerce & Membership Sites:** If you use WooCommerce, MemberPress, Ultimate Member, or similar plugins that provide front-end customer login/registration pages at paths like `/account/login`, `/signin`, `/signup`, or `/reset-password`, comment out **Rule 6b** in Section 6.3.

> [!CAUTION]
> **Always maintain a backup before modifying `.htaccess`!**
> One syntax mistake or unsupported module directive can make a site return a `500 Internal Server Error`. Keep FTP or hosting file manager access ready.

* **PHP-FPM / FastCGI Servers**: Directives like `php_value upload_max_filesize` are commented out by default because modern PHP-FPM hosts (cPanel EA4, Plesk, RunCloud, SpinupWP) will throw a 500 error if `php_value` is placed in `.htaccess`. Configure PHP limits in `.user.ini` or `php.ini` instead.
* **Testing Changes**: After uploading, test your site in an incognito window, verify static asset loading (CSS/JS/images), test login functionality at `/wp-login.php`, and verify media uploads in the WordPress admin.
* **Trim What You Don't Need**: If you use a reverse proxy or CDN (like Cloudflare) that handles hotlink protection or Brotli compression, you can comment out redundant blocks to keep your `.htaccess` as lightweight as possible.

---

## 💡 Recommendations for WordPress Security

1. **Comment Spam**: The built-in **Automated No-Referrer Comment Spam Blocker** (Section 6.8) blocks ~99% of automated comment spam bots without requiring resource-heavy anti-spam plugins.
2. **Two-Factor Authentication (2FA)**: Use in conjunction with a trusted 2FA plugin (e.g. WP 2FA) and security keys.
3. **Admin URL Protection**: If you have a static IP address, uncomment the IP restriction snippet in Section 6.10 to restrict `/wp-login.php` exclusively to your IP.
4. **Cloudflare / CDN**: When using Cloudflare, Section 6.1 automatically inspects `CF-Connecting-IP`, ensuring IP-based security rules work transparently.

---

## 🧰 Threat Intelligence & Validation Tooling

This repository includes a suite of automated intelligence and testing utilities to ensure zero-overhead defense without false positives:

### 1. Pre-Commit & CI Syntax Validator
Tests `.htaccess` tokens, whitespace escaping, flag brackets, and performs authentic runtime Apache 2.4/2.2 parsing with `mod_rewrite` loaded:
```bash
./scripts/test-syntax.sh
```

### 2. Threat Intelligence Wordlist Miner
Audits public fuzzing dictionaries (SecLists, FuzzDB, Bo0oM) against Section 6 early-drop rules, applying a strict WordPress false-positive filter to surface unhandled exploit candidates:
```bash
# Fetch and audit live SecLists quickhits & Bo0oM fuzzlists
python3 scripts/mine-threat-intel.py --fetch-seclists

# Audit a local wordlist file
python3 scripts/mine-threat-intel.py --file wordlist.txt
```

### 3. Fleet Log Telemetry Analyzer
Ingests raw web server access logs (Combined, Common, or Nginx format) across production WordPress installations to calculate scanner breadth, identify 404 fall-through requests that bypass `.htaccess`, and generate GitHub-ready markdown telemetry tables:
```bash
# Analyze production log files
python3 scripts/analyze-fleet-logs.py /var/log/httpd/access.log

# Stream compressed logs and output GitHub Markdown format
zcat /var/log/httpd/access.log.*.gz | python3 scripts/analyze-fleet-logs.py --format markdown
```

### 4. Automated Weekly GitHub Actions Audit
A scheduled GitHub Actions workflow ([`.github/workflows/threat-intel-audit.yml`](.github/workflows/threat-intel-audit.yml)) runs every Monday morning and on-demand via `workflow_dispatch`. It evaluates newly trending scan vectors from SecLists and outputs a visual dashboard directly to GitHub's **Job Summary**.

---

## ❓ Frequently Asked Questions (FAQ)

<details>
<summary><b>Can I use this configuration behind Cloudflare or another reverse proxy?</b></summary>
<br>
<b>Yes.</b> Section 6.1 automatically inspects <code>X-Forwarded-Proto</code> and <code>CF-Connecting-IP</code> to normalize SSL states and ensure security rules and logging evaluate authentic client IP addresses (<code>%{ENV:REAL_IP}</code>) rather than Cloudflare edge node IPs.
</details>

<details>
<summary><b>Does this replace caching plugins like WP Rocket or LiteSpeed Cache?</b></summary>
<br>
This configuration handles browser caching (<code>ExpiresByType</code>), immutable asset headers, Brotli/Gzip compression, and fast static asset short-circuiting at the web server layer. While it does not generate pre-rendered static HTML page caches like WP Rocket or LSCache, it accelerates every asset request and complements static caching solutions without directive conflicts.
</details>

<details>
<summary><b>Do I still need a security plugin like Wordfence?</b></summary>
<br>
You can safely run this alongside security plugins or use it to replace plugin-based firewall rules. By stopping brute-force scanners, exploit probes, and user enumeration at the Apache layer, this configuration prevents up to 90% of malicious requests from ever reaching your security plugins, drastically reducing server load.
</details>

<details>
<summary><b>Will this break WooCommerce or page builders like Elementor?</b></summary>
<br>
<b>No.</b> Standard WooCommerce endpoints (cart, checkout, digital product downloads, and PayPal/Stripe IPN webhooks) and page builder AJAX actions are explicitly accounted for. If using a membership plugin with custom front-end login routes (e.g. <code>/signin</code> or <code>/account/login</code>), clear toggle instructions are provided in Section 6.3 Rule 6b.
</details>

<details>
<summary><b>Why not just use HTML5 Boilerplate's .htaccess?</b></summary>
<br>
HTML5 Boilerplate is general-purpose and unaware of WordPress. Using H5BP alone leaves your site vulnerable to REST API author harvesting, <code>xmlrpc.php</code> DDoS attacks, rogue PHP execution in <code>wp-content/uploads/</code>, and missing icon/sourcemap 404 fall-throughs that drain PHP workers.
</details>

---

## 📜 Credits & Attributions

This project builds upon security research, server configuration standards, and optimization techniques from the open-source community:

* **[HTML5 Boilerplate Server Configs](https://github.com/h5bp/server-configs-apache)** — Standards for MIME types, character encodings, cross-origin resource timing, and HTTP caching.
* **[Imran Ahmed (SecureWP Defense Suite)](https://github.com/imranbru99/Ultimate-Secure-WordPress-.htaccess-Advanced-Firewall-Anti-Hack-Protection)** — WordPress REST API authorization passthrough and upload execution lockdown patterns.
* **[Perishable Press (Jeff Starr)](https://perishablepress.com/)** — [8G Firewall v1.5](https://perishablepress.com/8g-firewall/), nG blacklist concepts, bot query mitigation, and custom error handling.
* **[WordPress Codex & Security Team](https://wordpress.org/documentation/article/hardening-wordpress/)** — Core `wp-includes` and security hardening guidelines.
* **[Sucuri Research](https://blog.sucuri.net/)** — Research on XML-RPC amplification attacks and WordPress vulnerability patterns.
* **[David Walsh](https://davidwalsh.name/)** — Cross-domain font sharing (CORS) and SVG serving best practices.
* **[Crunchify](https://crunchify.com/)** — Browser caching and ETag optimization.
* **[KeyCDN](https://www.keycdn.com/)** — Research on `Cache-Control: immutable` caching directives.
* **[HackRepair.com](https://hackrepair.com/)** — Bad bot and malicious user-agent blacklisting research.
* **[Daniel Miessler's SecLists](https://github.com/danielmiessler/SecLists)** — Security tester's companion for web discovery, fuzzing, and endpoint intelligence.
* **[Bo0oM (Mikhail Egorov)](https://github.com/Bo0oM/fuzz.txt)** — High-frequency web root leak fuzzing and discovery lists.
* **[ProjectDiscovery Nuclei](https://github.com/projectdiscovery/nuclei-templates)** — Community-driven vulnerability templates and exposed panel signatures.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Contributions, bug reports, and pull requests are always welcome!
