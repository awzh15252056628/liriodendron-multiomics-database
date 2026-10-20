#!/bin/bash
set -e

WORKDIR=/data/hongky_data/comparative_genomics3
SYRI_BIN=/home/hongky/micromamba/envs/syri/bin
PYTHON=${SYRI_BIN}/python

REF=${WORKDIR}/Lchi.chr_only.fasta
QRY_RENAMED=${WORKDIR}/Ltu.chr_only.oriented.renamed.fasta

THREADS=100

echo "============================================================"
echo "  Robustness test: Version A (default) vs Version B (strict)"
echo "============================================================"
date
echo ""

# ──────────────────────────────────────────────────────
# Step 0: Rename query chromosomes
# ──────────────────────────────────────────────────────
echo ">>> Step 0: Rename query chromosomes to match reference"
${PYTHON} ${WORKDIR}/rename_query_chroms.py 2>&1
echo ""

# ──────────────────────────────────────────────────────
# Step 1: minimap2 with renamed query
# ──────────────────────────────────────────────────────
OUTDIR_A=${WORKDIR}/syri_versionA
OUTDIR_B=${WORKDIR}/syri_versionB
mkdir -p ${OUTDIR_A} ${OUTDIR_B}

BAM=${OUTDIR_A}/lchi_vs_ltu.sorted.bam

echo ">>> Step 1: minimap2 alignment (${THREADS} threads)"
${SYRI_BIN}/minimap2 -ax asm5 --eqx -t ${THREADS} \
    ${REF} ${QRY_RENAMED} 2>${OUTDIR_A}/minimap2.log | \
    ${SYRI_BIN}/samtools sort -@ 16 -o ${BAM}
${SYRI_BIN}/samtools index ${BAM}
echo "  minimap2 + sort + index done!"
ls -lh ${BAM}
date
echo ""

# Copy BAM for version B (same alignment, different SyRI params)
ln -sf ${BAM} ${OUTDIR_B}/lchi_vs_ltu.sorted.bam
ln -sf ${BAM}.bai ${OUTDIR_B}/lchi_vs_ltu.sorted.bam.bai

# ──────────────────────────────────────────────────────
# Step 2A: SyRI Version A - default params + --no-chrmatch
# ──────────────────────────────────────────────────────
echo ">>> Step 2A: SyRI Version A (default TD params)"
cd ${OUTDIR_A}
${SYRI_BIN}/syri \
    -c ${BAM} \
    -r ${REF} \
    -q ${QRY_RENAMED} \
    -k -F B \
    --no-chrmatch \
    --lf ${OUTDIR_A}/syri.log 2>&1 | tail -20
echo "  Version A done!"
ls -lh ${OUTDIR_A}/syri.out ${OUTDIR_A}/syri.vcf 2>/dev/null
date
echo ""

# ──────────────────────────────────────────────────────
# Step 2B: SyRI Version B - conservative TD params
#   --tdgaplen  500000 -> 100000  (stricter gap tolerance)
#   --unic      1000   -> 5000    (require more unique bps)
#   --unip      (default ~0.5?) -> 0.8  (require higher uniqueness %)
#   --tdmaxolp  0.8 -> 0.5       (less overlap allowed)
# ──────────────────────────────────────────────────────
echo ">>> Step 2B: SyRI Version B (conservative TD params)"
cd ${OUTDIR_B}
${SYRI_BIN}/syri \
    -c ${BAM} \
    -r ${REF} \
    -q ${QRY_RENAMED} \
    -k -F B \
    --no-chrmatch \
    --tdgaplen 100000 \
    --unic 5000 \
    --unip 0.8 \
    --tdmaxolp 0.5 \
    --lf ${OUTDIR_B}/syri.log 2>&1 | tail -20
echo "  Version B done!"
ls -lh ${OUTDIR_B}/syri.out ${OUTDIR_B}/syri.vcf 2>/dev/null
date
echo ""

# ──────────────────────────────────────────────────────
# Step 3: plotsr for both versions
# ──────────────────────────────────────────────────────
echo ">>> Step 3A: plotsr Version A"
cd ${OUTDIR_A}
echo -e "#file\tname\ttags" > ${OUTDIR_A}/genomes.txt
echo -e "${REF}\tL. chinense\tlw:1.5" >> ${OUTDIR_A}/genomes.txt
echo -e "${QRY_RENAMED}\tL. tulipifera\tlw:1.5" >> ${OUTDIR_A}/genomes.txt

if [ -s ${OUTDIR_A}/syri.out ]; then
    ${SYRI_BIN}/plotsr \
        --sr ${OUTDIR_A}/syri.out \
        --genomes ${OUTDIR_A}/genomes.txt \
        -o ${OUTDIR_A}/plotsr_synteny.png \
        -W 14 -H 8 -f 10 -d 300 2>&1 || echo "  plotsr A PNG warning"
    ${SYRI_BIN}/plotsr \
        --sr ${OUTDIR_A}/syri.out \
        --genomes ${OUTDIR_A}/genomes.txt \
        -o ${OUTDIR_A}/plotsr_synteny.pdf \
        -W 14 -H 8 -f 10 -d 300 2>&1 || echo "  plotsr A PDF warning"
fi
echo ""

echo ">>> Step 3B: plotsr Version B"
cd ${OUTDIR_B}
cp ${OUTDIR_A}/genomes.txt ${OUTDIR_B}/genomes.txt

if [ -s ${OUTDIR_B}/syri.out ]; then
    ${SYRI_BIN}/plotsr \
        --sr ${OUTDIR_B}/syri.out \
        --genomes ${OUTDIR_B}/genomes.txt \
        -o ${OUTDIR_B}/plotsr_synteny.png \
        -W 14 -H 8 -f 10 -d 300 2>&1 || echo "  plotsr B PNG warning"
    ${SYRI_BIN}/plotsr \
        --sr ${OUTDIR_B}/syri.out \
        --genomes ${OUTDIR_B}/genomes.txt \
        -o ${OUTDIR_B}/plotsr_synteny.pdf \
        -W 14 -H 8 -f 10 -d 300 2>&1 || echo "  plotsr B PDF warning"
fi
echo ""

# ──────────────────────────────────────────────────────
# Step 4: Compare two versions
# ──────────────────────────────────────────────────────
echo ">>> Step 4: Comparing Version A vs Version B"
${PYTHON} ${WORKDIR}/compare_versions.py 2>&1
echo ""

echo "============================================================"
echo "  ALL DONE!"
echo "============================================================"
echo ""
echo "Version A (default): ${OUTDIR_A}/"
echo "Version B (strict):  ${OUTDIR_B}/"
ls -lh ${OUTDIR_A}/*.png ${OUTDIR_B}/*.png 2>/dev/null
date
echo "ALL_DONE"
