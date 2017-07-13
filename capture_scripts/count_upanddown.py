import csv
import os

# set this midpoint value depending on the gene in question
midpoint = 31942885

files = [name for name in os.listdir('.') if 'af_filter' in name]

for name in files:

    total = 0
    up_count = 0
    down_count = 0

    name_list = name.split('_')
    low = name_list[2]
    hi = name_list[3]
    size = name_list[4]
    sep = name_list[7]

    with open(name) as handle:

        csv_dict = csv.DictReader(handle, delimiter='\t')

        for line in csv_dict:

            if int(line['POS']) < midpoint:
                down_count += 1
            else:
                up_count += 1

            total += 1

        print '{} SNPs where {} bases, af thresholds {} - {}, span {}'.format(total, sep, low, hi, size)
        print '\tsplit around the midpoint is {}:{} (ratio: {})\n'.format(down_count, up_count,
                                                                      float(max(down_count, up_count)) / float(
                                                                          min(down_count, up_count)))
