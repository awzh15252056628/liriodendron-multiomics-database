# LMDB 蛋白质组与代谢组公开数据目录

更新日期：2026-08-19

本目录为鹅掌楸多组学数据库的公开蛋白质组学与代谢组学数据层。网站不重复托管约 15.65 GB 的原始质谱文件，而是保存经过人工筛选的项目元数据、论文补充数据入口和文件级永久下载链接，以便部署到 GitHub Pages。

## 文件说明

- `omics_catalog.js`：网站直接读取的结构化数据目录，包含 13 项研究、4 个 MassIVE 项目、79 个鹅掌楸相关质谱文件链接和 37 个补充数据/数据包入口。
- `鹅掌楸公开蛋白质组与代谢组下载清单.md`：中文下载说明及完整链接清单。
- 网站入口：根目录 `multiomics.html`；主站 `index.html` 的 Omics Data 页面也已接入同一份目录。

## 数据分级

1. `raw-public`：MassIVE/GNPS 中可直接访问的厂商 RAW、mzXML 或 mzML 数据。
2. `processed-public`：论文补充表、蛋白/代谢物鉴定表或公开数据包。
3. `publication-only`：研究结果可公开阅读，但本次整理未检出对应的专属公开原始质谱 accession。

## MassIVE 文件筛选规则

- `LITU` 表示 *Liriodendron tulipifera*。
- `Chin` 表示 *Liriodendron chinense*。
- 混合物种项目仅保留鹅掌楸样品及与其配套的 blank、pooled QC 和 identification 文件。
- blank、QC 和 identification 文件用于质控或谱库构建，不能作为生物学重复。

部分浏览器不再直接支持 FTP。可将链接复制到 FileZilla、WinSCP 或其他支持 FTPES 的客户端，主机为 `massive-ftp.ucsd.edu`，端口 `21`，使用 anonymous 登录。

## 论文中可用的方法描述

本数据库对公开可获得的鹅掌楸属蛋白质组学和代谢组学资源进行了系统整理。数据来源包括 MassIVE/GNPS 公共质谱数据库以及论文关联的补充材料和数据仓库，并按物种、组织、分析平台、数据层级和 accession 进行标准化。对于包含多个植物物种的 MassIVE 项目，仅纳入文件名和项目元数据显示为鹅掌楸的质谱文件，同时保留与其配套的空白、混合质控和鉴定池文件。最终形成可检索的项目级与文件级索引，为鹅掌楸蛋白质表达、代谢物组成、花器官发育、胁迫响应和菌根互作等研究提供统一的数据入口。
