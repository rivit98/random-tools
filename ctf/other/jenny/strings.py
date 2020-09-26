import struct

data = [
    0x021f1e440a1d0a01,  # local_d8
    0xe05050a08384407,  # local_d0
    0x12291f130e056b19,  # local_c8
    0x196b0809086b0e1f,  # local_c0
    0x46070e0a0f050102,  # local_b8
    0x121b04286b53595a,  # local_b0
    0x436b0537184e4b51,  # local_a8
    0xa07440a1d0a0127,  # local_a0
    0x502191f38440c05,  # local_98
    0x180e126b3d42500c,  # local_90
    0x1f130e056b184e6b,  # local_88
    0x2576b04056b2b6b,  # local_80
    0x2a272d6b551f0205,  # local_78
    0x42436b2942436b2c,  # local_70
    0xa07440a1d0a0127,  # local_68
    0x502191f38440c05,  # local_60
    0xa1d0a01276b500c,  # local_58
    0x1f38440c050a0744,  # local_50
    0x38236b500c050219,  # local_48
    0x542e363a21314404,  # local_40
    0x115c363d00124c38,  # local_38
    0x6b0b4d293d0  # local_30
]


te = [
    0x12291f130e056b19,  # local_c8
    0x196b0809086b0e1f,  # local_c0
    0x46070e0a0f050102,  # local_b8
]


def convert_strings(nums):
    b = []
    for n in nums:
        b.extend(n.to_bytes(8, "little"))

    # print(b)
    # print(b)
    # print(hex(len(b)))

    res = []
    for i in range(len(b)):
        c = b[i]
        c ^= 0x6b
        res.append(chr(c))
        if c == 0:
            res.append("\n")

    print(''.join(res))


def get_break_offset(base):
    # print(hex(base + (-0x7f5bec178850 + 0x7f5bec179094)))
    print(hex(base + (-0x7f5bec178850 + 0x7f5bec179094)))

# convert_strings(te)
# convert_strings(data)

get_break_offset(0x7f9c3c0ae550)

