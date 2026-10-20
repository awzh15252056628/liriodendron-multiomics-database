# 鹅掌楸多组学数据库 GitHub Pages 版（v3.1）

这是可上传到 GitHub / GitHub Pages 的静态网页文件夹。入口文件是 `index.html`。

## 页面模块层级

- Home：数据库概览和四大组学入口
- Species：物种信息、参考组装、分布记录与标本数据
- Omics Data：Genomics、Transcriptomics、Proteomics、Metabolomics
- Analysis Tools：按 Sequence & Protein、Genome & Variation、Expression & Regulation、Breeding & Ploidy、Metabolism & Traits 分类
- Resources：外部数据库检索、核心文献和 Download Center

原来混合展示的 Featured modules 已移除；NCBI 运行记录仅在 Genomics → Resequencing Data 和 Transcriptomics 中显示；面向部署者的内部数据目录说明不再出现在用户页面。

## 已接入内容

- 主数据库页面：`index.html`
- “Omics Data” 以四个醒目的平级入口展示：Genomics、Transcriptomics、Proteomics、Metabolomics
- Genomics 下设 Genome Resources、Resequencing Data、Comparative Genomics 三个醒目的二级模块
- Genome Resources 明确展示两个染色体水平参考基因组：中国鹅掌楸（Liriodendron chinense v2.1）和北美鹅掌楸（Liriodendron tulipifera YP108A_766 v1.0）
- 两个参考基因组均提供本地 GFF 注释和蛋白质 FASTA；因 GitHub 文件大小限制未纳入的完整组装文件记录在 `EXCLUDED_LARGE_FILES.tsv`
- Transcriptomics 已收录完整目录：25 个 NCBI BioProject、379 条 RNA 相关 SRA 记录及 1 项无 SRA 编号的公开转录组–蛋白组研究
- 其中 6 套表达矩阵可直接进入 Expression Atlas（135 个文库、45 个条件分组、35,269 个基因）
- 可下载项目清单：`data/transcriptomics/transcriptome_projects.tsv`
- “Omics Data” 内的蛋白质组与代谢组详细目录：`multiomics.html`
- 公开组学结构化目录：`data/omics/omics_catalog.js`
- 中文完整下载清单：`data/omics/鹅掌楸公开蛋白质组与代谢组下载清单.md`
- 群体 SNP 分析页面：`snp-analysis.html`
- SNP 小结果表：`data/snp/`
- 本地依赖：React、Tailwind、Chart.js、Leaflet、Lucide 等已放在同一文件夹内

## 新增蛋白质组与代谢组资源

- 13 项公开研究：6 项蛋白质组学、7 项代谢组学
- 4 个 MassIVE/GNPS 公开质谱项目
- 79 个鹅掌楸样品及配套质控文件的文件级下载链接
- 约 15.65 GB 原始/转换质谱数据的外部索引
- 37 个论文补充表或公开数据包入口
- 按物种、组学类型、分析平台和公开数据层级检索

原始质谱文件体积较大，未重复放入 GitHub 包；网站保存的是经过筛选的项目元数据和永久下载入口。部分浏览器不支持 FTP，可复制链接到 FileZilla、WinSCP 等 FTPES 客户端。

## SNP 筛选阈值

- biallelic SNP
- MAF >= 0.05
- F_MISSING <= 0.05
- LD pruning: `--indep-pairwise 50 5 0.2`

## 上传方式

把本文件夹里的全部内容上传到 GitHub 仓库根目录，然后在 GitHub Pages 里选择该分支即可。请保持 `data/omics/` 与 `multiomics.html` 的相对路径不变。

## 未包含的大文件

为避免 GitHub 上传失败，超过约 24MB 的超大数据文件没有放进这个上传版。详见 `EXCLUDED_LARGE_FILES.tsv`。
