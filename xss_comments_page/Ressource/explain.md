## What Happened?

On the page `http://{IP}/index.php?page=feedback`by going on the comment page we see another input field for potential breach

- we try SQL injection and it doesn’t work
- We then try the second most famous breach, XSS

we try to insert some scripts (within <> and without) in the fields and it returns the flag. at some point writing `script` in the name field breaks it.

## How to prevent?

- **Escape all user-generated output**
    - Result: Prevents injected HTML or JavaScript from being interpreted by the browser.
    - Example: Use `{{ escape(user_input) }}` in templates instead of `{{ user_input }}`.
- **Sanitize input if allowing limited HTML**
    - Result: Removes unsafe tags like `<script>`, `<iframe>`, while allowing safe formatting tags like `<b>`, `<i>`.
    - Tool: Use libraries like DOMPurify (JavaScript) or sanitize-html (Node.js).
- **Validate and restrict input formats**
    - Result: Reduces attack surface by accepting only expected input formats (e.g., allow only letters/numbers in usernames).
    - Example: Validate comments to allow only text, no raw HTML or JavaScript.
- **Implement Content Security Policy (CSP) headers**
    - Result: Limits the sources from which scripts, styles, and other resources can be loaded, preventing inline scripts and untrusted domains from executing code.
    - Example: `Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com`.
- **Set HttpOnly flag on session cookies**
    - Result: Protects session cookies from being read via `document.cookie` by malicious scripts.
    - Example: `Set-Cookie: sessionid=abc123; HttpOnly; Secure; SameSite=Strict`.
- **Use frameworks with built-in XSS protections**
    - Result: Many modern frameworks automatically escape user input in templates, reducing XSS risks.
    - Example: React, Vue, Angular, Django templates automatically escape output by default.