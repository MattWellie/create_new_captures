#!/usr/bin/env bash


for sep in 30 50 70
do
    for span in 4 5 6 7 8
    do
        for ratio in 0.1 0.15 0.2 0.25
        do
            python ../scripts/filter_vcf_for_rhdo.py -i smn1_gnomad_+-${span}mb.vcf -sep ${sep} -t ${ratio}
        done
    done
done