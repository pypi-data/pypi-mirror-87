# Fir3base
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install fir3base

## Python Examples.

### The Firebase() object class.
The Firebase() object class.  
```python

# import the package.
from fir3base import Firebase

# initialize firebase.
firebase = Firebase(key="/path/to/credentials.json")

```

#### The FireStore() object class.
The FireStore() object class.  
```python

# loading documents.
response = firebase.firestore.load("my-collection/my-document")
if response["success"]:
	print(response["document"])

# saving documents.
response = firebase.firestore.save("my-collection/my-document", {
	"Hello":"World"
})

# deleting documents.
response = firebase.firestore.delete("my-collection/my-document")

# list the documents of a collectoin.
response = firebase.firestore.list("my-collection/")

```

#### The Users() object class.
The Users() object class.  
```python


# loading firestore data by user.
response = firebase.users.load_data(uid)

# saving firestore data by user.
response = firebase.users.save_data(uid, {})

# get a user.
response = firebase.user.get(
	# define one of the following parameters.
	uid=None,
	email="some@email.com",
	phone_number=None,
)

# create a user.
response = firebase.users.create(
	# required:
	email=None,
	password=None,
	verify_password=None,
	# optionals:
	name=None,
	phone_number=None,
	photo_url=None,
)

# update a user.
response = firebase.users.update(
	# required:
	uid=None,
	# optionals:
	name=None,
	email=None,
	password=None,
	phone_number=None,
	photo_url=None,
	email_verified=None,
)

# delete a user.
response = firebase.users.delete(
	# the user's uid.
	uid=None,
)
# iterate the users.
for user in firebase.users.iterate():
	print(user.uid)

# verify a javascript firebase user id token.
response = firebase.users.verify_id_token(id_token)


# configure email.
firebase.users.email_address = "your-email@gmail.com"
firebase.users.email_password = "your-password"
firebase.users.smtp_host = "smtp.gmail.com"
firebase.users.smtp_port = 587

# send a verification code.
response = firebase.users.send_code(
	# define uid or email to retrieve user.
	uid=None, 
	email=None, 
	# the clients ip.
	ip="unknown",
	# the mode id.
	mode="verification",
	# the mode title.
	title="Account Activation",
	# the html (str).
	html="",
	# optionally specify the code (leave None to generate).
	code=None,)

# verify a code.
response = firebase.users.verify_code(
	# define uid or email to retrieve user.
	uid=None, 
	email=None, 
	# the user entered code.
	code=000000, 
	# the message mode.
	mode="verification",)


```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}