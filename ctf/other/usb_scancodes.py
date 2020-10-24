import sys
from string import ascii_lowercase, ascii_uppercase

decode_table = {
    0x04: "A",
    0x05: "B",
    0x06: "C",
    0x07: "D",
    0x08: "E",
    0x09: "F",
    0x0A: "G",
    0x0B: "H",
    0x0C: "I",
    0x0D: "J",
    0x0E: "K",
    0x0F: "L",
    0x10: "M",
    0x11: "N",
    0x12: "O",
    0x13: "P",
    0x14: "Q",
    0x15: "R",
    0x16: "S",
    0x17: "T",
    0x18: "U",
    0x19: "V",
    0x1A: "W",
    0x1B: "X",
    0x1C: "Z",
    0x1D: "Y",
    0x1E: "!1",
    0x1F: "@2",
    0x20: "#3",
    0x21: "$4",
    0x22: "%5",
    0x23: "^6",
    0x24: "7\\",
    0x25: "*8",
    0x26: "(9",
    0x27: ")0",
    0x28: "\n",
    0x2B: "\t",
    0x2C: " ",
    0x2D: "_-",
    0x2E: "+=",
    0x2F: "{[",
    0x30: "}]",
    0x31: "|\\",
    0x33: ":;",
    0x34: "\",",
    0x35: "~`",
    0x36: "<,",
    0x37: ".:",
    0x38: "?/",
}

SHIFT = 0x02


def decode_scancodes(scancodes):
    out = []
    for s in scancodes:
        flags = s[1]
        code = s[0]

        k = ''
        data = decode_table.get(code, 'Unknown')
        # print(hex(code), data)

        if 0 < len(data) < 3:
            if flags == SHIFT:
                if len(data) == 1:
                    k = data[0]
                else:
                    k = data[1]
            else:
                k = data[0]
                if k in ascii_uppercase:
                    k = k.lower()

        out.append(k)

    print(''.join(out))


def main(fname):
    with open(fname, "rb") as f:
        data = f.read()

    scancodes = [data[i * 2:i * 2 + 2] for i in range(len(data) // 2)]

    print(f"{len(scancodes)} scancodes")

    decode_scancodes(scancodes)


if __name__ == '__main__':
    main(sys.argv[1])
