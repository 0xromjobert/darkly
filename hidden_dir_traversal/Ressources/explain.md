# Hidden Directory Traversal Attack

This was a fun one ! When connecting to the URL:
```
http://{ipdarkly}/.hidden
```
we find a directory containing multiple subdirectories and a `README` file. Each subdirectory contains additional nested directories with similar `README` files, forming a deeply nested structure.

Example directory listing:
```shell
../
amcbevgondgcrloowluziypjdh/       29-Jun-2021 18:15 
bnqupesbgvhbcwqhcuynjolwkm/       29-Jun-2021 18:15   
[... more links ...]
zzfzjvjsupgzinctxeqtzzdzll/       29-Jun-2021 18:15    
README                            29-Jun-2021 18:15   34
```
- Clicking on `README` files reveals messages such as:
  - "Demande à ton voisin de gauche"
  - "Non ce n'est toujours pas bon..."
  - Various misleading hints.



## Automated Directory Traversal Script
Manually browsing **18,650+ links** is impractical. Instead, we automate the traversal using Python.

### **Approach**

Btw, the script code is documented anyway but here is the logic:

1. **Fetch Initial Links**  
   - Start at `http://{ipdarkly}/.hidden/`
   - Extract all links pointing to subdirectories.
   
2. **Recursive Traversal**
   - For each directory, request its content.
   - If it contains:
     - **More directories** → Add them to the queue for further traversal.
     - **A `README` file** → Store and analyze its contents.
   - If a **flag** is detected in any file, **terminate immediately**.

3. **Analyzing Message Distribution**
   - If no flag is found, iterate over all **visited links** and analyze the frequency of messages.
   - This helps identify patterns or hints we may have overlooked.


## Security Implications & Prevention

### 1. Why Is This a Security Risk?
- **Exposure of hidden directories**: Directory listing should **never** be enabled on sensitive paths.
- **Unrestricted access to deep file structures**: Attackers can automate traversal to find sensitive data.
- **Potential for information disclosure**: If a developer accidentally leaves behind secret files, they could be extracted.

### 2. How to Prevent It
1. **Disable Directory Listing**  
   - On Nginx:
     ```nginx
     location / {
         autoindex off;
     }
     ```
   - This ensures that users **cannot see the list of files** inside directories.

2. **Restrict Access to Hidden Directories**  
   - Use **`.htaccess` rules** (Apache) or **server-side filtering** (Nginx) to **deny access** to hidden paths:
   - In Nginx:
     ```nginx
     location ~ /\.hidden {
         deny all;
     }
     ```

3. **Use Authentication & Authorization**
   - Ensure that **only authorized users** can access certain paths.
   - For example, add **Basic Authentication**
   - This prevents **unauthorized access** even if directory listing is enabled.

4. **Prevent Arbitrary File Access**
   - Avoid exposing filenames that could **reveal hints**.
   - Ensure **web applications do not allow arbitrary file inclusion** via user input.
