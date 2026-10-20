#!/usr/bin/env python3
"""
Generate whole-genome dotplot and per-chromosome dotplots from BAM alignment.
Used to visually validate chromosome pairing from mapids.txt.
"""
import pysam
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from collections import defaultdict
import os

WORKDIR = '/data/hongky_data/comparative_genomics3'
OUTDIR = os.path.join(WORKDIR, 'syri_output')
BAM = os.path.join(OUTDIR, 'lchi_vs_ltu_oriented.sorted.bam')
MAPIDS = os.path.join(OUTDIR, 'mapids.txt')

# Read chromosome pairing
ref_to_qry = {}
with open(MAPIDS) as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            ref_to_qry[parts[0]] = parts[1]

print(f"Chromosome pairs from mapids.txt: {len(ref_to_qry)}")

# Define chromosome order (natural sort for ref)
def chr_sort_key(c):
    num = ''.join(filter(str.isdigit, c))
    return int(num) if num else 0

ref_chroms = sorted(ref_to_qry.keys(), key=chr_sort_key)

# Get reference chromosome lengths from BAM header
bam = pysam.AlignmentFile(BAM, 'rb')
ref_lengths = {}
for sq in bam.header['SQ']:
    name = sq['SN']
    length = sq['LN']
    ref_lengths[name] = length

# Get query chromosome lengths from FASTA file (not in BAM header)
QRY_FASTA = os.path.join(WORKDIR, 'Ltu.chr_only.oriented.fasta')
qry_lengths = {}
current_name = None
current_len = 0
with open(QRY_FASTA, 'r') as f:
    for line in f:
        if line.startswith('>'):
            if current_name:
                qry_lengths[current_name] = current_len
            current_name = line.strip().lstrip('>').split()[0]
            current_len = 0
        else:
            current_len += len(line.strip())
    if current_name:
        qry_lengths[current_name] = current_len

print(f"Ref chroms: {len(ref_lengths)}, Query chroms: {len(qry_lengths)}")
for c in sorted(qry_lengths.keys(), key=chr_sort_key):
    print(f"  {c}: {qry_lengths[c]:,} bp")

# ── Extract alignments ──
print("Reading alignments from BAM...")
alignments = []  # (ref_chr, ref_start, ref_end, qry_chr, qry_start, qry_end, is_reverse)
count = 0
for read in bam.fetch():
    if read.is_unmapped or read.is_secondary:
        continue
    if read.mapping_quality < 10:
        continue

    ref_chr = read.reference_name
    qry_chr = read.query_name
    ref_start = read.reference_start
    ref_end = read.reference_end

    # Get query coordinates from aligned pairs
    pairs = read.get_aligned_pairs(matches_only=False)
    qry_positions = [p[0] for p in pairs if p[0] is not None]
    if not qry_positions:
        continue
    qry_start = min(qry_positions)
    qry_end = max(qry_positions)

    is_reverse = read.is_reverse

    alignments.append((ref_chr, ref_start, ref_end, qry_chr, qry_start, qry_end, is_reverse))
    count += 1
    if count % 100000 == 0:
        print(f"  Read {count:,} alignments...")

bam.close()
print(f"Total alignments: {count:,}")

# ── PLOT 1: Whole-genome dotplot ──
print("\nGenerating whole-genome dotplot...")

# Build cumulative offsets for ref and query chromosomes
ref_offsets = {}
cumul = 0
for c in ref_chroms:
    ref_offsets[c] = cumul
    cumul += ref_lengths.get(c, 0)
total_ref = cumul

# Order query chroms to match ref order
qry_order = [ref_to_qry[rc] for rc in ref_chroms if rc in ref_to_qry]
qry_offsets = {}
cumul = 0
for c in qry_order:
    qry_offsets[c] = cumul
    cumul += qry_lengths.get(c, 0)
total_qry = cumul

fig, ax = plt.subplots(figsize=(14, 14))

fwd_x, fwd_y = [], []
rev_x, rev_y = [], []

for ref_chr, rs, re, qry_chr, qs, qe, is_rev in alignments:
    if ref_chr not in ref_offsets or qry_chr not in qry_offsets:
        continue

    rx = ref_offsets[ref_chr] + (rs + re) / 2
    qy = qry_offsets[qry_chr] + (qs + qe) / 2

    if is_rev:
        rev_x.append(rx)
        rev_y.append(qy)
    else:
        fwd_x.append(rx)
        fwd_y.append(qy)

ax.scatter(fwd_x, fwd_y, c='#2166ac', s=0.1, alpha=0.3, rasterized=True, label='Forward')
ax.scatter(rev_x, rev_y, c='#b2182b', s=0.1, alpha=0.3, rasterized=True, label='Reverse')

# Chromosome boundary lines and labels
for c in ref_chroms:
    off = ref_offsets[c]
    ax.axvline(x=off, color='gray', linewidth=0.3, alpha=0.5)
    mid = off + ref_lengths.get(c, 0) / 2
    ax.text(mid, -total_qry * 0.02, c.replace('chr', ''), ha='center', va='top', fontsize=7)

for c in qry_order:
    off = qry_offsets[c]
    ax.axhline(y=off, color='gray', linewidth=0.3, alpha=0.5)
    mid = off + qry_lengths.get(c, 0) / 2
    ax.text(-total_ref * 0.02, mid, c.replace('Chr', ''), ha='right', va='center', fontsize=7)

ax.set_xlim(-total_ref * 0.05, total_ref * 1.02)
ax.set_ylim(-total_qry * 0.05, total_qry * 1.02)
ax.set_xlabel('L. chinense (Reference)', fontsize=12)
ax.set_ylabel('L. tulipifera (Query)', fontsize=12)
ax.set_title('Whole-Genome Dotplot: L. chinense vs L. tulipifera', fontsize=14)
ax.set_aspect('equal')

legend_elements = [
    mpatches.Patch(color='#2166ac', label='Forward alignment'),
    mpatches.Patch(color='#b2182b', label='Reverse alignment'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

plt.tight_layout()
dotplot_path = os.path.join(OUTDIR, 'dotplot_whole_genome.png')
plt.savefig(dotplot_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: {dotplot_path}")

# ── PLOT 2: Per-chromosome dotplots (4x5 grid) ──
print("\nGenerating per-chromosome dotplots...")
fig, axes = plt.subplots(4, 5, figsize=(20, 16))
axes_flat = axes.flatten()

for i, ref_chr in enumerate(ref_chroms):
    if i >= 19:
        break
    ax = axes_flat[i]
    qry_chr = ref_to_qry.get(ref_chr)
    if not qry_chr:
        ax.set_visible(False)
        continue

    fwd_rx, fwd_ry = [], []
    rev_rx, rev_ry = [], []

    for rc, rs, re, qc, qs, qe, is_rev in alignments:
        if rc == ref_chr and qc == qry_chr:
            rmid = (rs + re) / 2
            qmid = (qs + qe) / 2
            if is_rev:
                rev_rx.append(rmid)
                rev_ry.append(qmid)
            else:
                fwd_rx.append(rmid)
                fwd_ry.append(qmid)

    ax.scatter(fwd_rx, fwd_ry, c='#2166ac', s=0.3, alpha=0.4, rasterized=True)
    ax.scatter(rev_rx, rev_ry, c='#b2182b', s=0.3, alpha=0.4, rasterized=True)

    ref_len = ref_lengths.get(ref_chr, 0)
    qry_len = qry_lengths.get(qry_chr, 0)
    ax.set_xlim(0, ref_len)
    ax.set_ylim(0, qry_len)
    ax.set_title(f'{ref_chr} vs {qry_chr}', fontsize=9, fontweight='bold')
    ax.tick_params(labelsize=6)

    # Add alignment count
    total_pts = len(fwd_rx) + len(rev_rx)
    fwd_pct = len(fwd_rx) / total_pts * 100 if total_pts > 0 else 0
    ax.text(0.02, 0.98, f'n={total_pts:,}\nfwd={fwd_pct:.0f}%',
            transform=ax.transAxes, fontsize=6, va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Hide extra axes
for j in range(19, 20):
    axes_flat[j].set_visible(False)

fig.suptitle('Per-Chromosome Dotplot: L. chinense vs L. tulipifera\n(blue=forward, red=reverse)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
per_chr_path = os.path.join(OUTDIR, 'dotplot_per_chromosome.png')
plt.savefig(per_chr_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: {per_chr_path}")

# ── PLOT 3: Chromosome pairing heatmap (alignment coverage matrix) ──
print("\nGenerating chromosome pairing heatmap...")

# Build alignment length matrix: ref_chr x qry_chr
all_qry_chroms = sorted(qry_lengths.keys(), key=chr_sort_key)
if not all_qry_chroms:
    all_qry_chroms = sorted(set(qc for _, _, _, qc, _, _, _ in alignments), key=chr_sort_key)
    for qc in all_qry_chroms:
        if qc not in qry_lengths:
            qry_lengths[qc] = max((qe for _, _, _, c, _, qe, _ in alignments if c == qc), default=0)
pair_matrix = np.zeros((len(ref_chroms), len(all_qry_chroms)))

ref_idx = {c: i for i, c in enumerate(ref_chroms)}
qry_idx = {c: i for i, c in enumerate(all_qry_chroms)}

for rc, rs, re, qc, qs, qe, is_rev in alignments:
    if rc in ref_idx and qc in qry_idx:
        aln_len = re - rs
        pair_matrix[ref_idx[rc], qry_idx[qc]] += aln_len

# Normalize each row to percentage
row_sums = pair_matrix.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1
pair_pct = pair_matrix / row_sums * 100

fig, ax = plt.subplots(figsize=(12, 10))
im = ax.imshow(pair_pct, cmap='YlOrRd', aspect='auto', interpolation='nearest')
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('% of ref chromosome aligned', fontsize=10)

ax.set_xticks(range(len(all_qry_chroms)))
ax.set_xticklabels([c.replace('Chr', 'C') for c in all_qry_chroms], fontsize=8, rotation=45)
ax.set_yticks(range(len(ref_chroms)))
ax.set_yticklabels(ref_chroms, fontsize=8)
ax.set_xlabel('L. tulipifera (Query)', fontsize=12)
ax.set_ylabel('L. chinense (Reference)', fontsize=12)
ax.set_title('Chromosome Pairing Heatmap\n(% alignment coverage per ref chromosome)', fontsize=13)

# Annotate dominant pairs
for i, rc in enumerate(ref_chroms):
    if pair_pct.shape[1] == 0:
        break
    best_j = np.argmax(pair_pct[i])
    best_val = pair_pct[i, best_j]
    if best_val > 5:
        ax.text(best_j, i, f'{best_val:.0f}%', ha='center', va='center',
                fontsize=6, fontweight='bold', color='white' if best_val > 50 else 'black')

plt.tight_layout()
heatmap_path = os.path.join(OUTDIR, 'dotplot_pairing_heatmap.png')
plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"  Saved: {heatmap_path}")

print("\n=== Summary ===")
print("Generated 3 validation plots:")
print(f"  1. {dotplot_path}")
print(f"  2. {per_chr_path}")
print(f"  3. {heatmap_path}")
print("ALL_DOTPLOT_DONE")
