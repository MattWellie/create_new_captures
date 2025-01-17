from argparse import ArgumentParser
import sys

"""
This script will take a VCF input stream (Gnomad, pre-filtered to a region of interest), and filter this dataset
according to the passed parameters

This will receive a few arguments:
    output file name (default to an alteration of the input?)
    selection radius (e.g. 0.15 would create the boundaries 0.5-0.15 : 0.5+0.15 = 0.35:0.65)
    separation minimum (e.g. for 20, SNPs within 20bp will not be selected
"""


parser = ArgumentParser(description='take a gnomad VCF file, region filtered using tabix, and filter the variants down '
                                    'to those which are within the provided allele freq threshold [and base position '
                                    'separation (optional)]')
parser.add_argument('-o', help='output filtered Gnomad file', type=str, default=False)
parser.add_argument('-sep', help='minimum separation between SNPs in base pairs (default = 0)', default=0, type=int)
parser.add_argument('-t', help='allele_freq thresholds will be 0.5 +/- this argument', required=True, type=float)
parser.add_argument('-span', help='a number representing the rough span up and downstream of these SNPs', required=True)
args = parser.parse_args()

# header row contents to fir VCF format - allows loading into IGV/GenomeBrowse
cols = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']

# take the arguments from the argparse input
low_af_threshold = 0.5 - args.t
hi_af_threshold = 0.5 + args.t
separation = args.sep

if args.o:
    outfile = args.o

else:
    # create a default name for the file to take if not specified - descriptive
    outfile = 'af_filter_{}_{}_sep{}_pm{}mb.vcf'.format(low_af_threshold, hi_af_threshold, separation, args.span)

# the initial position of the first SNP - checked to overwrite 0 with a real value
prev_pos = 0

# open both in and out file-handles to ensure file size is no limitation
snp_count = 0

with open(outfile, 'a') as outhandle:

    # print headers out
    print >>outhandle, '\t'.join(cols)

    # create a dictionary based on the row and headers (checked working for Gnomad, may differ for 1000G)
    for row in sys.stdin:

        drow = dict(zip(cols, row.split()))

        # only take variants which have passed on all filters
        if drow['FILTER'].rstrip() != 'PASS':
            continue

        # reject any multi-allelic SNPs
        if ',' in drow['ALT']:
            continue

        # reject any multi-allelic SNPs
        if len(drow['ALT']) != 1:
            continue

        # reject any multi-allelic SNPs
        if len(drow['REF']) != 1:
            continue

        # get the annotation entry, which will have all available gnomad details
        annot = drow['INFO']

        # get the second element from the ';' delimited data - allele freq in n.8-eX notation. cast as a float
        af = float(annot.split(';')[1].replace('AF=', ''))

        # is the allele freq within the selected thresholds?
        if low_af_threshold <= af <= hi_af_threshold:

            # if so, take the allele freq in the file as a String to write into the output
            drow['INFO'] = str(af)

            # check whether the previous SNP position is too close to this SNP. this is done here to ensure that
            # only the SNPs that will be written to the output file are considered for proximity... Gnomad has a SNP
            # at almost every position so checking separation before filter means most are never considered for AF
            if prev_pos == 0:
                prev_pos = int(drow['POS'])
            elif (prev_pos + separation) > int(drow['POS']):
                continue
            else:
                prev_pos = int(drow['POS'])

            # print dat shit to the output file
            print >>outhandle, '\t'.join([drow[x] for x in cols])
            snp_count += 1

print '{} SNPs kept after filtering'.format(snp_count)
