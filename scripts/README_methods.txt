========================================================================
  中国鹅掌楸 (Liriodendron chinense) vs 北美鹅掌楸 (L. tulipifera)
  比较基因组分析 -- 方法说明与流程文档
========================================================================

一、研究背景
------------------------------------------------------------------------
鹅掌楸属 (Liriodendron) 是木兰科的孑遗属，现存仅两个种：中国鹅掌楸
(L. chinense, 2n=38) 和北美鹅掌楸 (L. tulipifera, 2n=38)。两者在第三纪
由共同祖先分化而来，分别分布于东亚和北美东部，构成经典的东亚-北美间断
分布格局。本分析基于两物种的染色体级别基因组组装，利用全基因组比对和
结构变异检测，系统解析两物种间的基因组共线性、倒位、易位、重复等结构
变异，以及SNP/InDel等小变异。


二、分析流程
------------------------------------------------------------------------

  Step 0: 染色体方向校正 (fix_orientation.py)
  ──────────────────────────────────────────────
  由于两个物种的基因组独立组装，染色体序列的方向（正链/负链）可能不一致。
  初次运行 SyRI 时发现 19 条染色体中有 13 条在 query 基因组 (L. tulipifera)
  中的比对方向与 reference (L. chinense) 相反，导致 SyRI 分析失败。

  解决方法：对 L. tulipifera 基因组中方向不一致的 13 条染色体 (Chr03,
  Chr06, Chr07, Chr09, Chr10, Chr11, Chr12, Chr13, Chr14, Chr15, Chr17,
  Chr18, Chr19) 进行反向互补 (reverse complement) 处理，生成方向校正后的
  基因组文件 Ltu.chr_only.oriented.fasta。

  脚本：fix_orientation.py


  Step 1: 全基因组比对 (minimap2)
  ──────────────────────────────────────────────
  使用 minimap2 v2.24 进行全基因组比对，参数如下：

    minimap2 -ax asm5 --eqx -t 100 \
        Lchi.chr_only.fasta \
        Ltu.chr_only.oriented.fasta

  参数说明：
    -ax asm5    组装比对模式，适用于序列相似度 >95% 的近缘物种比较
    --eqx       在 CIGAR 中使用 =/X 区分匹配和错配（SyRI 要求）
    -t 100      使用 100 个线程并行加速

  比对结果通过管道直接传入 samtools sort 进行坐标排序，生成排序后的
  BAM 文件 (23 GB)，并用 samtools index 建立索引。


  Step 2: 结构变异检测 (SyRI v1.6.3)
  ──────────────────────────────────────────────
  使用 SyRI (Synteny and Rearrangement Identifier) v1.6.3 进行全基因组
  结构变异检测：

    syri -c lchi_vs_ltu_oriented.sorted.bam \
         -r Lchi.chr_only.fasta \
         -q Ltu.chr_only.oriented.fasta \
         -k -F B

  参数说明：
    -c          输入为 BAM 格式的比对文件
    -r / -q     参考基因组和查询基因组
    -k          保留中间文件（synOut.txt, invOut.txt, TLOut.txt 等）
    -F B        输入格式为 BAM

  SyRI 自动匹配两个基因组的染色体对应关系 (mapids.txt)，然后依次检测：
  (1) 共线性区域 (Synteny)
  (2) 倒位 (Inversions)
  (3) 易位和重复 (Translocations & Duplications)
  (4) 结构变异内部的小变异 (SNPs, InDels)

  输出文件：syri.out (754 MB), syri.vcf (1.3 GB)


  Step 3: 共线性可视化 (plotsr)
  ──────────────────────────────────────────────
  使用 plotsr 工具基于 SyRI 输出绘制全基因组共线性图：

    plotsr --sr syri.out --genomes genomes.txt \
           -o plotsr_synteny.png -W 14 -H 8 -f 10 -d 300

  生成 PNG 和 PDF 两种格式的出版级共线性图。图中以不同颜色表示共线性
  区域（灰色）、倒位（橙色）、易位（蓝色）、重复（绿色）等。


  Step 4: 结构变异统计分析 (parse_syri_results.py)
  ──────────────────────────────────────────────
  自定义 Python 脚本解析 syri.out，生成：
  - 结构变异类型统计柱状图 (analysis_sv_stats.png)
  - 结构变异大小分布图 (analysis_sv_sizes.png)
  - SNP 密度热图 (analysis_snp_density.png)
  - 染色体共线性图 (analysis_chr_synteny.png)
  - 完整文本报告 (analysis_report.txt)
  - 解析后的 CSV 数据表 (syri_parsed.csv)

  脚本：parse_syri_results.py


  Step 5: 基因结构比较 (gene_comparison_v2.py)
  ──────────────────────────────────────────────
  解析两物种的 GFF 基因注释文件，比较：
  - 基因数目、平均基因长度
  - 外显子数目分布
  - CDS 长度分布
  - 各染色体上的基因密度

  输出：
  - 基因结构比较图 (analysis_gene_comparison.png)
  - 基因密度比较图 (analysis_gene_density.png)
  - 基因数据表 (lchi_genes.csv, ltu_genes.csv)

  脚本：gene_comparison_v2.py


三、主要结果
------------------------------------------------------------------------

  1. 基因组共线性
     两物种间共检测到 78,423 个共线性区块，总长度 975.4 Mb，表明两者
     在基因组水平上高度保守。19 条染色体全部实现一一对应。

  2. 结构变异
     - 倒位 (Inversions):    11,892 个，总长 340.7 Mb，最大倒位 29.2 Mb
     - 易位 (Translocations): 11,176 个，总长  62.2 Mb
     - 重复 (Duplications):    3,932 个，总长  27.0 Mb
     - 倒位易位:               3,445 个，总长  37.6 Mb
     - 倒位重复:               3,062 个，总长  15.6 Mb
     - 未比对区域:            24,774 个，总长 356.4 Mb

  3. 小变异
     - SNPs:    9,113,623 个
     - 插入:      448,372 个
     - 缺失:      504,963 个，平均长度 9 bp

  4. 染色体对应关系
     chr1↔Chr01, chr2↔Chr02, chr3↔Chr03, chr4↔Chr04, chr5↔Chr11,
     chr6↔Chr15, chr7↔Chr09, chr8↔Chr05, chr9↔Chr18, chr10↔Chr13,
     chr11↔Chr16, chr12↔Chr06, chr13↔Chr19, chr14↔Chr14, chr15↔Chr08,
     chr16↔Chr17, chr17↔Chr12, chr18↔Chr07, chr19↔Chr10

     注：仅 chr1-chr4 和 chr14 编号一致，其余 14 条染色体编号不同，
     反映了两物种独立组装和命名的差异。


四、软件版本
------------------------------------------------------------------------
  - minimap2     v2.24-r1122
  - samtools     (syri env)
  - SyRI         v1.6.3
  - plotsr       (syri env)
  - Python       3.8.15 (syri conda env)
  - pandas, matplotlib, seaborn, numpy


五、文件清单
------------------------------------------------------------------------

  scripts/                              分析脚本目录
  ├── fix_orientation.py                染色体方向校正脚本
  ├── run_full_fixed.sh                 完整分析流水线 (主脚本)
  ├── parse_syri_results.py             SyRI 结果解析与统计可视化
  └── gene_comparison_v2.py             基因结构比较分析

  syri_output/                          分析结果目录
  ├── lchi_vs_ltu_oriented.sorted.bam   minimap2 比对结果 (23 GB)
  ├── lchi_vs_ltu_oriented.sorted.bam.bai  BAM 索引
  ├── syri.out                          SyRI 主输出 (754 MB)
  ├── syri.vcf                          VCF 格式输出 (1.3 GB)
  ├── syri.log                          SyRI 运行日志
  ├── mapids.txt                        染色体对应关系表
  ├── synOut.txt                        共线性区块
  ├── invOut.txt                        倒位区块
  ├── TLOut.txt                         易位区块
  ├── dupOut.txt                        重复区块
  ├── invTLOut.txt                      倒位易位
  ├── invDupOut.txt                     倒位重复
  ├── ctxOut.txt                        跨染色体易位
  ├── notAligned.txt                    未比对区域
  ├── snps.txt                          SNPs 数据 (708 MB)
  ├── sv.txt                            结构变异数据 (1.5 GB)
  ├── plotsr_synteny.png                全基因组共线性图 (plotsr)
  ├── plotsr_synteny.pdf                共线性图 PDF 版
  ├── analysis_sv_stats.png             结构变异统计柱状图
  ├── analysis_sv_sizes.png             结构变异大小分布
  ├── analysis_snp_density.png          SNP 密度热图
  ├── analysis_chr_synteny.png          染色体共线性图
  ├── analysis_gene_comparison.png      基因结构比较图
  ├── analysis_gene_density.png         基因密度比较图
  ├── analysis_report.txt               完整统计报告
  ├── syri_parsed.csv                   解析后结构变异表
  ├── lchi_genes.csv                    中国鹅掌楸基因数据
  └── ltu_genes.csv                     北美鹅掌楸基因数据

========================================================================
