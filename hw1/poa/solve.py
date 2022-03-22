from pwn import *

r = remote('edu-ctf.csie.org', 42070)
q = r.recvline()
cipher = bytes.fromhex(q.split(b' ')[-1][:-1].decode())

def xor(a, b):
    return bytes(i^j for i,j in zip(a,b))

for block in range(2):
    ok = b''
    for i in range(16):
        for j in range(256):
            c = b'\x00'*(15-i)+bytes([j^0x80])
            if i == 15:
                c = b'\x00' * 16 + c
            c += ok
            c += cipher[16 * block + 16: 16 * block + 32]
            p = c.hex().encode()
            r.sendlineafter(b'cipher = ', p)
            q = r.recvline()
            if q != b'NOOOOOOOOO\n':
                ok = bytes([j]) + ok
                print(xor(cipher[:16*block+16][-i-1:], ok))
                break

r.interactive()