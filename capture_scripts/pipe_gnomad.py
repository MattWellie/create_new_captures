import sys

file_out = sys.argv[1]

with open(file_out, 'a') as handle:

    for line in sys.stdin:

        llist = line.split()
        pos = llist[1]

        if len(llist[3]) != 1 or len(llist[4]) != 1:
            continue

        else:
            info = llist[7]
            af = float(info.split(';')[1].replace('AF=', ''))

            if af == 0.0:
                continue

            print >>handle, '{}'.format(af).rstrip()
