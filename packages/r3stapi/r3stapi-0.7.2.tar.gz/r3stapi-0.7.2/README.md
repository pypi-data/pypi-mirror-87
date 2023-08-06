# r3stapi
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## Description
Easiliy create a subscription based RESTful webservice with django, firebase & stripe through r3stapi.

## Installation
	pip3 install r3stapi --upgrade

## Python Examples.

### Initializing the rest api.
Using the r3stapi.RestAPI object class.
```python

# import the package.
import r3stapi, fir3base

# initialize the firebase object (or pass the credentials to the rest api).
# 	(https://github.com/vandenberghinc/fir3base)
firebase = fir3base.Firebase("/path/to/firebase-credentials.json")

# initialize the restapi class.
restapi = r3stapi.RestAPI(
	# Pass either the firebase credentials or initialzed firebase object.
	# 	the firebase credentials.
	firebase_credentials=None,
	# 	the fir3base.FireBase object (optional).
	firebase=None,
	# Pass the stripe keys.
	# 	the stripe secret key.
	stripe_secret_key=None,
	# 	the stripe publishable key.
	stripe_publishable_key=None,)

```
### Configurating the rest api.
The users will be stored in firestore with the following structure:
```python
	users/
		$uid/
			api_key: null
			membership: $plan_id
			requests: 0
			timestamp: null
			... your additional data ...
```
Define your additional user data.
```python
restapi.__default_user_data__ = {
	"api_key":None,
	"membership":"free",
	"requests":0,
	"timestamp":None,
}
```
Define your plans.

	the "rate_limit" is total requests per "rate_reset"
	the "rate_reset" is the total days before rate limit reset.
	the "plan_id" is the price id from your stripe plan.

```python
restapi.__plans__ = {
	"developer": {
		"plan_id":None,
		"rate_limit":None,
		"rate_reset":None,
		"api_keys":[],
	},
	"free": {
		"plan_id":None,
		"rate_limit":3,
		"rate_reset":1, # in days.
		"api_keys":[],
	},
	"premium": {
		"plan_id":"price_I41.......",
		"rate_limit":10000,
		"rate_reset":30, # in days.
		"api_keys":[],
	},
	"pro": {
		"plan_id":"price_IPi.......",
		"rate_limit":25000,
		"rate_reset":30, # in days.
		"api_keys":[],
	},
}
```

### Post Sign Up
After a successfull sign up call this function.
```python
# save new user data.
response = restapi.__save_new_user__(uid)
```

### Functions.
Controlling the restapi object class.
```python

# identifying an api key.
response = restapi.identify_key(api_key=None)

# verifying an api key.
response = restapi.verify_key(api_key=None, plan=None)

# verifying the rate limit from an api key.
response = restapi.verify_rate_limit( 
	# required.
	api_key=None, 
	# optional to increase speed.
	# the uid from the api key.
	uid=None,
	# the plan from the api key.
	plan=None,
)

# get the api key from a user uid.
response = restapi.get_key_by_uid(uid)

# get the user uid from an api key .
response = restapi.get_uid_by_key(api_key)

# get the stripe subscriptions.
response = restapi.get_subscriptions()

# create a stripe subscription.
response = restapi.create_subscription(... coming soon ...)

# cancel a stripe subscription.
response = restapi.cancel_subscription( 
	# the user's uid.
	uid=None,
	# the plan name.
	plan=None,
	# the users plans (to increase speed) (optional)
	plans={},
	)

# synchronize the users.
# (Checks the: default user data, membership, api keys, subscriptions)
response = restapi.synchronize(silent=False)
```

### Daemons
#### SynchronizeUsers() daemon
Start the synchronize users daemon.

```python
# start the synchronize users daemon.
daemon = r3stapi.daemons.SynchronizeUsers(
	# pass the restapi object.
	restapi=restapi,
	# show the daemon logs.
	silent=False,
	# the synchronize interval in minutes (default: synchronizes once per 60 min).
	synchronize_interval=60,
	# the sleep interval in minutes (default: checks synchronize interval once per 15 min).
	sleep_interval=15,)
daemon.start()
```


### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}