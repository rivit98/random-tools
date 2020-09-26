from copy import copy
from typing import List

reverse_dict = {}
reverse_functions_cnt = 0

TEST_STRING = "TEST_STRING_123_asdfqwerty{}32132321"
k = len(TEST_STRING)
TEST_DATA = [ord(i) for i in TEST_STRING]

def get_test_data():
    return copy(TEST_DATA)

def skip_comments(lines_orig):
    lines = []
    cnt = 0
    for l in lines_orig:
        if "def " in l:
            cnt += 1

        if not l.startswith("    #") and not l.startswith("#"):
            lines.append(l)

    print("Found {} functions in total".format(cnt))
    return lines

def parse_functions(lines):
    python_functions = []
    func_buffer = []
    function_started = False
    for line in lines:
        if "def " in line:
            if function_started:
                python_functions.append(copy(func_buffer))
                func_buffer.clear()

            function_started = True

        if not function_started:
            continue

        if "flag =" in line:
            break

        if function_started:
            func_buffer.append(line)

    python_functions.append(copy(func_buffer))

    return python_functions

def build_dict(python_functions):
    function_types = set()
    for f in python_functions:
        function_types.add(f[0][4:].split("_")[0])

    for ftype in function_types:
        reverse_dict[ftype] = globals()["{}_rev".format(ftype)]

    # print("{} function types".format(len(function_types)))

def reverse_functions():
    with open("D:\\mucho_encrypto.py", "rt") as f:
        lines_orig = f.read().splitlines()

    lines = skip_comments(lines_orig)
    python_functions = parse_functions(lines)
    build_dict(python_functions)

    flag_functions = copy(lines)
    for item in python_functions:
        for i2 in item:
            flag_functions.remove(i2)

    final_lines = []
    for func in python_functions:
        ftype = func[0][4:].split("_")[0]

        reversed_function_data = reverse_dict[ftype](copy(func))

        if reversed_function_data:
            good = test_function(func, reversed_function_data)
            if good:
                final_lines.extend(reversed_function_data)
            else:
                print(func)
                print(reversed_function_data)

                raise Exception("Test failed")

    print("Reversed {}/{} ({}%) functions".format(
        reverse_functions_cnt,
        len(python_functions),
        100 * (reverse_functions_cnt / len(python_functions))
    ))
    print("Remember to:")
    print("- fix loading data from file")
    print("- put k at the top of the file")
    print("- update k after loading ints from file")
    print("- print the flag")

    final_lines.extend(flag_functions[::-1])

    with open("D:\\mucho_encrypto_rev.py", "wt") as f:
        f.write('\n'.join(final_lines))


def get_func_name(func_line: str):
    func_line = func_line.strip()[4:]
    return func_line[:func_line.index('(')]


def eval_func(lines, data_to_eval=None):
    if data_to_eval is None:
        data_to_eval = get_test_data()

    scope = {'k': k}
    exec('\n'.join(lines), scope)
    f = scope[get_func_name(lines[0])]
    enc = f(data_to_eval)
    return enc

def test_function(lines_orig, lines_modified):
    enc = eval_func(lines_orig)
    dec = eval_func(lines_modified, enc)
    res = dec == TEST_DATA
    if not res:
        return False

    global reverse_functions_cnt
    reverse_functions_cnt += 1
    return True


# REVERSED FUNCTIONS

def cxor_rev(lines: List[str]):
    return lines


def chxor_rev(lines: List[str]):
    return lines


def mul_rev(lines: List[str]):
    lines[2] = lines[2].replace("*", "//")
    return lines


def sub_rev(lines: List[str]):
    lines[2] = lines[2].replace("-", "+")
    return lines


def deck_rev(lines: List[str]):
    line = lines[1]
    parts = line.split("+")

    new_lines = [
        "import re",
        "input_parts = []",
        "for part in {}:".format(parts),
        "    indices = re.findall(r'\[(.*)]', part)",
        "    indices = indices[0]",
        "",
        "    left, right = indices.split(\":\")",
        "    if not left:",
        "        left = '0'",
        "",
        "    if not right:",
        "        right = str(k)",
        "",
        "    input_parts.append((int(left), int(right)))",
        "",
        "off = 0",
        "res = []",
        "for tpl in input_parts:",
        "    a, b = tpl",
        "    l = b - a",
        "    part = x[off:off + l]",
        "    res.append((a, part))",
        "    off += l",
        "",
        "input_parts = sorted(res, key=lambda x: x[0])",
        "res.clear()",
        "for a, data in input_parts:",
        "    res.extend(data)",
        "",
        "return res"
    ]

    new_lines = [lines[0]] + list(map(lambda x: "    " + x, new_lines))
    return new_lines


def add_rev(lines: List[str]):
    lines[2] = lines[2].replace("+", "-")
    return lines


def xor_rev(lines: List[str]):
    return lines


def chmul_rev(lines: List[str]):
    lines[2] = lines[2].replace("*", "//")
    return lines


def shuffle_rev(lines: List[str]):
    numbers = lines[1].split("in")[1].strip()
    if numbers.endswith("]]"):
        numbers = numbers[:-1]

    new_lines = [
        "res = [None] * k",
        "for i, o in zip(range(k), {}):".format(numbers),
        "    res[o] = x[i]",
        "return res"
    ]

    new_lines = [lines[0]] + list(map(lambda x: "    " + x, new_lines))
    return new_lines


def chadd_rev(lines: List[str]):
    lines[2] = lines[2].replace("+", "-")
    return lines


def cadd_rev(lines: List[str]):
    lines[1] = lines[1].replace("+", "-")
    return lines


def cmul_rev(lines: List[str]):
    lines[1] = lines[1].replace("*", "//")
    return lines


def chunk_rev(lines: List[str]):
    new_st = []
    num_started = False
    for c in lines[1]:
        if c.isdigit():
            if not num_started:
                new_st.append("-")
            num_started = True

        else:
            num_started = False

        new_st.append(c)

    lines[1] = ''.join(new_st)
    return lines


def csub_rev(lines: List[str]):
    lines[1] = lines[1].replace("-", "+")
    return lines


def chsub_rev(lines: List[str]):
    lines[2] = lines[2].replace("-", "+")
    return lines


def digsub_rev(lines: List[str]):
    sub_list = lines[1].split(".join(")[1].split("]")[0] + "]"

    new_lines = [
        "sub_dict = dict(zip(list(map(lambda x: int(x), {})), [str(x) for x in range(10)]))".format(sub_list),
        "return [int(str(n)[:1] + ''.join(sub_dict[int(p)] for p in str(n)[1:])) for n in x]"
    ]

    new_lines = [lines[0]] + list(map(lambda x: "    " + x, new_lines))
    return new_lines


if __name__ == "__main__":
    reverse_functions()