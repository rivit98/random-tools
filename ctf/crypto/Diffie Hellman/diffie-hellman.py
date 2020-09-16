from binascii import unhexlify

# https://www.alpertron.com.ar/DILOG.HTM

p = 0x8c5378994ef1b
g = 0x2
A = 0x269beb3b0e968
B = 0x4757336da6f70

# A = g^a % p

for k in range(1):
    a = 310100388912 + (822880711932510 * k)
    b = 77456265670244 + (822880711932510 * k)

    if A == pow(g, a, p) and B == pow(g, b, p):
        print("CTFlearn{{{}_{}}}".format(unhexlify(hex(a)[2:]).decode(), unhexlify(hex(b)[2:]).decode()))
        # print("CTFlearn{{{}_{}}}".format(a, b))
    else:
        print("nope")


