# Brute force login form

flag:

**b3a6e43ddf8b4bbb4125e5e7d23040433827759d4de1c04ea63907479a80a6b2**

# What happened?

we have a canonical login form in the sign in section of the page, and we're gonna assume that the owners are lazy and careless and a valid username is 'admin'

### Observation:

- If we have guessed the username, we only need to guess the password.
- If the password is also weak, predictible, common... this is gonna be easy.

### Breach:

- We use a parallel password cracker called hydra, and it just takes seconds to guess the password is `shadow`!
- This is the command we use:

    hydra -l admin -P 10-million-password-list-top-10000.txt -F -o hydra.log 192.168.1.150 http-get-form '/index.php:page=signin&username=^USER^&password=^PASS^&Login=Login:F=images/WrongAnswer.gif'

-l is the username we are using for the attack
-P is the path to the file of a dictionary of passwords... this are free and available for everyone to use, it's a list of really horrible and weak passwords
-F this makes hydra end the session after the first success
-o just where to save the log

after that we specify the ip address of the victim and finally specify we are attacking a HTTP get form (the login form is a get, very bad also) and three different sections (separated by colons)
    - page (index.php)
    - variables
    - fail pattern, so hydra know it has failed and must continue

### Why is this bad?

- It's more than obvius, having predictible usernames and weak or common passwords can lead to malicious users gain access into an authenticated
system, and furthermore, in this case gaining access as an admin user, having possibly catastrofic consequences.


## How to prevent this issue?

### 1. **Strong passwords, password manager**

    -Keepass is your friend. Generate strong passwords, long and meaningless. Keep them in a password manager, better locally, so
    you avoid other possible breaches. (LastPass was famously breached in 2022)

### 2. Be strict with repeated http requests**

    -Hydra has had to request maybe hundreds and hundreds of requests in a few seconds. This is highly suspicious and we could implement 
    some kind of security policy in which we block an IP from further requests if they behave this way.
