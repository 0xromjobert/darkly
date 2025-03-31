# Malicious redirections

flag:

**b9e775a0291fed784a2d9680fcfad7edd6b8cdf87648da647aaf4bba288bcab3**

# What happened?

on the bottom of the page we notice three icons, one for each social network. These are supposed to be clicked and redirect you to the corresponding web page.
inspecting the DOM we can see the vulnerability

### Observation:

- The icon element has an href `index.php?page=redirect?site=....` .
- This suggests this icon leads to a redirection script that takes you to the website that the variable after `site` points to.

### Breach:

- You just simply change the variable result for anything else and we get the flag!
    

### Why is this bad?

- A malicious user can change that variable to point to a fake clone of that social network, where you can be asked for sensitive data. This is called `phishing`


## How to prevent this issue?

### 1. **Validate redirection in ibackend.*

- Whitelist valid URLS in the backend logic, thus protecting the final user from phishing attacks.
