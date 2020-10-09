import itertools
import subprocess

DATA_LEN = 6
data = list(range(1, DATA_LEN + 1))


def numOfSubseq(arr):
    n = len(arr)
    lis = [1] * n

    for i in range(1, n):
        for j in range(0, i):
            if arr[i] > arr[j] and lis[i] < lis[j] + 1:
                lis[i] = lis[j] + 1


    return max(lis)


for p in itertools.permutations(data, DATA_LEN):
    p = list(p)
    with open("./data_test", "wb") as f:
        f.write(int.to_bytes(DATA_LEN, 4, 'little'))
        for n in p:
            f.write(int.to_bytes(n, 4, 'little'))

    try:
        output = subprocess.check_output(["./my_cruncher", "data_test"])
        my_return = numOfSubseq(p)

        # if my_return != int(output.decode().strip().split(':')[1]):
        print(p)
        print(output.decode().strip())
        print("My alg:       {}".format(my_return))
        print()


    except Exception as e:
        print(e)
