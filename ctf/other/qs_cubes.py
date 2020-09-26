import pprint
from binascii import unhexlify

with open("D:\\q2.txt", "rt") as f:
    lines = f.read().splitlines()

SIZE = len(lines)
print(SIZE)

cube = [[[0 for k in range(1)] for j in range(SIZE)] for _ in range(SIZE)]

for i, line in enumerate(lines):
    for j, c in enumerate(line.strip()):
        cube[i][j][0] = c


def get_size(cube):
    return len(cube), len(cube[0]), len(cube[0][0])

def print_size(cube):
    print("{}x{}x{}".format(len(cube), len(cube[0]), len(cube[0][0])))


def fold(cube, direction):
    x, y, z = get_size(cube)
    if x == 1 and y == 1:
        print_size(cube)
        flag = ''.join(cube[0][0])[::-1]
        return flag

    print_size(cube)
    print("{}".format("top" if direction else "left"))
    pprint.pprint(cube)
    print()

    if direction:  # up
        new_cube = [[[0 for _ in range(z * 2)] for _ in range(y)] for _ in range(x // 2)]

        for xi in range(x // 2, x):
            for yi in range(y):
                for zi in range(z):
                    new_cube[xi - x // 2][yi][zi] = cube[xi][yi][zi]

        # pprint.pprint(new_cube)

        for xi in range(0, x // 2):
            for yi in range(y):
                for zi in range(z, z*2):
                    new_cube[xi][yi][z*2-(zi-z)-1] = cube[x//2-xi-1][yi][zi - z]


        return fold(new_cube, False)

    else:  # left
        new_cube = [[[0 for _ in range(z * 2)] for _ in range(y // 2)] for _ in range(x)]

        for xi in range(x):
            for yi in range(y // 2, y):
                for zi in range(z):
                    new_cube[xi][yi - y // 2][zi] = cube[xi][yi][zi]

        for xi in range(x):
            for yi in range(0, y // 2):
                for zi in range(z, z*2):
                    new_cube[xi][yi][z*2-(zi-z)-1] = cube[xi][y//2-yi-1][zi - z]


        return fold(new_cube, True)


a = fold(cube, True)
print(a)
print(unhexlify(a))