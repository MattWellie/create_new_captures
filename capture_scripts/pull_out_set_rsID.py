from random import random
import csv
import sys
import os

print """
arguments!
    1) input file name
    2) output file name
    3) threshold for random selection (float, randoms > input will be kept. Defaults to 0.01)
      """

# check argument list length to determine input
if len(sys.argv) == 4:
    print 'all arguments specified'
    input_name = sys.argv[1]
    output_name = sys.argv[2]
    threshold = float(sys.argv[3])

elif len(sys.argv) == 3:
    print '2 argument mode selected'
    input_name = sys.argv[1]
    output_name = sys.argv[2]
    threshold = float(0.01)

else:
    print "WTF are you doing... at least an input and output file pls"
    sys.exit(1)

if not os.path.exists(str(input_name)):
    print "Input file can't be seen by the OS..."
    sys.exit(1)

# set a counter for the number of kept IDs
count = 0

# iterate over the input file, generating a random number each time
# for each row, check if the random number is below the threshold - if so, keep it, else move on
# 'keep it' means print the RSID to a file
with open(str(input_name)) as handle:

    # write direct to outfile
    with open(str(output_name), 'w')as outhandle:

        csv_rd = csv.DictReader(handle, delimiter='\t')

        for line in csv_rd:

            if random() < threshold:

                print >>outhandle, line['ID'].rstrip()
                count += 1

print '{} IDs were kept'.format(count)
