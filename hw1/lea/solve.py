from pwn import *
from math import sin

def ExtendedMao(s, A, B, C, D, E, F):
    def G(X, Y, Z):
        return (X ^ (~Z | ~Y) ^ Z) & 0xFFFFFFFF
    def M(X, Y):
        return (X << Y| X >> (32 - Y)) & 0xFFFFFFFF
    X = [int((0xFFFFFFFE) * sin(i)) & 0xFFFFFFFF for i in range(256)]
    s_size = len(s) + 128
    s += bytes([0x80])
    if len(s) % 128 > 120:
        while len(s) % 128 != 0: s += bytes(1)
    while len(s) % 128 < 120: s += bytes(1)
    s += bytes.fromhex(hex(s_size * 8)[2:].rjust(16, '0'))
    for i, b in enumerate(s):
        k, l = int(b), i & 0x1f
        A = (B + M(A + G(B,C,D) + X[k], l)) & 0xFFFFFFFF
        B = (C + M(B + G(C,D,E) + X[k], l)) & 0xFFFFFFFF
        C = (D + M(C + G(D,E,F) + X[k], l)) & 0xFFFFFFFF
        D = (E + M(D + G(E,F,A) + X[k], l)) & 0xFFFFFFFF
        E = (F + M(E + G(F,A,B) + X[k], l)) & 0xFFFFFFFF
        F = (A + M(F + G(A,B,C) + X[k], l)) & 0xFFFFFFFF
    return ''.join(map(lambda x : hex(x)[2:].rjust(8, '0'), [A, F, C, B, D, E]))

for i in range(20):
    passlength = i
    r = remote('edu-ctf.csie.org', 42073)
    r.sendlineafter(b'username: ', b'Admin')
    r.recvline()
    session = r.recvline()
    session = session.decode().split(': ')[1][:-1]
    mac = r.recvline()
    mac = mac.decode().split(': ')[1][:-1]

    A = int(mac[:8], 16)
    F = int(mac[8:16], 16)
    C = int(mac[16:24], 16)
    D = int(mac[24:32], 16)
    B = int(mac[32:40], 16)
    E = int(mac[40:], 16)
    MAC = ExtendedMao(b'&&flag', A, B, C, D, E, F)
    # print(MAC)
    def partofmao(s):
        s_size = len(s)
        print(s_size - 29)
        s += bytes([0x80])
        if len(s) % 128 > 120:
            while len(s) % 128 != 0: s += bytes(1)
        while len(s) % 128 < 120: s += bytes(1)
        s += bytes.fromhex(hex(s_size * 8)[2:].rjust(16, '0'))
        return s
    part_of_message = partofmao(b'&&'.join([b'Admin', b'a'*passlength, session.encode()]))
    part_of_message = part_of_message[9 + passlength:]
    p = MAC.encode() + b'&&' + part_of_message + b'&&flag'
    print(p)
    r.sendlineafter(b'do? ', p.hex().encode())
    q = r.recvline()
    print(q)
    r.close()
