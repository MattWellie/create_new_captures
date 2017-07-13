import sys

file_out = sys.argv[1]
helena_in = sys.argv[2]

# associate the SNP positions with their frequency in real cases
h_dict = {}
with open(str(helena_in)) as handle:

    for line in handle:

        llist = line.split()
        h_dict[str(int(llist[1])+1).rstrip()] = llist[3]

with open(file_out, 'w') as handle:

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

            if not llist[1] in h_dict.keys():
                print 'no key entry for {}'.format(llist[1])
                continue

            print >>handle, '{}\t{}'.format(af, str(h_dict[llist[1]]).rstrip()).rstrip()