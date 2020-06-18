INPUT_FILE = "./in.txt"
OUTPUT_FILE = "./out.txt"


def transformLine(line):
    if len(line) == 0:
        return None

    if '→' in line:
        symbols = line.split('→')
    elif '->' in line:
        symbols = line.split('->')
    else:
        symbols = line.split('')
        
    nonterminal = symbols[0].strip()
    terminals_str = symbols[1].strip()
    terminals = list(map(lambda x: x.strip(), terminals_str.split('|')))

    prods = []
    for phrase in terminals:
        letters_list = list(phrase.replace("eps", "ϵ").replace(".", "ϵ"))
        prods.append(' '.join(letters_list))

    return "{} -> {}".format(nonterminal, ' | '.join(prods))


def go():
    output = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    for line in lines:
        r = transformLine(line)
        if r:
            output.append(r)

    o_str = '\n'.join(output)
    print(o_str)

    with open(OUTPUT_FILE, "wb") as f:
        f.write(o_str.encode("utf-8"))


if __name__ == "__main__":
    go()
