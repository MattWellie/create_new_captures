import sys

"""
this script will take the <capture>_Report.txt from SureDesign and filter out any regions which are insufficiently 
covered by the probes selected
"""


try:
    # take arguments from the command line
    infile = sys.argv[1]
    outfile = sys.argv[2]
    # threshold = sys.argv[3]
except:
    print """to use this script please provide 2 arguments:\ninput report file\noutput file name"""
    sys.exit()

# check when the coverage analysis section of the file begins
region_start = False
with open(infile) as inhandle:

    with open(outfile, 'w') as outhandle:

        for line in inhandle:

            llist = line.split()

            # skip empty lines safely, and check if the TargetID field is found (column header at the start of coverage)
            try:
                if llist[0].rstrip() == 'TargetID':
                    region_start = True
                    continue

            except:
                continue

            # if the line can be split, and the region section is started...
            if not region_start:
                continue

            # re-iterate over the rest of the rest of the file under different conditions
            for line in inhandle:

                llist = line.split()

                # if low coverage is indicated
                if float(llist[-1]) == 1.0:
                    continue

                # otherwise, keep this entry (storing chr:pos-pos \t rsID)
                else:
                    print >>outhandle, '{}\t{}'.format(llist[1], llist[0])


