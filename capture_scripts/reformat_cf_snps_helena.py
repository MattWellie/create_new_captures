name = 'CF_RHDO_counts.csv'

t = True
with open(name) as handle:

    for line in handle:

        if t:
            t = False
            continue

        llist = line.rstrip().split(',')
        chrom = str(llist[1].replace('"', '').replace('chr', ''))
        pos = int(llist[2].replace('"', ''))
        freq = int(llist[3].replace('"', ''))

        # initially, try for exact positions
        print '{}\t{}\t{}\t{}\t"{}"'.format(chrom, pos-1, pos+1, freq, line.rstrip())
