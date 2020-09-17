try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
except:
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64encode
import requests,time,lxml.html,json,sys
from saved_cookies import cookies
from saved_data import submit_shipping_body
from saved_data import submit_payment_body

def my_module():
    link = "https://www.bestbuy.com/site/corsair-tm30-performance-thermal-paste/6318342.p?skuId=6318342"
    headers={
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "content-type": "application/json",
            "referer": "https://www.bestbuy.com/checkout/r/payment",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"
    }
    r = requests.get("https://www.bestbuy.com/api/csiservice/v2/key/tas", headers=headers)
    tas = json.loads(r.text)                                                                                            
    card_number = submit_payment_body["creditCard"]["number"]
    
    key = RSA.importKey(tas["publicKey"])
    cipher = PKCS1_OAEP.new(key)
    encrypted_card = b64encode(cipher.encrypt(("00926999"+card_number).encode("utf-8"))).decode("utf-8")
    zero_string = ""
    for i in range(len(card_number)-10):
        zero_string+="0"
    bin_number = card_number[:6]
    encrypted_card +=":3:"+tas["keyId"]+":"+bin_number+zero_string+card_number[-4:]
    print("Encrypted card: {}".format(encrypted_card))
    
    
    cookie_buffer = []
    for cookie in cookies:
        cookie_buffer.append(cookie['name'] + "=" + cookie['value'])
    formatted_cookies = "; ".join(cookie_buffer)
    print("Cookies: {}".format(formatted_cookies))
