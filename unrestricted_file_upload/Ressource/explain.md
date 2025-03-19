# Unrestricted file upload
flag

46910d9ce35b385885a9f7e2b336249d622f29b267a1771fbacf52133beddba8

## What happened

we realize that the page [`http://10.12.250.125/?page=upload`](http://10.12.250.125/?page=upload) allow to upload a page. we can try with the frontend to add some funky types (like `file.xyz.wtf.jpg`) so we then try with curl to directly send a malicious POST request: a request with a script file instead of a jpg but hide the mime type as jpg.

we create a python script [`shell.py`](http://shell.py) that is simple (it prints “you have been hacked”) but it could be something more powerful.

then we send it via curl and realize the response is a flag 🙂

```tsx
curl -X POST -F 'Upload=Upload' -F 'uploaded=@shell.py;type=image/jpeg' "10.11.249.211/?page=upload#" | grep "flag”
```

`curl`

- A command-line tool to make HTTP requests (GET, POST, PUT, etc.).

---

`X POST`

- `X` specifies the HTTP method to use.
- `POST` is used, meaning you are sending data to the server (typically for form submissions or uploads).

`F 'Upload=Upload'`

- `F` stands for **form data**. It is used to simulate a form submission with `multipart/form-data` (like submitting a file via an HTML form).
- `'Upload=Upload'` sends a form field named `Upload` with the value `Upload`.

---

`F 'uploaded=@shell.py;type=image/jpeg'`

- Another form field named `uploaded`.
- `@shell.py` tells `curl` to upload a file named `shell.py` .
- `;type=image/jpeg` tricks the server into thinking the file is an image (MIME type spoofing). This is often used to bypass file upload restrictions that only accept images.

## **What is the Breach / OWASP Classification?**

This maps to:

- **OWASP A01:2021 - Broken Access Control**
    
    If anyone can upload without proper restrictions and gain elevated access (e.g., upload a web shell).
    
- **OWASP A05:2021 - Security Misconfiguration**
    
    If the upload folder is executable or the server improperly handles MIME types and file paths.
    
- **OWASP A08:2021 - Software and Data Integrity Failures**
    
    If uploaded files aren't validated for integrity or authenticity.
    

### **Common impact / risk**

- Remote Code Execution (RCE)
- Web server compromise
- Data exfiltration
- Defacement

## **How to avoid? Mitigation strategies**

1. **Restrict allowed file types**
    - Only allow safe file types (e.g., `.jpg`, `.png`, `.pdf`).
    - Use a **whitelist** approach, not a blacklist.
2. **Check MIME types on the server side**
    - Don’t trust the `Content-Type` header or form-data values (as in `type=image/jpeg`); check the real MIME type and file signature (magic bytes) on the backend.
3. **Check file content (deep inspection)**
    - Inspect file headers (e.g., JPEG header `0xFFD8`) to verify that the file matches its expected format.
4. **Rename uploaded files**
    - Rename files on upload to random names (e.g., `UUID.jpg`) to prevent execution by referencing original filenames like `shell.php`.