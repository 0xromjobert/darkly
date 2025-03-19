# hidden field manipulation : recover pwd
flag :

**1D4855F7337C0C14B6F44946872C4EB33853F40B2D54393FBE94F49F1E19BBB0**

## What Happened

if you go on recover password for login : there is submit button but no field form ; looks a bit weird. An inspection of the page shows that there is a form linked ot submit button with POST method but the type is `type=hidden` 

```tsx
<form action="#" method="POST">
	<input type="hidden" name="mail" value="webmaster@borntosec.com" maxlength="15">
	<input type="submit" name="Submit" value="Submit">
</form>
```

we can delete the type and put any email address to receive the flag

### **Breach Summary:**

- The form has an `input` field of `type="hidden"` for an email address.
- The user is **not supposed to change it**, but because it is in the client-side code, it can be easily manipulated via browser dev tools (right-click > Inspect > Edit HTML).
- After editing the hidden field (e.g., removing `type="hidden"` or modifying the `value` attribute), the attacker can submit **any arbitrary email** to the backend.

**Root cause:**

- Lack of server-side validation.
- The server does not verify that the provided email address is authorized or belongs to the user requesting the reset.

### **How to prevent this vulnerability?**

### **1. Never trust client-side data**

- Always assume that **all input from the client is untrusted** — whether visible or hidden.
- Always validate data **on the server side**.

### **2. Validate ownership server-side**

- When handling password recovery, **the server should verify**:
    - Is this email linked to an actual user in the system?
    - Does this email belong to the currently authenticated or verified user (if applicable)?

### **3. Avoid sending critical information based on user-supplied email**

- Instead of relying on a client-provided email, **use server-side user session information** to determine the user's email.

### **4. Remove hidden fields for critical data**

- **Avoid using hidden fields** for critical logic like user identity, roles, or permissions. These should be handled **entirely on the backend**