#!/usr/bin/env python3
"""
Reverse complement Ltu chromosomes that have inverted orientation
relative to Lchi reference, based on SyRI warnings.
"""
import sys
import os

WORKDIR = '/data/hongky_data/comparative_genomics3'
INPUT_FASTA = os.path.join(WORKDIR, 'Ltu.chr_only.fasta')
OUTPUT_FASTA = os.path.join(WORKDIR, 'Ltu.chr_only.oriented.fasta')

# Ltu chromosomes that need reverse complementing (from SyRI log warnings)
RC_CHROMS = {
    'Chr03', 'Chr06', 'Chr07', 'Chr09', 'Chr10', 'Chr11',
    'Chr12', 'Chr13', 'Chr14', 'Chr15', 'Chr17', 'Chr18', 'Chr19'
}

COMP_TABLE = str.maketrans('ATCGatcgNnRrYySsWwKkMmBbDdHhVv',
                           'TAGCtagcNnYyRrSsWwMmKkVvHhDdBb')

def reverse_complement(seq):
    return seq.translate(COMP_TABLE)[::-1]

def read_fasta(filepath):
    """Read FASTA file, return list of (header, sequence)"""
    records = []
    header = None
    seq_parts = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('>'):
                if header is not None:
                    records.append((header, ''.join(seq_parts)))
                header = line
                seq_parts = []
            else:
                seq_parts.append(line)
    if header is not None:
        records.append((header, ''.join(seq_parts)))
    return records

def write_fasta(filepath, records, line_width=80):
    """Write FASTA file with specified line width"""
    with open(filepath, 'w') as f:
        for header, seq in records:
            f.write(header + '\n')
            for i in range(0, len(seq), line_width):
                f.write(seq[i:i+line_width] + '\n')

print(f"Reading {INPUT_FASTA}...")
records = read_fasta(INPUT_FASTA)
print(f"  Found {len(records)} sequences")

new_records = []
rc_count = 0
for header, seq in records:
    chrom_name = header.split()[0].lstrip('>')
    if chrom_name in RC_CHROMS:
        print(f"  Reverse complementing {chrom_name} ({len(seq):,} bp)")
        new_seq = reverse_complement(seq)
        new_records.append((header, new_seq))
        rc_count += 1
    else:
        print(f"  Keeping {chrom_name} as-is ({len(seq):,} bp)")
        new_records.append((header, seq))

print(f"\nReverse complemented {rc_count}/{len(records)} chromosomes")
print(f"Writing {OUTPUT_FASTA}...")
write_fasta(OUTPUT_FASTA, new_records)
print("Done!")
