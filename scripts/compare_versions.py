#!/usr/bin/env python3
"""
Compare SyRI Version A (default) vs Version B (conservative TD params).
Generate summary statistics table and comparison plots.
"""
import os
from collections import defaultdict

WORKDIR = '/data/hongky_data/comparative_genomics3'
OUTDIR_A = os.path.join(WORKDIR, 'syri_versionA')
OUTDIR_B = os.path.join(WORKDIR, 'syri_versionB')

# SyRI annotation types
SV_TYPES = {
    'SYN': 'Synteny',
    'INV': 'Inversion',
    'TRANS': 'Translocation',
    'DUP': 'Duplication',
    'INVTR': 'Inverted Trans.',
    'INVDP': 'Inverted Dup.',
    'NOTAL': 'Not aligned',
}

SMALL_VAR_TYPES = {
    'SNP': 'SNP',
    'INS': 'Insertion',
    'DEL': 'Deletion',
}


def parse_syri_out(filepath):
    """Parse syri.out and collect statistics per SV type."""
    sv_stats = defaultdict(lambda: {'count': 0, 'total_len': 0, 'max_len': 0})
    small_var_counts = defaultdict(int)

    # Also track per-chromosome SV regions for overlap comparison
    sv_regions = defaultdict(list)  # type -> list of (chr, start, end)

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 11:
                continue

            ref_chr = parts[0]
            ref_start = parts[1]
            ref_end = parts[2]
            ann_type = parts[10]

            # Structural variants (block-level annotations)
            for sv_key in SV_TYPES:
                if ann_type == sv_key:
                    try:
                        start = int(ref_start)
                        end = int(ref_end)
                        length = abs(end - start)
                        sv_stats[sv_key]['count'] += 1
                        sv_stats[sv_key]['total_len'] += length
                        if length > sv_stats[sv_key]['max_len']:
                            sv_stats[sv_key]['max_len'] = length
                        sv_regions[sv_key].append((ref_chr, start, end))
                    except ValueError:
                        pass
                    break

            # Small variants
            for sm_key in SMALL_VAR_TYPES:
                if ann_type == sm_key:
                    small_var_counts[sm_key] += 1
                    break

    return sv_stats, small_var_counts, sv_regions


def compute_overlap(regions_a, regions_b, sv_type):
    """
    Compute how much of Version A's SV regions overlap with Version B's.
    Simple interval overlap on same chromosome.
    Returns (overlap_bp, total_a_bp, total_b_bp, overlap_count_a).
    """
    # Build interval index for B by chromosome
    b_by_chr = defaultdict(list)
    for chrom, start, end in regions_b:
        b_by_chr[chrom].append((start, end))

    # Sort B intervals
    for chrom in b_by_chr:
        b_by_chr[chrom].sort()

    overlap_bp = 0
    total_a_bp = 0
    overlap_count = 0

    for chrom, a_start, a_end in regions_a:
        a_len = a_end - a_start
        total_a_bp += a_len
        found_overlap = False

        for b_start, b_end in b_by_chr.get(chrom, []):
            # Check overlap
            ov_start = max(a_start, b_start)
            ov_end = min(a_end, b_end)
            if ov_start < ov_end:
                overlap_bp += (ov_end - ov_start)
                found_overlap = True

        if found_overlap:
            overlap_count += 1

    total_b_bp = sum(e - s for _, s, e in regions_b)

    return overlap_bp, total_a_bp, total_b_bp, overlap_count


print("=" * 70)
print("  SyRI Robustness Comparison: Version A (default) vs Version B (strict)")
print("=" * 70)
print()

# Parse both versions
print("Parsing Version A (default params)...")
sv_a, sm_a, regions_a = parse_syri_out(os.path.join(OUTDIR_A, 'syri.out'))
print("Parsing Version B (conservative TD params)...")
sv_b, sm_b, regions_b = parse_syri_out(os.path.join(OUTDIR_B, 'syri.out'))

# Print comparison table - Structural Variants
print()
print("-" * 70)
print(f"{'SV Type':<18} {'Version A':>20}  {'Version B':>20}  {'Change':>8}")
print(f"{'':18} {'Count':>8} {'Length(Mb)':>11}  {'Count':>8} {'Length(Mb)':>11}  {'':>8}")
print("-" * 70)

for sv_key in ['SYN', 'INV', 'TRANS', 'DUP', 'INVTR', 'INVDP', 'NOTAL']:
    name = SV_TYPES[sv_key]
    ca = sv_a[sv_key]['count']
    la = sv_a[sv_key]['total_len'] / 1e6
    cb = sv_b[sv_key]['count']
    lb = sv_b[sv_key]['total_len'] / 1e6
    if ca > 0:
        change_pct = f"{(cb - ca) / ca * 100:+.1f}%"
    else:
        change_pct = "N/A"
    print(f"{name:<18} {ca:>8,} {la:>10.1f}  {cb:>8,} {lb:>10.1f}  {change_pct:>8}")

print("-" * 70)
print()

# Print small variants
print(f"{'Small Variants':<18} {'Version A':>10}  {'Version B':>10}  {'Change':>8}")
print("-" * 50)
for sm_key in ['SNP', 'INS', 'DEL']:
    name = SMALL_VAR_TYPES[sm_key]
    ca = sm_a[sm_key]
    cb = sm_b[sm_key]
    if ca > 0:
        change_pct = f"{(cb - ca) / ca * 100:+.1f}%"
    else:
        change_pct = "N/A"
    print(f"{name:<18} {ca:>10,}  {cb:>10,}  {change_pct:>8}")
print()

# Overlap analysis for key SV types
print("=" * 70)
print("  Overlap Analysis: regions shared between Version A and Version B")
print("=" * 70)
print()
print(f"{'SV Type':<18} {'A regions':>10} {'B regions':>10} {'A in B':>10} {'% A->B':>8} {'bp overlap':>12}")
print("-" * 70)

for sv_key in ['INV', 'TRANS', 'DUP', 'INVTR', 'INVDP']:
    name = SV_TYPES[sv_key]
    ra = regions_a.get(sv_key, [])
    rb = regions_b.get(sv_key, [])

    if ra and rb:
        ov_bp, total_a, total_b, ov_count = compute_overlap(ra, rb, sv_key)
        pct = ov_count / len(ra) * 100 if len(ra) > 0 else 0
        print(f"{name:<18} {len(ra):>10,} {len(rb):>10,} {ov_count:>10,} {pct:>7.1f}% {ov_bp/1e6:>10.1f} Mb")
    else:
        print(f"{name:<18} {len(ra):>10,} {len(rb):>10,}     --       --           --")

print()
print("Interpretation:")
print("  - Regions present in BOTH versions are high-confidence SVs")
print("  - Regions only in Version A but not B were likely borderline calls")
print("    removed by stricter TD filtering")
print("  - High overlap % = robust signal, Low overlap % = sensitive to params")
print()

# Save report
report_path = os.path.join(WORKDIR, 'syri_output', 'robustness_comparison.txt')
with open(report_path, 'w') as f:
    f.write("SyRI Robustness Comparison: Version A (default) vs Version B (strict)\n")
    f.write("=" * 70 + "\n\n")
    f.write("Version A: default SyRI parameters\n")
    f.write("Version B: --tdgaplen 100000 --unic 5000 --unip 0.8 --tdmaxolp 0.5\n\n")

    f.write(f"{'SV Type':<18} {'Version A':>20}  {'Version B':>20}\n")
    f.write(f"{'':18} {'Count':>8} {'Length(Mb)':>11}  {'Count':>8} {'Length(Mb)':>11}\n")
    f.write("-" * 62 + "\n")
    for sv_key in ['SYN', 'INV', 'TRANS', 'DUP', 'INVTR', 'INVDP', 'NOTAL']:
        name = SV_TYPES[sv_key]
        ca = sv_a[sv_key]['count']
        la = sv_a[sv_key]['total_len'] / 1e6
        cb = sv_b[sv_key]['count']
        lb = sv_b[sv_key]['total_len'] / 1e6
        f.write(f"{name:<18} {ca:>8,} {la:>10.1f}  {cb:>8,} {lb:>10.1f}\n")

    f.write("\n\nSmall Variants\n")
    f.write("-" * 50 + "\n")
    for sm_key in ['SNP', 'INS', 'DEL']:
        name = SMALL_VAR_TYPES[sm_key]
        ca = sm_a[sm_key]
        cb = sm_b[sm_key]
        f.write(f"{name:<18} {ca:>10,}  {cb:>10,}\n")

print(f"Report saved: {report_path}")
print("COMPARE_DONE")
