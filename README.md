# jays-wp-htaccess / Improved Fork (2026)

> **Forked from** [JayHoltslander/jays-wp-htaccess](https://github.com/JayHoltslander/jays-wp-htaccess) / Original work by Jay Holtslander.

An improved and modernized `.htaccess` file for WordPress websites, updated in 2026 with enhanced security, modern file type support, and detailed beginner-friendly comments.

---

## What's new in this fork vs the original

| Feature | Original (2021) | This fork (2026) |
|---|---|---|
| Security headers | Basic | Permissions-Policy, Referrer-Policy, improved CSP |
| Image formats | WebP | + AVIF, HEIC, HEIF |
| WebAssembly | No | Yes |
| Comment quality | Short | Detailed - explains **why**, not just what |
| Duplicate declarations | Present | Fixed |
| HSTS preload guidance | Partial | Complete with registration link |
| Beginner-friendly | Partial | Every rule explained in plain English |

---

## Who is this for ?

- **Beginners and juniors** - every single rule has a comment explaining what it does and why it exists
- **WordPress developers** - covers all common WP security and performance needs
- **Anyone using Apache** - works on any Apache-based hosting (shared, VPS, dedicated)

---

## How to use

1. Download the `.htaccess` file
2. Make a **backup** of your current `.htaccess` first!
3. Replace your existing `.htaccess` at the root of your WordPress installation
4. Read the comments - most sections are **commented out by default**. Activate only what you need by removing the `#` characters.
5. Test your site after each change

---

## What's inside

- **Section 1** - WordPress core rewrite rules
- **Section 2** - HTTPS / SSL forcing + HSTS
- **Section 3** - URL canonicalization (www vs no-www)
- **Section 4** - Security headers (X-Frame-Options, CSP, Referrer-Policy, Permissions-Policy...)
- **Section 5** - WordPress-specific security (wp-config, xmlrpc, username enumeration...)
- **Section 6** - Compression (mod_deflate / gzip)
- **Section 7** - Browser caching (Expires headers)
- **Section 8** - MIME types (including AVIF, HEIC, WebAssembly, modern fonts)
- **Section 9** - Character encoding (UTF-8)
- **Section 10** - CORS headers
- **Section 11** - Force file downloads
- **Section 12** - Custom error pages
- **Section 13** - PHP settings
- **Section 14** - Legacy browser compatibility
- **Section 15** - 301 redirects

---

## Useful tools

| Tool | What it does |
|---|---|
| [securityheaders.com](https://securityheaders.com) | Test your security headers |
| [ssllabs.com](https://www.ssllabs.com/ssltest/) | Test your SSL certificate |
| [hstspreload.org](https://hstspreload.org) | Register for HSTS preload list |
| [htaccess.madewithlove.com](https://htaccess.madewithlove.com) | Debug your .htaccess rules |
| [webpagetest.org](https://www.webpagetest.org) | Test your site speed |

---

## License

MIT same as the original project. See [LICENSE](LICENSE).

---

*Improved by [madjeek-web](https://github.com/madjeek-web) / February 2026*
