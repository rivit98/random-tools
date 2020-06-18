INPUT_FILE = "./in.txt"
OUTPUT_FILE = "./out.txt"


def transformLine(line):
    if len(line) == 0:
        return []

    res = []

    if '→' in line:
        symbols = line.split('→')
    else:
        symbols = line.split('->')
        
    nonterminal = symbols[0].strip()
    terminals_str = symbols[1].strip()
    terminals = list(map(lambda x: x.strip(), terminals_str.split('|')))

    for phrase in terminals:
        if phrase == "eps" or phrase == '.':
            res.append("{} -> .".format(nonterminal))
        else:
            letters_list = list(phrase)
            res.append("{} -> {} .".format(nonterminal, ' '.join(letters_list)))

    return res


def go():
    output = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    for line in lines:
        r = transformLine(line)
        output.extend(r)

    o_str = '\n'.join(output)
    print(o_str)

    with open(OUTPUT_FILE, "w") as f:
        f.write(o_str)


if __name__ == "__main__":
    go()
