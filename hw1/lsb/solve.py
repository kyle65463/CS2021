from pwn import *
from Crypto.Util.number import *

r = remote('edu-ctf.csie.org', 42071)
q = r.recvline()
n = int(q[4:])
q = r.recvline()
c = int(q[4:])
e = 65537

a = inverse(3, n)
m = 0
b = 0
i = 0
f = 0

while True:
    r.sendline(str(pow(a, i * e, n) * c % n).encode())
    q = r.recvline()
    mm = (int(q.split()[-1]) - (a * b) % n) % 3
    if mm == 0:
        f += 1
        if f == 10:
            break
    else:
        f = 0
    b = (a * b + mm) % n
    m = 3 ** i * mm + m
    i += 1

print(m)
print(long_to_bytes(m))