#!/usr/bin/env python3
"""
Gene structure comparison between L. chinense and L. tulipifera
Parses GFF files and generates gene-level comparative statistics
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import os

WORKDIR = '/data/hongky_data/comparative_genomics3'
OUTDIR = os.path.join(WORKDIR, 'syri_output')

plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def parse_gff(gff_file, chr_prefix=None):
    """Parse GFF file and extract gene/mRNA/CDS/exon information"""
    print(f"Parsing GFF: {gff_file}")

    genes = []
    exon_counts = defaultdict(int)
    cds_lens = defaultdict(list)

    with open(gff_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue

            chr_id = parts[0]
            feature = parts[2]
            start = int(parts[3])
            end = int(parts[4])
            strand = parts[6]
            attrs = parts[8]

            # Only process chromosome-level data (skip scaffolds)
            if chr_prefix:
                if not chr_id.startswith(chr_prefix):
                    continue

            if feature == 'mRNA':
                gene_id = ''
                for attr in attrs.split(';'):
                    if attr.startswith('ID='):
                        gene_id = attr.split('=')[1]
                        break

                genes.append({
                    'chr': chr_id,
                    'start': start,
                    'end': end,
                    'length': end - start + 1,
                    'strand': strand,
                    'gene_id': gene_id,
                })

            elif feature == 'exon':
                parent = ''
                for attr in attrs.split(';'):
                    if attr.startswith('Parent='):
                        parent = attr.split('=')[1]
                        break
                exon_counts[parent] += 1

            elif feature == 'CDS':
                parent = ''
                for attr in attrs.split(';'):
                    if attr.startswith('Parent='):
                        parent = attr.split('=')[1]
                        break
                cds_lens[parent].append(end - start + 1)

    df = pd.DataFrame(genes)

    # Add exon count and CDS total length
    if not df.empty:
        df['exon_count'] = df['gene_id'].map(exon_counts).fillna(0).astype(int)
        df['cds_total_len'] = df['gene_id'].map(
            lambda x: sum(cds_lens.get(x, []))
        )

    print(f"  Genes (mRNA): {len(df)}")
    print(f"  Chromosomes: {df['chr'].nunique() if not df.empty else 0}")
    return df


def plot_gene_comparison(lchi, ltu, output_prefix):
    """Generate comprehensive gene comparison plots"""
    print("Generating gene comparison plots...")

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    # 1. Gene length distribution
    ax = axes[0, 0]
    ax.hist(lchi['length'].clip(upper=30000), bins=60, alpha=0.6,
            label=f'L. chinense (n={len(lchi):,})', color='#3498db', density=True)
    ax.hist(ltu['length'].clip(upper=30000), bins=60, alpha=0.6,
            label=f'L. tulipifera (n={len(ltu):,})', color='#e74c3c', density=True)
    ax.set_xlabel('Gene Length (bp)')
    ax.set_ylabel('Density')
    ax.set_title('Gene Length Distribution', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Exon count distribution
    ax = axes[0, 1]
    max_exon = 20
    lchi_exons = lchi['exon_count'].clip(upper=max_exon)
    ltu_exons = ltu['exon_count'].clip(upper=max_exon)
    bins = range(0, max_exon + 2)
    ax.hist(lchi_exons, bins=bins, alpha=0.6, label='L. chinense', color='#3498db', density=True)
    ax.hist(ltu_exons, bins=bins, alpha=0.6, label='L. tulipifera', color='#e74c3c', density=True)
    ax.set_xlabel('Exon Count per Gene')
    ax.set_ylabel('Density')
    ax.set_title('Exon Count Distribution', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 3. CDS total length
    ax = axes[0, 2]
    ax.hist(lchi['cds_total_len'].clip(upper=5000), bins=50, alpha=0.6,
            label='L. chinense', color='#3498db', density=True)
    ax.hist(ltu['cds_total_len'].clip(upper=5000), bins=50, alpha=0.6,
            label='L. tulipifera', color='#e74c3c', density=True)
    ax.set_xlabel('Total CDS Length (bp)')
    ax.set_ylabel('Density')
    ax.set_title('CDS Total Length Distribution', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Genes per chromosome
    ax = axes[1, 0]
    lchi_chr = lchi['chr'].value_counts().sort_index()
    ltu_chr = ltu['chr'].value_counts().sort_index()

    n_chr = min(len(lchi_chr), len(ltu_chr), 19)
    x = np.arange(n_chr)
    width = 0.35
    ax.bar(x - width/2, lchi_chr.values[:n_chr], width,
           label='L. chinense', color='#3498db', alpha=0.8)
    ax.bar(x + width/2, ltu_chr.values[:n_chr], width,
           label='L. tulipifera', color='#e74c3c', alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(lchi_chr.index[:n_chr], rotation=45, ha='right', fontsize=8)
    ax.set_xlabel('Chromosome')
    ax.set_ylabel('Gene Count')
    ax.set_title('Genes per Chromosome', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    # 5. Gene length boxplot
    ax = axes[1, 1]
    data = [lchi['length'].clip(upper=20000), ltu['length'].clip(upper=20000)]
    bp = ax.boxplot(data, labels=['L. chinense', 'L. tulipifera'], patch_artist=True)
    bp['boxes'][0].set_facecolor('#3498db')
    bp['boxes'][0].set_alpha(0.6)
    bp['boxes'][1].set_facecolor('#e74c3c')
    bp['boxes'][1].set_alpha(0.6)
    ax.set_ylabel('Gene Length (bp)')
    ax.set_title('Gene Length Comparison', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    # 6. Summary stats table
    ax = axes[1, 2]
    ax.axis('off')
    summary = f"""
    ╔══════════════════════════════════════════╗
    ║    Gene Structure Summary                ║
    ╠══════════════════════════════════════════╣
    ║                 L.chi      L.tul         ║
    ║  Total genes:   {len(lchi):>6,d}     {len(ltu):>6,d}        ║
    ║  Mean length:   {lchi['length'].mean():>6.0f}     {ltu['length'].mean():>6.0f}     bp ║
    ║  Median length: {lchi['length'].median():>6.0f}     {ltu['length'].median():>6.0f}     bp ║
    ║  Mean exons:    {lchi['exon_count'].mean():>6.1f}     {ltu['exon_count'].mean():>6.1f}        ║
    ║  Mean CDS len:  {lchi['cds_total_len'].mean():>6.0f}     {ltu['cds_total_len'].mean():>6.0f}     bp ║
    ║  Chromosomes:   {lchi['chr'].nunique():>6d}     {ltu['chr'].nunique():>6d}        ║
    ╚══════════════════════════════════════════╝
    """
    ax.text(0.05, 0.5, summary, fontsize=10, family='monospace',
            verticalalignment='center', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.suptitle('Gene Structure Comparison: L. chinense vs L. tulipifera',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_gene_comparison.png', dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_prefix}_gene_comparison.png")
    plt.close()


def plot_gene_density(lchi, ltu, output_prefix, window=1000000):
    """Plot gene density comparison"""
    print("Plotting gene density comparison...")

    fig, axes = plt.subplots(2, 1, figsize=(16, 10), sharex=False)

    for ax, (species_name, genes, color) in zip(axes, [
        ('L. chinense', lchi, '#3498db'),
        ('L. tulipifera', ltu, '#e74c3c')
    ]):
        for chr_id in sorted(genes['chr'].unique()):
            chr_genes = genes[genes['chr'] == chr_id]
            max_pos = chr_genes['end'].max()

            positions = []
            densities = []
            for w_start in range(0, int(max_pos), window):
                w_end = w_start + window
                n_genes = len(chr_genes[(chr_genes['start'] >= w_start) &
                                        (chr_genes['start'] < w_end)])
                positions.append(w_start / 1e6)
                densities.append(n_genes)

            ax.plot(positions, densities, alpha=0.7, linewidth=1, label=chr_id)

        ax.set_ylabel('Genes per Mb')
        ax.set_title(f'{species_name} Gene Density', fontweight='bold')
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=7)
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel('Position (Mb)')
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_gene_density.png', dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_prefix}_gene_density.png")
    plt.close()


def main():
    print("=" * 60)
    print("  Gene Structure Comparison Analysis")
    print("=" * 60)
    print()

    gff_lchi = os.path.join(WORKDIR, 'Lchi_zong.gff')
    gff_ltu = os.path.join(WORKDIR, 'LtulipiferaYP108A_766_v1.1.gene_exons.gff')

    # Parse GFF files (filter to chromosomes only)
    lchi = parse_gff(gff_lchi, chr_prefix='chr')
    ltu = parse_gff(gff_ltu, chr_prefix='Chr')

    print()

    # Save gene tables
    lchi.to_csv(os.path.join(OUTDIR, 'lchi_genes.csv'), index=False)
    ltu.to_csv(os.path.join(OUTDIR, 'ltu_genes.csv'), index=False)
    print(f"Gene tables saved to {OUTDIR}/")

    # Generate plots
    prefix = os.path.join(OUTDIR, 'analysis')
    plot_gene_comparison(lchi, ltu, prefix)
    plot_gene_density(lchi, ltu, prefix)

    print("\n=== Gene comparison analysis complete ===")


if __name__ == '__main__':
    main()
