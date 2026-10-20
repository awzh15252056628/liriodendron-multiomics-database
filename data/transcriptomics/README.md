# LMDB transcriptomics catalog

The Transcriptomics module is generated from the complete RNA-related subset of the 682-run NCBI table embedded in `index.html`.

- 25 NCBI BioProjects
- 379 public run records: 357 RNA-Seq, 12 miRNA-Seq and 10 EST
- 1 additional processed diploid–tetraploid transcriptome–proteome study
- 6 projects with integrated expression matrices in `gene_expression_explorer.html`
- 135 expression libraries, 45 condition groups and 35,269 genes in the Expression Atlas

The project-level inventory is available in `transcriptome_projects.tsv`. BioProject and SRA links in the website point to the external NCBI records; raw FASTQ files are not duplicated inside the GitHub package.

Expression Atlas projects: PRJNA559687, PRJNA780974, PRJNA1177383, PRJNA679089, PRJNA679101 and PRJNA761222.
