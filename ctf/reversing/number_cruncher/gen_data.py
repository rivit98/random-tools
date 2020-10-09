import random
import struct

LEN = 6
REORDERED = 1

if not REORDERED:
    with open("./d{}".format(LEN), "wb") as f:
        nums = random.sample(range(1, 20 + LEN), LEN)
        print(list(map(hex, nums)))
        a = [struct.pack("<I", n) for n in nums]
        f.write(struct.pack("<I", len(nums)))
        f.write(b''.join(a))

else:
    b = [1, 5, 3, 2, 4, 6]
    with open("./d{}_reordered1".format(LEN), "wb") as f:
        nums = b
        print(list(map(hex, nums)))
        a = [struct.pack("<I", n) for n in nums]
        f.write(struct.pack("<I", len(nums)))
        f.write(b''.join(a))
