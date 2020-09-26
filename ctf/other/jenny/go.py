from z3 import  *
import ctypes

expected_values = [0x2f6f5348, 0x5d514a5a, 0x27533f45, 0x5d566b79, 0x56657a37, 0x00602642]
expected_values = list(map(lambda x: x ^ 0xcafebabe, expected_values))

def add_condition(s, v, current_index):
    s.add(((v << 5) | LShR(v, 0x1b)) == expected_values[current_index])

def uint32_to_int32(i):
    if i > 2147483647:
        return ctypes.c_int32(i).value
    else:
        return i

def main():
    lines = []

    for i in range(120, 180):
        s = Solver()

        xor_value = BitVecVal(i, 32)
        v = [BitVec("x{}".format(n + 1), 32) for n in range(6)]

        for n in reversed(range(6)):

            if n != 0:
                v[n-1] -= v[n]
                v[n] ^= xor_value

            add_condition(s, v[n], n)

        if s.check() == sat:
            mdl = s.model()

            res = []
            for d in mdl.decls():
                res.append("{} = {}".format(d, mdl[d]))

            res.sort()
            # asdf = "{} {}".format(i, '@'.join([str(int(va.split(" = ")[1]))  for va in res]))
            asdf = "{} {}".format(i, '@'.join([str(uint32_to_int32(int(va.split(" = ")[1])))  for va in res]))
            print(asdf)
            lines.append(asdf)

            # s.add(Or(v[0] != s.model()[v[0]], b != s.model()[b]))

    return lines

if __name__ == "__main__":
    lines = main()

    # format_template = "python -c 'print(\"520\\n{}\\n\")' | java Jenny"
    format_template = "python3 -c 'print(str({}))'; python3 -c 'print(\"520\\n{}\\n\")' | /usr/lib/jvm/java-1.8.0-openjdk-amd64/bin/java Jenny; python3 -c 'print(\"-\" * 40)'"

    cmds = []
    for line in lines:
        line = line.strip()

        a, b = line.split(" ")
        a = int(a)
        if a > 127:
            a -= 256

        line = str(a) + " " + b

        cmds.append(format_template.format(a, line))

    with open("D:\\ctf\\cmds.sh", "w", newline="\n") as f:
        f.write('\n'.join(cmds))