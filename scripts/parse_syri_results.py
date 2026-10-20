#!/usr/bin/env python3
"""
Parse SyRI output and generate comprehensive statistics report
for Liriodendron chinense vs L. tulipifera comparative genomics
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from datetime import datetime
import os

OUTDIR = '/data/hongky_data/comparative_genomics3/syri_output'

# Try to use Chinese font, fallback to DejaVu Sans
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def parse_syri_out(syri_file):
    """Parse syri.out file"""
    print(f"Parsing {syri_file}")

    records = []
    with open(syri_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 11:
                records.append({
                    'ref_chr': parts[0],
                    'ref_start': int(parts[1]) if parts[1] != '-' else 0,
                    'ref_end': int(parts[2]) if parts[2] != '-' else 0,
                    'qry_chr': parts[5],
                    'qry_start': int(parts[6]) if parts[6] != '-' else 0,
                    'qry_end': int(parts[7]) if parts[7] != '-' else 0,
                    'id': parts[8] if len(parts) > 8 else '',
                    'parent': parts[9] if len(parts) > 9 else '',
                    'type': parts[10] if len(parts) > 10 else '',
                })

    df = pd.DataFrame(records)
    df['ref_len'] = (df['ref_end'] - df['ref_start']).abs()
    df['qry_len'] = (df['qry_end'] - df['qry_start']).abs()
    print(f"  Total records: {len(df)}")
    return df


def generate_summary_stats(df):
    """Generate summary statistics"""
    stats = {}

    # Structural variant types
    sv_types = {
        'SYN': 'Syntenic regions',
        'INV': 'Inversions',
        'TRANS': 'Translocations',
        'DUP': 'Duplications',
        'INVTR': 'Inverted translocations',
        'INVDP': 'Inverted duplications',
        'NOTAL': 'Not aligned (ref)',
        'NOTAQ': 'Not aligned (qry)',
        'SNP': 'SNPs',
        'INS': 'Insertions',
        'DEL': 'Deletions',
        'CPG': 'Copy gain',
        'CPL': 'Copy loss',
        'HDR': 'Highly diverged regions',
        'TDM': 'Tandem repeats',
    }

    # Main structural categories (parent-level)
    main_types = ['SYNAL', 'INVAL', 'TRANSAL', 'DUPAL', 'INVTRAL', 'INVDPAL']
    sub_types = ['SYN', 'INV', 'TRANS', 'DUP', 'INVTR', 'INVDP']

    for sv_type in df['type'].unique():
        subset = df[df['type'] == sv_type]
        stats[sv_type] = {
            'count': len(subset),
            'total_ref_len': subset['ref_len'].sum(),
            'total_qry_len': subset['qry_len'].sum(),
            'mean_ref_len': subset['ref_len'].mean() if len(subset) > 0 else 0,
        }

    return stats, sv_types


def plot_structural_variants(df, output_prefix):
    """Plot structural variant statistics"""
    print("Plotting structural variant statistics...")

    # Filter to main structural types
    main_types = ['SYNAL', 'INVAL', 'TRANSAL', 'DUPAL', 'INVTRAL', 'INVDPAL']
    labels_map = {
        'SYNAL': 'Synteny',
        'INVAL': 'Inversion',
        'TRANSAL': 'Translocation',
        'DUPAL': 'Duplication',
        'INVTRAL': 'Inv. Transloc.',
        'INVDPAL': 'Inv. Duplication',
    }

    type_data = []
    for t in main_types:
        subset = df[df['type'] == t]
        if len(subset) > 0:
            type_data.append({
                'type': labels_map.get(t, t),
                'count': len(subset),
                'total_len_mb': subset['ref_len'].sum() / 1e6,
            })

    if not type_data:
        # Try sub-types
        sub_types = ['SYN', 'INV', 'TRANS', 'DUP', 'INVTR', 'INVDP']
        for t in sub_types:
            subset = df[df['type'] == t]
            if len(subset) > 0:
                type_data.append({
                    'type': t,
                    'count': len(subset),
                    'total_len_mb': subset['ref_len'].sum() / 1e6,
                })

    if not type_data:
        print("  No structural variant data to plot")
        return

    type_df = pd.DataFrame(type_data)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # 1. Count bar chart
    colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']
    ax = axes[0]
    bars = ax.barh(type_df['type'], type_df['count'], color=colors[:len(type_df)])
    ax.set_xlabel('Count', fontsize=12)
    ax.set_title('Structural Variant Counts', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    for bar, val in zip(bars, type_df['count']):
        ax.text(bar.get_width() + max(type_df['count']) * 0.01, bar.get_y() + bar.get_height()/2,
                f'{val:,}', va='center', fontsize=10)

    # 2. Total length bar chart
    ax = axes[1]
    bars = ax.barh(type_df['type'], type_df['total_len_mb'], color=colors[:len(type_df)])
    ax.set_xlabel('Total Length (Mb)', fontsize=12)
    ax.set_title('Structural Variant Span', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    for bar, val in zip(bars, type_df['total_len_mb']):
        ax.text(bar.get_width() + max(type_df['total_len_mb']) * 0.01, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}', va='center', fontsize=10)

    # 3. Pie chart of genome composition
    ax = axes[2]
    ax.pie(type_df['total_len_mb'], labels=type_df['type'], autopct='%1.1f%%',
           colors=colors[:len(type_df)], startangle=90)
    ax.set_title('Genome Composition', fontsize=13, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{output_prefix}_sv_stats.png', dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_prefix}_sv_stats.png")
    plt.close()


def plot_chromosome_synteny(df, output_prefix):
    """Plot per-chromosome synteny breakdown"""
    print("Plotting chromosome synteny breakdown...")

    main_types = ['SYNAL', 'INVAL', 'TRANSAL', 'DUPAL', 'INVTRAL', 'INVDPAL']
    colors_map = {
        'SYNAL': '#2ecc71',
        'INVAL': '#e74c3c',
        'TRANSAL': '#3498db',
        'DUPAL': '#f39c12',
        'INVTRAL': '#9b59b6',
        'INVDPAL': '#1abc9c',
    }

    # If no SYNAL, try SYN etc.
    if df[df['type'].isin(main_types)].empty:
        main_types = ['SYN', 'INV', 'TRANS', 'DUP', 'INVTR', 'INVDP']
        colors_map = {
            'SYN': '#2ecc71', 'INV': '#e74c3c', 'TRANS': '#3498db',
            'DUP': '#f39c12', 'INVTR': '#9b59b6', 'INVDP': '#1abc9c',
        }

    sv_df = df[df['type'].isin(main_types)]
    if sv_df.empty:
        print("  No chromosome synteny data")
        return

    chr_order = sorted(sv_df['ref_chr'].unique())

    fig, ax = plt.subplots(figsize=(14, 8))

    chr_sv_data = {}
    for chr_name in chr_order:
        chr_data = sv_df[sv_df['ref_chr'] == chr_name]
        chr_sv_data[chr_name] = {}
        for t in main_types:
            t_data = chr_data[chr_data['type'] == t]
            chr_sv_data[chr_name][t] = t_data['ref_len'].sum() / 1e6

    x = np.arange(len(chr_order))
    bottom = np.zeros(len(chr_order))

    for t in main_types:
        vals = [chr_sv_data[c].get(t, 0) for c in chr_order]
        if sum(vals) > 0:
            ax.bar(x, vals, bottom=bottom, label=t, color=colors_map.get(t, 'gray'), alpha=0.8)
            bottom += np.array(vals)

    ax.set_xticks(x)
    ax.set_xticklabels(chr_order, rotation=45, ha='right')
    ax.set_xlabel('Chromosome (L. chinense)', fontsize=12)
    ax.set_ylabel('Length (Mb)', fontsize=12)
    ax.set_title('Chromosome-level Structural Composition\nL. chinense vs L. tulipifera', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(f'{output_prefix}_chr_synteny.png', dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_prefix}_chr_synteny.png")
    plt.close()


def plot_sv_size_distribution(df, output_prefix):
    """Plot size distribution of structural variants"""
    print("Plotting SV size distributions...")

    sv_types_to_plot = ['INV', 'TRANS', 'DUP', 'INVTR', 'INVDP',
                        'INVAL', 'TRANSAL', 'DUPAL', 'INVTRAL', 'INVDPAL']
    sv_df = df[df['type'].isin(sv_types_to_plot)]
    sv_df = sv_df[sv_df['ref_len'] > 0]

    if sv_df.empty:
        print("  No SV size data")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Log-scale histogram
    ax = axes[0]
    for sv_type in sv_df['type'].unique():
        data = sv_df[sv_df['type'] == sv_type]['ref_len']
        if len(data) > 5:
            ax.hist(np.log10(data + 1), bins=30, alpha=0.5, label=sv_type)
    ax.set_xlabel('log10(Length)', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('SV Size Distribution', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Box plot
    ax = axes[1]
    plot_data = []
    plot_labels = []
    for sv_type in sorted(sv_df['type'].unique()):
        data = sv_df[sv_df['type'] == sv_type]['ref_len']
        if len(data) > 0:
            plot_data.append(np.log10(data + 1))
            plot_labels.append(sv_type)

    if plot_data:
        bp = ax.boxplot(plot_data, labels=plot_labels, patch_artist=True)
        colors = plt.cm.Set2(np.linspace(0, 1, len(plot_data)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        ax.set_ylabel('log10(Length)', fontsize=12)
        ax.set_title('SV Size by Type', fontsize=13, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(f'{output_prefix}_sv_sizes.png', dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_prefix}_sv_sizes.png")
    plt.close()


def plot_snp_indel_density(df, output_prefix, window=1000000):
    """Plot SNP/InDel density along chromosomes"""
    print("Plotting SNP/InDel density...")

    snp_df = df[df['type'] == 'SNP']
    ins_df = df[df['type'] == 'INS']
    del_df = df[df['type'] == 'DEL']

    if snp_df.empty and ins_df.empty and del_df.empty:
        print("  No SNP/InDel data")
        return

    chromosomes = sorted(snp_df['ref_chr'].unique()) if not snp_df.empty else []
    if not chromosomes:
        return

    n_chr = len(chromosomes)
    fig, axes = plt.subplots(min(n_chr, 19), 1, figsize=(14, min(n_chr, 19) * 1.5), sharex=False)
    if min(n_chr, 19) == 1:
        axes = [axes]

    for idx, chr_name in enumerate(chromosomes[:19]):
        ax = axes[idx]
        chr_snps = snp_df[snp_df['ref_chr'] == chr_name]
        chr_ins = ins_df[ins_df['ref_chr'] == chr_name]
        chr_del = del_df[del_df['ref_chr'] == chr_name]

        max_pos = max(
            chr_snps['ref_end'].max() if not chr_snps.empty else 0,
            chr_ins['ref_end'].max() if not chr_ins.empty else 0,
            chr_del['ref_end'].max() if not chr_del.empty else 0,
        )

        windows = range(0, int(max_pos) + window, window)
        snp_counts = []
        indel_counts = []

        for w_start in windows:
            w_end = w_start + window
            n_snp = len(chr_snps[(chr_snps['ref_start'] >= w_start) & (chr_snps['ref_start'] < w_end)])
            n_indel = len(chr_ins[(chr_ins['ref_start'] >= w_start) & (chr_ins['ref_start'] < w_end)]) + \
                      len(chr_del[(chr_del['ref_start'] >= w_start) & (chr_del['ref_start'] < w_end)])
            snp_counts.append(n_snp)
            indel_counts.append(n_indel)

        positions = [w / 1e6 for w in windows]
        ax.fill_between(positions, snp_counts, alpha=0.5, color='blue', label='SNP')
        ax.fill_between(positions, indel_counts, alpha=0.5, color='red', label='InDel')
        ax.set_ylabel(chr_name, fontsize=8, rotation=0, ha='right')
        ax.tick_params(axis='y', labelsize=7)
        if idx == 0:
            ax.legend(loc='upper right', fontsize=8)
        if idx < len(chromosomes) - 1:
            ax.set_xticklabels([])

    axes[-1].set_xlabel('Position (Mb)', fontsize=12)
    fig.suptitle('SNP & InDel Density Along Chromosomes\nL. chinense vs L. tulipifera',
                 fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_snp_density.png', dpi=300, bbox_inches='tight')
    print(f"  Saved: {output_prefix}_snp_density.png")
    plt.close()


def generate_report(df, stats, sv_types, output_file):
    """Generate text report"""
    print(f"Generating report: {output_file}")

    lines = []
    lines.append("=" * 72)
    lines.append("  Liriodendron chinense vs L. tulipifera")
    lines.append("  Comparative Genomics Analysis Report")
    lines.append("  (minimap2 + SyRI)")
    lines.append("=" * 72)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # 1. Overview
    lines.append("1. ANALYSIS OVERVIEW")
    lines.append("-" * 72)
    lines.append("  Reference: L. chinense (Lchi) - 19 chromosomes")
    lines.append("  Query:     L. tulipifera (Ltu) - 19 chromosomes")
    lines.append("  Aligner:   minimap2 (asm5 mode)")
    lines.append("  SV caller: SyRI v1.6.3")
    lines.append("")

    # 2. Structural variant summary
    lines.append("2. STRUCTURAL VARIANT SUMMARY")
    lines.append("-" * 72)
    lines.append(f"  {'Type':<25s} {'Count':>10s} {'Total Len (bp)':>18s} {'Mean Len (bp)':>16s}")
    lines.append("  " + "-" * 69)

    # Group by major categories
    for sv_type in sorted(stats.keys()):
        s = stats[sv_type]
        label = sv_types.get(sv_type, sv_type)
        lines.append(f"  {sv_type:<8s} {label:<16s} {s['count']:>10,d} "
                     f"{s['total_ref_len']:>18,.0f} {s['mean_ref_len']:>16,.0f}")
    lines.append("")

    # 3. Synteny
    syn_types = ['SYNAL', 'SYN']
    syn_df = df[df['type'].isin(syn_types)]
    total_syn = syn_df['ref_len'].sum()
    lines.append("3. SYNTENY STATISTICS")
    lines.append("-" * 72)
    lines.append(f"  Total syntenic regions: {len(syn_df):,}")
    lines.append(f"  Total syntenic length:  {total_syn:,.0f} bp ({total_syn/1e6:.1f} Mb)")
    lines.append("")

    # 4. Inversions
    inv_types = ['INVAL', 'INV']
    inv_df = df[df['type'].isin(inv_types)]
    total_inv = inv_df['ref_len'].sum()
    lines.append("4. INVERSION STATISTICS")
    lines.append("-" * 72)
    lines.append(f"  Total inversions:      {len(inv_df):,}")
    lines.append(f"  Total inverted length: {total_inv:,.0f} bp ({total_inv/1e6:.1f} Mb)")
    if not inv_df.empty:
        lines.append(f"  Largest inversion:     {inv_df['ref_len'].max():,.0f} bp")
        lines.append(f"  Mean inversion size:   {inv_df['ref_len'].mean():,.0f} bp")
        lines.append("")
        lines.append("  Inversions by chromosome:")
        for chr_name in sorted(inv_df['ref_chr'].unique()):
            chr_inv = inv_df[inv_df['ref_chr'] == chr_name]
            lines.append(f"    {chr_name}: {len(chr_inv)} inversions, "
                        f"total {chr_inv['ref_len'].sum():,.0f} bp")
    lines.append("")

    # 5. Translocations
    trans_types = ['TRANSAL', 'TRANS']
    trans_df = df[df['type'].isin(trans_types)]
    total_trans = trans_df['ref_len'].sum()
    lines.append("5. TRANSLOCATION STATISTICS")
    lines.append("-" * 72)
    lines.append(f"  Total translocations:     {len(trans_df):,}")
    lines.append(f"  Total translocated length: {total_trans:,.0f} bp ({total_trans/1e6:.1f} Mb)")
    lines.append("")

    # 6. SNPs and InDels
    snp_df = df[df['type'] == 'SNP']
    ins_df = df[df['type'] == 'INS']
    del_df = df[df['type'] == 'DEL']
    lines.append("6. SMALL VARIANTS (SNPs & InDels)")
    lines.append("-" * 72)
    lines.append(f"  SNPs:       {len(snp_df):,}")
    lines.append(f"  Insertions: {len(ins_df):,}")
    lines.append(f"  Deletions:  {len(del_df):,}")
    if not ins_df.empty:
        lines.append(f"  Mean insertion size: {ins_df['ref_len'].mean():,.0f} bp")
    if not del_df.empty:
        lines.append(f"  Mean deletion size:  {del_df['ref_len'].mean():,.0f} bp")
    lines.append("")

    # 7. Chromosome pairing
    lines.append("7. CHROMOSOME CORRESPONDENCE")
    lines.append("-" * 72)
    syn_df2 = df[df['type'].isin(['SYNAL', 'SYN'])]
    if not syn_df2.empty:
        pairs = syn_df2.groupby(['ref_chr', 'qry_chr']).agg(
            total_len=('ref_len', 'sum'),
            count=('ref_len', 'count')
        ).reset_index().sort_values('total_len', ascending=False)

        main_pairs = pairs.groupby('ref_chr').first().reset_index().sort_values('ref_chr')
        for _, row in main_pairs.iterrows():
            lines.append(f"  {row['ref_chr']:>8s}  <-->  {row['qry_chr']:<8s}  "
                        f"({row['count']:>4d} blocks, {row['total_len']/1e6:>8.2f} Mb)")
    lines.append("")

    lines.append("=" * 72)
    lines.append("  Report End")
    lines.append("=" * 72)

    report_text = '\n'.join(lines)
    print(report_text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"\nReport saved to: {output_file}")


def main():
    syri_file = os.path.join(OUTDIR, 'syri.out')

    if not os.path.exists(syri_file):
        print(f"ERROR: {syri_file} not found")
        return

    # Parse SyRI output
    df = parse_syri_out(syri_file)

    print(f"\nSyRI output type distribution:")
    print(df['type'].value_counts().to_string())
    print()

    # Generate statistics
    stats, sv_types = generate_summary_stats(df)

    # Save parsed data
    df.to_csv(os.path.join(OUTDIR, 'syri_parsed.csv'), index=False)
    print(f"Parsed data saved to: {OUTDIR}/syri_parsed.csv\n")

    # Generate plots
    prefix = os.path.join(OUTDIR, 'analysis')
    plot_structural_variants(df, prefix)
    plot_chromosome_synteny(df, prefix)
    plot_sv_size_distribution(df, prefix)
    plot_snp_indel_density(df, prefix)

    # Generate report
    generate_report(df, stats, sv_types, os.path.join(OUTDIR, 'analysis_report.txt'))

    print("\n=== All statistics and plots generated ===")


if __name__ == '__main__':
    main()
