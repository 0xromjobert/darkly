# What is the attack

So first : what are we targetting? `/etc/passwd`, i.e.: trying to access the `/etc/passwd` file. But what is it?

## Understanding /etc/passwd
The `/etc/passwd` file is a system file on Unix-like operating systems that contains user account information. It is readable by all users but writable only by the superuser (root). Historically, it stored passwords in an encrypted form, but for security reasons, modern systems use /etc/shadow for that purpose.

Format of `/etc/passwd`
Each line `in /etc/passwd` represents a user account and follows this structure:
`username`:`x`:`UID`:`GID`:`comment`:`home_directory`:`shell`
The fields are sparated by : and the interesting ones are:

* `username` – The account name (e.g., root, john).
* `x` – This used to store the encrypted password, but now it contains an x, meaning the password is stored elsewhere in `/etc/shadow`.

## How is it done
Since /etc/passwd is world-readable, attackers can read it to gather valid usernames on the system. This can help in:

1. Brute-force attacks: Using discovered usernames to try SSH or login attempts.
Privilege escalation: Identifying system accounts that might be misconfigured.

2. Path Traversal to Access /etc/passwd
Path traversal (or directory traversal) exploits vulnerabilities in file-handling mechanisms that allow an attacker to access files outside the intended directory structure.

so the concept is to traverse and iterate on `/..` until we reach a path with a `GET` request returning the `/etc/passwd` folder

example : `GET /download?file=../../../../etc/passwd` returning the file

## How we did it 

At first we tried on classic path, like `http://10.12.250.125/../../../etc/passwd` but it didn't work, probably becasue most web servers (e.g., Nginx, Apache) normalize and sanitize the URL path before processing it.

Then we noticed in sign in pages or othe rone the syntax `http://10.12.250.125/?page=` : The ?page= parameter is likely used by the web application in its backend code, which directly processes user input without proper sanitization.

so we tried on iterating for `http://10.12.250.125/?page=x` with `x=../../ {n} /etc/passwd/` until it yields a result or timeout 

# How to avoid 
* Sanitize user input: Disallow ../ sequences using validation checks.
* Use absolute paths: Instead of allowing dynamic file access, define safe file paths.
* Set proper file permissions: Ensure web applications do not have read access to sensitive files.