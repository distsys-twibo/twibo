import sys
import time
import random


def main():
    if len(sys.argv) != 3:
        print('args: input_file n')
        exit(1)
    fin = open(sys.argv[1])
    n = int(sys.argv[2])
    fouts = [open(sys.argv[1] + '.{}'.format(i), 'w') for i in range(n)]
    for i, l in enumerate(fin):
        print(l.strip(), file=fouts[i % n])


if __name__ == '__main__':
    main()