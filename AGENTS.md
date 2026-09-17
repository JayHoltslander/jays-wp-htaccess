# Agent Guidelines & Repository Directives

This document provides mandatory operational instructions for AI assistants (Antigravity, Claude Code, Cursor, Copilot, etc.) working within this repository.

---

## 🚨 MANDATORY VERSIONING PROTOCOL
Every single change or commit that modifies `.htaccess` **MUST** bump the version number and update the release date in the `.htaccess` header banner:

```apache
# Version:      X.Y.Z
# Released:     YYYY-MM-DD
```

### Versioning Rules:
- **Patch (`X.Y.Z+1`):** Small rule tweaks, regex fixes, documentation clarifications, or minor directive additions.
- **Minor (`X.Y+1.0`):** New security categories, new feature blocks, or significant rule enhancements.
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

## 🔒 Git & Security Protocols

1. **Commit Authorship:**
   - Ensure all commits are authored by the repository maintainer (`Jay Holtslander <j.holtslander@gmail.com>`).

2. **Explicit Push Authorization:**
   - Never execute `git push` autonomously. Always commit locally, present the changes to the user, and wait for the user's explicit `"push to git"` confirmation before pushing to remote.
