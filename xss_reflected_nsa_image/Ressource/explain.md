# Reflective xss attack

flag:

**928D819FC19405AE09921A2B71227BD9ABA106F9D2D37AC412E9E5A750F1506D**

# What happened?

on the home page we notice a funky image : an NSA eagle with some headphones. it is the only clickable image of the page as well, with an href ,  so we click on it and arrive on the image page.

`http://10.12.250.125/?page=media&src=nsa`

### Observation:

- The URL contains a `src=` parameter.
- This suggests that **the `src` value is reflected or used to generate content** on the page.
- This doesn't immediately look like an input field exploitable by traditional SQL injection, but it **appears injctable for other types of attacks** (such as XSS).

### First attempts:

- I started by testing a basic reflected XSS payload:
    
    ```html
    <script>alert('xss')</script>
    ```
    
- However, this initially resulted in a **404 or broken page**, suggesting the application might be trying to fetch a file/resource with `src=nsa`.

### Idea

- I realized that the `src` parameter might not expect a typical URL or string but could **accept a `data:` URI scheme**, which allows browsers to load content directly from inline data.

### Successful payload:

I encoded the payload `<script>alert('xss hack')</script>` into Base64:

```
PHNjcmlwdD5hbGVydCgneHNzIGhhY2snKTwvc2NyaXB0Pg==

```

I then crafted this **data URI**:

```
data:text/html;base64,PHNjcmlwdD5hbGVydCgneHNzIGhhY2snKTwvc2NyaXB0Pg==

```

### Final injected URL:

```
http://10.12.250.125/?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgneHNzIGhhY2snKTwvc2NyaXB0Pg==

```

### Result:

- The payload triggered an **XSS popup (alert box)**.
- The page **executed the `<script>` tag inside the injected Base64-encoded HTML**, which led to revealing the flag.

### Why did `text/html` work?

- **The browser sees `data:text/html;base64,...`** as a valid **HTML document**, and it automatically parses it as if you had loaded a normal webpage.
- Since the payload is wrapped inside a valid `text/html` document type and decoded into HTML by the browser, the `<script>` tag runs as soon as the page loads.

**Other MIME types like `image/png` or `text/plain` would not execute scripts**, but `text/html` triggers HTML rendering.

## How to prevent this issue?

### 1. **Validate and sanitize input server-side**

- Block dangerous inputs like `data:` schemes or any non-whitelisted URLs.
- Apply a strict **input allowlist**, accepting only known and safe resource URLs.

### 2. **Enforce proper CSP (Content Security Policy)**

- Example CSP header:
    
    ```
   Content-Security-Policy: default-src 'self'; object-src 'none'; script-src 'self'
    
    ```
    
- This would **block execution of inline `data:`based scripts**.