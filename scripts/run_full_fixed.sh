#!/bin/bash
set -e

WORKDIR=/data/hongky_data/comparative_genomics3
OUTDIR=${WORKDIR}/syri_output
SYRI_BIN=/home/hongky/micromamba/envs/syri/bin
PYTHON=${SYRI_BIN}/python

REF=${WORKDIR}/Lchi.chr_only.fasta
QRY_ORIG=${WORKDIR}/Ltu.chr_only.fasta
QRY=${WORKDIR}/Ltu.chr_only.oriented.fasta

THREADS=100

echo "============================================================"
echo "  Lchi vs Ltu - Full re-run with orientation fix"
echo "============================================================"
date
echo ""

# Step 0: Fix chromosome orientation
echo ">>> Step 0: Fix Ltu chromosome orientation"
${PYTHON} ${WORKDIR}/fix_orientation.py 2>&1
ls -lh ${QRY}
date
echo ""

# Clean previous SyRI output (keep BAM for reference)
rm -f ${OUTDIR}/syri.out ${OUTDIR}/syri.vcf ${OUTDIR}/syri.log ${OUTDIR}/mapids.txt
rm -f ${OUTDIR}/*.png ${OUTDIR}/*.pdf ${OUTDIR}/*.csv ${OUTDIR}/*.txt
rm -f ${OUTDIR}/lchi_vs_ltu_oriented.*

# Step 1: minimap2 with oriented query
echo ">>> Step 1: minimap2 alignment with oriented query (${THREADS} threads)"
${SYRI_BIN}/minimap2 -ax asm5 --eqx -t ${THREADS} \
    ${REF} ${QRY} 2>${OUTDIR}/minimap2_oriented.log | \
    ${SYRI_BIN}/samtools sort -@ 16 -o ${OUTDIR}/lchi_vs_ltu_oriented.sorted.bam
${SYRI_BIN}/samtools index ${OUTDIR}/lchi_vs_ltu_oriented.sorted.bam
echo "  minimap2 done!"
ls -lh ${OUTDIR}/lchi_vs_ltu_oriented.sorted.bam
date
echo ""

# Step 2: SyRI
echo ">>> Step 2: SyRI structural variant detection"
cd ${OUTDIR}
${SYRI_BIN}/syri \
    -c ${OUTDIR}/lchi_vs_ltu_oriented.sorted.bam \
    -r ${REF} \
    -q ${QRY} \
    -k -F B 2>&1 | tail -50
echo "  SyRI done!"
ls -lh ${OUTDIR}/syri.out ${OUTDIR}/syri.vcf 2>/dev/null
date
echo ""

# Step 3: plotsr
echo ">>> Step 3: plotsr visualization"
cd ${OUTDIR}
echo -e "#file\tname\ttags" > ${OUTDIR}/genomes.txt
echo -e "${REF}\tL. chinense\tlw:1.5" >> ${OUTDIR}/genomes.txt
echo -e "${QRY}\tL. tulipifera\tlw:1.5" >> ${OUTDIR}/genomes.txt

if [ -s ${OUTDIR}/syri.out ]; then
    ${SYRI_BIN}/plotsr \
        --sr ${OUTDIR}/syri.out \
        --genomes ${OUTDIR}/genomes.txt \
        -o ${OUTDIR}/plotsr_synteny.png \
        -W 14 -H 8 -f 10 -d 300 2>&1 || echo "  plotsr PNG warning (non-fatal)"
    ${SYRI_BIN}/plotsr \
        --sr ${OUTDIR}/syri.out \
        --genomes ${OUTDIR}/genomes.txt \
        -o ${OUTDIR}/plotsr_synteny.pdf \
        -W 14 -H 8 -f 10 -d 300 2>&1 || echo "  plotsr PDF warning (non-fatal)"
    echo "  plotsr done!"
else
    echo "  WARNING: syri.out is empty or missing, skipping plotsr"
fi
date
echo ""

# Step 4: Parse SyRI results
echo ">>> Step 4: Parse SyRI results and generate statistics"
cd ${WORKDIR}
${PYTHON} ${WORKDIR}/parse_syri_results.py 2>&1
echo ""

# Step 5: Gene comparison
echo ">>> Step 5: Gene comparison analysis"
${PYTHON} ${WORKDIR}/gene_comparison_v2.py 2>&1
echo ""

echo "============================================================"
echo "  ALL ANALYSIS COMPLETE!"
echo "============================================================"
ls -lh ${OUTDIR}/*.png ${OUTDIR}/*.pdf ${OUTDIR}/*.csv ${OUTDIR}/*.txt 2>/dev/null
echo ""
date
echo "ALL_DONE"
