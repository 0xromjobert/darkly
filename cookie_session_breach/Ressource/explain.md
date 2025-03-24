**Flag**

df2eb4ba34ed059a1e3e89ff4dfc13445f104a1a52295214def1c4fb1693a5c3

## What happened?

we go to the website cookie in the console and get :

| cookie     |            value                 |
| ---------- | -------------------------------- |
| I_am_admin | 68934a3e9455fa72420237eb05902327 |
|  |  |

that looks juicy

Then when we look at the hash and keeo trying different decrypt to extract a potential seed value : with md5 we found that `68934a3e9455fa72420237eb05902327 : false`

so we try the value `true` (to get i_am_admin → true) with md5 which is `b326b5062b2f0e69046810717534cb09`. This gives the alert message:

`Good job! Flag : df2eb4ba34ed059a1e3e89ff4dfc13445f104a1a52295214def1c4fb1693a5c3`

## What is the issue?

- The user can manipulate the cookie since it relies on a hash of predictable values like `"true"` or `"false"`.
- MD5 hashes are fast to brute-force, so it took only seconds to find that `"false"` → `68934a3e9455fa72420237eb05902327` and `"true"` → `b326b5062b2f0e69046810717534cb09`.
- The website trusts the **client-side input** (the cookie) without any **server-side verification**.

## **How to mitigate it?**

1. **Never trust client-side cookies for sensitive data like admin flags**
    - Do not store authorization or user role decisions (e.g., `is_admin`) in plain cookies or simple hashes.
    - Perform **role checks on the server-side**.
2. **Use secure session management**
    - Store sensitive information (e.g., `is_admin` or user role) in a **server-side session** or **JWT with proper signing**.
    - If using JWT, ensure:
        - It is **signed with HMAC or RSA/ECDSA** (e.g., HS256 or RS256).
        - Tokens are **short-lived** and have proper **audience and issuer claims**.
3. **Use strong cryptography**
    - Never use MD5 or SHA1. Instead, use **SHA-256, bcrypt, Argon2, or PBKDF2** for hashing where needed.
    - For token signing or data integrity, use **HMAC-SHA256** or **RSA/ECDSA signatures**.
4. **HTTP-only and Secure flags on cookies**
    - Set cookies as `HttpOnly` and `Secure` to reduce exposure via XSS and network sniffing.
5. **Integrity checks**
    - If you must store data client-side (e.g., in a JWT or cookie), always include a **server-validated signature or MAC** to prevent tampering.