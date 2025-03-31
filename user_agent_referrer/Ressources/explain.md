# Authentication based on user-agent and referrer

flag:

**f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188**

# What happened?

visiting page `http://192.168.1.150/?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758`, or the page that has a link
at the very bottom of the main page (as the variable after page can change), inspecting the DOM there is some cryptic stuff going on:

<!--
You must come from : "https://www.nsa.gov/".
-->

<!--
Let's use this browser : "ft_bornToSec". It will help you a lot.
-->

### Observation:

- We can assume this instructions are referring to: 

    `You must come from` -> Referrer (url where the request was initiated, origin of the traffic).
    `Let's use this browser` -> User-Agent (identifies the application, browser, client that is making the request)

- This lead us to try this simple curl command:

    `curl -e https://www.nsa.gov/ -A ft_bornToSec "http://192.168.1.150/?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f" | grep flag`

    curl (Client of Url) is this lightweight but powerful command tool that enables us to transfer data using different network protocols. TLDR;
    it enables us to send http requests and customize the headers as we see fit.

    That's what we're doing here:

        -e   Referrer header
        -A   User-Agent header
        the url of the resource (page) we want to access

    and we pipe a grep flag, to catch the flag if we have detected a vulnerability....

### Breach:

- We did catch a flag and this a breach.

### Why is this bad?

- It's a horrible a idea to show sensitive information just based on the Referrer, User-Agent headers, and really in any http header, which as you can see, 
it only takes a simple curl command to send.


## How to prevent this issue?

### 1. **Authentication*

- Just hide sensitive information behind a properly secured login-authentication wall. Easy but secure.
