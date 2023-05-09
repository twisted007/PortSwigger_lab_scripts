#!/bin/python3

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={"http":"http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


# TODO: #1
# Make a GET request to /login2 passing in the name of the user.
# This will trigger the 2FA email and create a valid PIN.




# TODO: #2
# Loop around the potential pin space, 0001-9999. Make sure to format the numbers correctly.
