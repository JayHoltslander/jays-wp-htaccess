# Jay's WordPress `.htaccess`

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![WordPress](https://img.shields.io/badge/WordPress-5.0+-21759b.svg?logo=wordpress&logoColor=white)](https://wordpress.org)
[![Apache](https://img.shields.io/badge/Apache-2.2%20%7C%202.4%2B-d22128.svg?logo=apache&logoColor=white)](https://httpd.apache.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/JayHoltslander/jays-wp-htaccess/pulls)

A production-tested, high-performance, and hardened `.htaccess` configuration for WordPress websites. Designed to maximize speed, minimize TTFB (Time to First Byte), block automated bot scans before PHP boots, and provide seamless compatibility across Apache 2.2/2.4+, LiteSpeed, and reverse proxies like Cloudflare.

---

## ⚡ Highlights & Key Features

* **🚀 Maximum Performance & Caching**
  * **Next-Gen Compression**: Native support for **Brotli** (`mod_brotli`) and **Gzip** (`mod_deflate`).
  * **Static Asset Short-Circuit & Fast 404**: Bypasses rewrite processing entirely for existing static assets (`.css`, `.js`, `.woff2`, images) and immediately drops missing source map requests (`.js.map`, `.css.map`) and missing root icons (`favicon.ico`, `apple-touch-icon*.png`) with a zero-PHP 404, preventing PHP worker exhaustion from vulnerability scanners.
  * **Far-Future Expires Headers**: Aggressive, standards-compliant browser caching for media, scripts, styles, and fonts.
  * **Next-Gen Image & MIME Support**: Ready for **AVIF**, **WebP**, **JXL**, **WebAssembly** (`application/wasm`), **USDZ** (iOS AR), and modern RFC standard MIME types (`text/javascript`, `font/woff2`).
  * **HTTP/2 & HTTP/3 Friendly**: Protocol-aware TCP Keep-Alive scoping.

* **🛡️ Hardened Multi-Layer Security**
  * **8G Firewall v1.5 Integration**: Native, lightweight server-level Web Application Firewall (WAF) by [Perishable Press](https://perishablepress.com/8g-firewall/) protecting against malicious query strings, exploit URIs, bad user-agents, malicious referrers, attack cookies, and unwanted request methods.
  * **Zero-PHP Overhead Early-Drop Protection**: Kills known automated exploit tools (`wpscan`, `sqlmap`, `nikto`, `gobuster`), web shells & droppers (`c99`, `r57`, `alfa`, `b374k`, `wp-plain.php`, `ioxi-o.php`), standalone database managers (`adminer`, `phpmyadmin`, `sql.php`), CouchDB exposure probes (`/_all_dbs`), cluster/Kubernetes discovery APIs (`/api/v1/nodes`, in-pod `serviceaccount/token`), Docker Compose specs (`compose.yaml`), cloud, PaaS & AI deployment manifests (`serverless.yml`, `vercel.json`, `fly.toml`, `wrangler.toml`, `netlify.toml`, `terraform.tfvars`, Helm `values.yaml`, `.s3cfg`, `.pgpass`), build & frontend manifests (`dist/manifest.json`, `build/manifest.json`), editor sync credentials & backups (`.ftpconfig`, `.remote-sync.json`, `sftp-config.json`, `.save`, `~`), non-WordPress framework config/storage probes (`/config/*.json`, `/storage/logs/`), modern SSR & framework RCE exploits (Next.js `/_next`, Server Actions `__nextjs`, Nuxt `/_nuxt`, Metabase `api/session/properties`, Windmill `api/w/`), OpenAPI & Swagger specs (`/swagger`, `openapi.json`), enterprise/VPN portals & appliances (SonicWall `sonicui`, FortiProxy `fpui`, SSL-VPN, Ivanti / Pulse Secure `dana-cached`, `/Remote`, `/vpn/`, Exchange `owa`, Zimbra, SharePoint `_layouts`, SCADA/PLC `webvisu`), probe discovery endpoints (`/version`, `/api/status`, `/web_api/`, bare `/server-status`), Linux `/proc/` filesystem probes, Vite/RSC dev server traversal (`@fs`, `@vite`, `__vite`), obfuscated, encoded dot & double-encoded path traversal (`%252f`, `%2e%2e`, `admin%2F.env`, `....//`), backup plugin staging folders (`updraft`, `ai1wm-backups`, `wp-snapshots`), documentation/readme fingerprinting files (`readme.html`, `license.txt`, `changelog.txt`), IDE/CI metadata probes (`.vscode`, `.idea`, `.gitlab-ci`, `.github`), bare & suffixed SSH/SSL private keys (`id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`, `private-key`), and non-WP executables (`.jsp`, `.asp`, `.exe`, `.zul`) at the Apache layer before PHP or database workers initialize.
  * **Backdoor Execution Neutralization**: Prevents direct PHP execution inside the root `/wp-content/` directory, `/wp-content/uploads/`, and `/wp-content/themes/`.
  * **User Enumeration Defense**: Blocks both author query scans (`?author=1`) and REST API user dumping (`/wp-json/wp/v2/users`).
  * **SQLi & RFI Query Filtering**: Drops database injection payloads (`UNION SELECT`, `BENCHMARK`, `SLEEP`, null bytes `%00`, directory traversal).
  * **Automated No-Referrer Comment Spam Killer**: Blocks headless spam bots submitting direct POSTs to `wp-comments-post.php`.
  * **Legacy Attack Surface Reduction**: Blocks XML-RPC brute-force amplification (`xmlrpc.php`), trackback spam (`wp-trackback.php`), and legacy blogroll exports (`wp-links-opml.php`).
  * **Modern Security Headers**: `Header always set` enforcement for `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Permissions-Policy` (sensor & FLoC/Topics restriction), `X-Permitted-Cross-Domain-Policies: none`, and `Cross-Origin-Opener-Policy (COOP)`.
  * **Apache 2.4 & 2.2 Dual-Compatibility**: Safe on modern `mod_authz_core` (`Require all denied`) and legacy hosts without triggering 500 configuration errors.
  * **Let's Encrypt / ACME Whitelisted**: Preserves automated SSL renewals by explicitly excluding `/.well-known/acme-challenge/` from dotfile blocks.
  * **Cloudflare & Reverse Proxy `REAL_IP` Normalization**: Auto-detects `CF-Connecting-IP` without requiring manual file edits.

---

## 📑 Table of Contents

The [`.htaccess`](.htaccess) file is cleanly organized into 8 distinct sections:

1. **[Emergency & Maintenance Toggles](.htaccess#L35)** — Instant 302 redirect-to-homepage killswitch and legacy `.shtml` redirects.
2. **[Directory Index & Server Options](.htaccess#L64)** — `DirectoryIndex` maintenance fallback, `Options -Indexes`, `Options -MultiViews`, and `ServerSignature Off`.
3. **[MIME Types & Encodings](.htaccess#L137)** — UTF-8 character sets, RFC-standard MIME types for fonts, scripts, manifests, and modern images (AVIF, WebP, JXL, HEIC/HEIF).
4. **[Security Headers & CORS](.htaccess#L236)** — Clickjacking, MIME sniffing, COOP, Referrer-Policy, Permissions-Policy, cross-domain policy restriction, font CDN CORS, and optional HSTS.
5. **[Performance & Caching](.htaccess#L388)** — Brotli/Deflate compression, Far-Future Expires, Immutable Cache-Control, and ETag disabling.
6. **[Security Filters & Access Restrictions](.htaccess#L685)**
   * **6.1** Reverse Proxy & Cloudflare Normalization (REAL_IP & HTTPS)
   * **6.2** Static Asset Performance Short-Circuit & Fast 404 (Bypasses Deep Rewrite Scans for Existing Static Files & Drops Missing .map / Root Icon Probes)
   * **6.3** Advanced Early-Drop Protection (Methods, Executables, Dotfiles, Manifests, Framework Probes, DB Dumps, Web Shells, Uploads PHP, REST API, Scanner UAs)
   * **6.4** Block Hidden Files & Directories (ACME / SSL Whitelisted)
   * **6.5** File Access Protections (Apache 2.4/2.2 Dual Syntax for `.ht*`, `wp-config.php`, `debug.log`, `xmlrpc.php`, `wp-trackback.php`, `wp-links-opml.php`)
   * **6.6** Core WordPress Directory Hardening (`install.php`, `wp-includes`)
   * **6.7** Image Hotlinking Defense (Optional)
   * **6.8** Bot, Enumeration & Spam Query Filtering (SQLi, Comment Spam, Author Scans)
   * **6.9** 8G Firewall v1.5 (Perishable Press Server-Level WAF)
   * **6.10** Rate Limiting (`mod_ratelimit`) & IP Access Control Examples
7. **[URL Canonicalization, HTTPS & Redirects](.htaccess#L1337)** — Force SSL, WWW vs Naked domain canonicalization, direct IP redirects, and staging robots.txt.
8. **[WordPress Front Controller](.htaccess#L1467)** — Standard WordPress rewrite rules (placed at the very end to ensure all security/optimization rules run first).

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
Open `.htaccess` in your editor and review optional toggles:
* **SSL / HTTPS**: If not enforcing SSL at Cloudflare/CDN level, uncomment the **Force SSL** redirect block in Section 7.
* **Domain Canonicalization**: Uncomment either **WWW to Naked** or **Naked to WWW** redirect depending on your domain preference.
* **Jetpack / WP Mobile App**: If using Jetpack or mobile publishing, uncomment the allowed Automattic IP ranges in the `xmlrpc.php` block in Section 6.5.

---

## ⚠️ Important Notes & Troubleshooting

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

## 📜 Credits & Attributions

This project builds upon security research, server configuration standards, and optimization techniques from the open-source community:

* **[HTML5 Boilerplate Server Configs](https://github.com/h5bp/server-configs-apache)** — Standards for MIME types, character encodings, and HTTP caching.
* **[Perishable Press (Jeff Starr)](https://perishablepress.com/)** — [8G Firewall v1.5](https://perishablepress.com/8g-firewall/), nG blacklist concepts, bot query mitigation, and custom error handling.
* **[WordPress Codex & Security Team](https://wordpress.org/documentation/article/hardening-wordpress/)** — Core `wp-includes` and security hardening guidelines.
* **[Sucuri Research](https://blog.sucuri.net/)** — Research on XML-RPC amplification attacks and WordPress vulnerability patterns.
* **[David Walsh](https://davidwalsh.name/)** — Cross-domain font sharing (CORS) and SVG serving best practices.
* **[Crunchify](https://crunchify.com/)** — Browser caching and ETag optimization.
* **[KeyCDN](https://www.keycdn.com/)** — Research on `Cache-Control: immutable` caching directives.
* **[HackRepair.com](https://hackrepair.com/)** — Bad bot and malicious user-agent blacklisting research.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Contributions, bug reports, and pull requests are always welcome!
