flag is : 

**03A944B434D5BAFF05F46C4BEDE5792551A2595574BCAFC9A6E25F67C382CCAA**

## What happened?

when we arrive on the page [`http://{ip}/?page=survey`](http://10.12.250.125/?page=survey)

we realize we have an input field in the survey : not a direct input that could be tested with SQL injection, but a list field.

when looking at the code in the console we have:

```tsx
				<form action="#" method="post">
					<input type="hidden" name="sujet" value="2">
					<SELECT name="valeur" onChange='javascript:this.form.submit();'>
						<option value="1">1</option>
						<option value="2">2</option>
						<option value="3">3</option>
						<option value="4">4</option>
						<option value="5">5</option>
						<option value="6">6</option>
						<option value="7">7</option>
						<option value="8">8</option>
						<option value="9">9</option>
						<option value="10">10</option>
					</SELECT>
				</form>
```

so we realize on change the value is submitted : we can try to change one of the value (for instance changing the value for index 8 to something else like 888888).

this will return the flag

## What is the breach?

1. **Hidden or poorly validated parameters**:
    
    The `<select>` element has values from `1` to `10`, and the form automatically submits when a user changes the selection.
    
2. **Client-side trust issue**:
    
    The server expects values between `1` and `10`, but nothing prevents a user from changing the HTML or using browser developer tools (as you did) to send a value like `888888`.
    
3. **Server-side logic flaw**:
    
    If submitting `888888` reveals a flag (or some privileged resource), it means the backend does **not** properly validate whether the submitted `valeur` falls within an expected, valid range (`1` to `10`).
    

in OWASP this is **OWASP Top 10 - Broken Access Control**

### Why this happens:

- The backend **trusts** the client-side form without sufficient validation.
- Attackers can **manipulate form inputs** (even hidden fields or select values) using browser dev tools or tools like Burp Suite.

## How to avoid

- Implement strict **server-side input validation** (never trust client-side controls like dropdowns or hidden fields).
- Enforce **access control checks** before returning sensitive data.
- Avoid relying solely on UI controls for limiting user actions.