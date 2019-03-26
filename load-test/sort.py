import sys
import time


def main():
    if len(sys.argv) != 3:
        print('args: input_file output_file')
        exit(1)
    fin = open(sys.argv[1])
    fout = open(sys.argv[2], 'w')
    lines = []
    for i, l in enumerate(fin):
        sp = l.strip().split('\t')
        lines.append((float(sp[0]), *sp[1:]))
        if i % 100000 == 0:
            print('read {} lines'.format(i))
    t0 = time.time()
    print('{} lines. sort now. {}'.format(len(lines), t0))
    lines.sort(key=lambda x: x[0])
    t1 = time.time()
    print('sorted, used {} seconds. writing'.format(t1 - t0))
    for i, l in enumerate(lines):
        print('{}\t{}\t{}\t{}'.format(*l), file=fout)
        if i % 100000 == 0:
            print('wrote {} lines'.format(i))


if __name__ == '__main__':
    main()