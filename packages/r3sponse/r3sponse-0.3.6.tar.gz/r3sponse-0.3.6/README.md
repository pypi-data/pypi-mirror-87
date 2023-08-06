# Example
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install example

## CLI:
	Usage: example <mode> <options> 
	Modes:
	    -h / --help : Show the documentation.
	Options:
	Author: Daan van den Bergh 
	Copyright: © Daan van den Bergh 2020. All rights reserved.

## Python Examples.

Initialize the encryption class (Leave the passphrase None if you require no passphrase).
```python
# import the package
from r3sponse import r3sponse

# universal responses.
def my_function():

	# return an error response from a function.
	return r3sponse.error_response("Failed to retrieve your personal API key")

	# return a success response from a function.
	return r3sponse.success_response("Success retrieved your personal API key", {
		"api_key":api_key,
	})

# check if a response was successfull.
response = my_function()
if r3sponse.success(response):
	message = response["message"]
else:
	error = response["error"]
```


