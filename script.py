try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
except:
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64encode
import requests, time, lxml.html, json, sys, re
from saved_cookies import cookies
from saved_data import submit_shipping_body
from saved_data import submit_payment_body

def best_buy(link, data):
    session = requests.Session()

    print_separator = '_______________________________________________________________________'
    encrypted_card = "TQwTjt5EhrumAloHdxcjrrMe+XEAE+fWXvg7s/NSy0l/3SuVRzf9og9x/cNNRi19MOKFebbP/VXSfPV6OKgLRRBoy9rKV2mygN6DGI8sH4nOSoLFe6s7rOSnQW+VQKrWEuE9in4JeM6EJe17AgXfZSg+iMnKv2lUV5xLB3wS9NN0/iOQR/hky5JchhQj8bv4YXBIvv2xSYkHnfPhJAWlC+tV5EZaNAWnS8GCs851gjedHTP+GFFb4uwPVQr3Gc76FeFmQRovjLxVGGDHzfPtZ0XM1m7hBYJI9x3ay0DdVOalUg7pM8yyLtsHl6Z5paJqDVCEszZATEcr9lr02F1IHQ==:3:735818052:4767710000009527"
    
    
    cookie_buffer = []
    for cookie in cookies:
        cookie_buffer.append(cookie['name'] + "=" + cookie['value'])
    formatted_cookies = "; ".join(cookie_buffer)
    
    '''
    r_cookies = {}
    for cookie in cookies:
        r_cookies[cookie['name']] = cookie['value']
    '''
    link = "https://www.bestbuy.com/site/corsair-tm30-performance-thermal-paste/6318342.p?skuId=6318342"
    sku = "6318342"
    credit_card = ""
    
    atc_headers = {
        "authority": "www.bestbuy.com",
        "accept": "application/json",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://www.bestbuy.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "referer" : link, 
        "cookie": formatted_cookies
    }

    basket_headers = {
        'authority': 'www.bestbuy.com',
        'x-client-id': 'attach',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': link,
        'accept-language': 'en-US,en;q=0.9',
    }

    headers = {
        "authority": "www.bestbuy.com",
        "accept": "application/com.bestbuy.order+json",
        "x-user-interface": "DotCom-Optimized",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "content-type": "application/json",
        "origin": "https://www.bestbuy.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer" : "https://www.bestbuy.com/checkout/r/fulfillment", 
        "accept-language": "en-US,en;q=0.9",                                                                                
        "cookie": formatted_cookies
    }
    body = {'items': [{'skuId': sku}]}

    atc = session.post('https://www.bestbuy.com/cart/api/v1/addToCart', json=body, headers=atc_headers)
    #print(atc)
    #print(print_separator)

    basket = session.get('https://www.bestbuy.com/basket/v1/basket', headers=basket_headers)
    #print(basket)
    #print(print_separator)

    basket_dict = json.loads(basket.text)
    basket_id = basket_dict['id']
    line_id = basket_dict['basketItems'][0]['lineId']
    #print(f"basketId: {basket_id}")
    #print(f"lineId: {line_id}")

    body = {
        "items":[
            {
                "id":line_id,
                "type":"DEFAULT",
                "selectedFulfillment":{
                    "shipping":{
                    "address":{
                        "country":"US",
                        "saveToProfile":False,
                        "street2":"Unit 10",
                        "useAddressAsBilling":True,
                        "middleInitial":"",
                        "lastName":"Altov",
                        "street":"5757 Owensmouth Ave",
                        "city":"Woodland Hills",
                        "override":False,
                        "zipcode":"91302",
                        "state":"CA",
                        "firstName":"Vladimir",
                        "isWishListAddress":False,
                        "dayPhoneNumber":"8185858122",
                        "type":"RESIDENTIAL"
                    }
                    }
                },
                "giftMessageSelected":False
            }
        ],
        "phoneNumber":"8185858122",
        "smsNotifyNumber":"",
        "smsOptIn":False,
        "emailAddress":"masonabagnale@gmail.com"
    }
    ff_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        }
    fulfillment = session.get('https://www.bestbuy.com/checkout/r/fulfillment', headers=ff_headers)

    address = session.patch('https://www.bestbuy.com/checkout/orders/{}/'.format(basket_id), json=body, headers=headers)
    address_dict = json.loads(address.text)
    print(address.text)
    customer_order_id = address_dict['customerOrderId']
    payment_id = address_dict['payment']['id']
    #body = {"phoneNumber":"8185858122","smsNotifyNumber":"","smsOptIn":False,"emailAddress":"masonabagnale@gmail.com"}

    #address = session.patch('https://www.bestbuy.com/checkout/d/orders/{}/'.format(basket_id), json=body, headers=headers)

    headers = {
    'authority': 'www.bestbuy.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-context-id': customer_order_id,
    'x-client': 'CHECKOUT',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'content-type': 'application/json',
    'origin': 'https://www.bestbuy.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.bestbuy.com/checkout/r/payment',
    'accept-language': 'en-US,en;q=0.9',
    'cookie':formatted_cookies 
    }
    body = {
    "billingAddress":{
        "country":"US",
        "useAddressAsBilling":True,
        "middleInitial":"",
        "lastName":"",
        "isWishListAddress":False,
        "city":"",
        "state":"CA",
        "firstName":"",
        "addressLine1":"",
        "addressLine2":"",
        "dayPhone":"",
        "postalCode":"91367",
        "userOverridden":False
    },
    "creditCard":{
        "hasCID":False,
        "invalidCard":False,
        "isCustomerCard":False,
        "isNewCard":True,
        "isVisaCheckout":False,
        "govPurchaseCard":False,
        "number":encrypted_card,
        "binNumber":credit_card[:6],
        "isPWPRegistered":False,
        "expMonth":"08",
        "expYear":"2026",
        "cvv":"578",
        "orderId":customer_order_id,
        "saveToProfile":False,
        "type":"VISA",
        "international":False,
        "virtualCard":False
    }
    }
    credit = session.put('https://www.bestbuy.com/payment/api/v1/payment/{}/creditCard'.format(payment_id), json=body, headers=headers)
