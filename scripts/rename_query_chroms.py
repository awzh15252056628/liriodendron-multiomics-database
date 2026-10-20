#!/usr/bin/env python3
"""
Rename query (Ltu) chromosomes according to SyRI mapids.txt,
so that query chrom names match reference chrom names.
This allows running SyRI with --no-chrmatch.
"""
import os

WORKDIR = '/data/hongky_data/comparative_genomics3'
INPUT_FASTA = os.path.join(WORKDIR, 'Ltu.chr_only.oriented.fasta')
OUTPUT_FASTA = os.path.join(WORKDIR, 'Ltu.chr_only.oriented.renamed.fasta')
MAPIDS = os.path.join(WORKDIR, 'syri_output', 'mapids.txt')

# Read mapids: ref_chr -> query_chr, we need the reverse: query_chr -> ref_chr
qry_to_ref = {}
with open(MAPIDS, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        ref_chr = parts[0]   # e.g. chr1
        qry_chr = parts[1]   # e.g. Chr01
        qry_to_ref[qry_chr] = ref_chr

print("Chromosome rename mapping (query -> reference name):")
for q, r in sorted(qry_to_ref.items()):
    print(f"  {q} -> {r}")

print(f"\nReading {INPUT_FASTA}...")
with open(INPUT_FASTA, 'r') as fin, open(OUTPUT_FASTA, 'w') as fout:
    for line in fin:
        if line.startswith('>'):
            old_name = line.strip().lstrip('>').split()[0]
            if old_name in qry_to_ref:
                new_name = qry_to_ref[old_name]
                fout.write(f'>{new_name}\n')
                print(f"  Renamed: {old_name} -> {new_name}")
            else:
                fout.write(line)
                print(f"  Kept as-is: {old_name}")
        else:
            fout.write(line)

print(f"\nOutput: {OUTPUT_FASTA}")
print("Done!")
