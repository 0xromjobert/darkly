# Breach : Sensitive Data Exposure hidden file robots.txt h

**the flag is :**

**d19b4823e0d5600ceed56d5e896ef328d7a2b9e7ac7e80f4fcdb9b10bcb3e7ff**

How did we do it ?
`robots.txt` is a **text file** that tells web crawlers (like Googlebot) which pages **should not** be indexed or accessed.

- It is **not a security mechanism** but rather a guideline for search engines.
- It is publicly accessible at:

```tsx
https://example.com/robots.txt
```

doing it on our vm for ip 10.12.250.125 yields for robots.txt

```
User-agent: *
Disallow: /whatever
Disallow: /.hidden
```

so we tried /.hidden and found nothing, but for /whatever it gets juicy :


we donwload it and get a user:password kind of kv pair. 

```tsx
root:437394baff5aa33daa618be47b75cb49
```

we just then google the password to try to find what the hash correspond to and we get

from [https://md5.gromweb.com/?string=qwerty123@](https://md5.gromweb.com/?string=qwerty123@)

**MD5 hash for « qwerty123@ »**

so we try it for the sign in page → doesn’t work 

then find a forum of very nice security tester (with plenty of good intention) recommending to try the classic address

```tsx
https://example.com/admin
```

and then we input root:qwerty123@

and we get the flag :) 

# how to avoid ?

### **Never Store Sensitive Data in `robots.txt`**

- `robots.txt` is **publicly accessible** and should **never** contain links to sensitive files.
- Attackers actively scan `robots.txt` to find hidden paths.