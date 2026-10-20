(function () {
  'use strict';

  const species = {
    chinense: { name: 'Liriodendron chinense', shortName: 'L. chinense', labelZh: '中国鹅掌楸' },
    tulipifera: { name: 'Liriodendron tulipifera', shortName: 'L. tulipifera', labelZh: '北美鹅掌楸' },
    hybrid_2x: { name: 'Liriodendron × sinoamericanum', shortName: 'L. × sinoamericanum (2x)', labelZh: '二倍体杂交鹅掌楸' },
    hybrid_4x: { name: 'Liriodendron × sinoamericanum', shortName: 'L. × sinoamericanum (4x)', labelZh: '四倍体杂交鹅掌楸' }
  };

  const link = (name, url, kind) => ({ name, url, kind: kind || 'data' });

  const carotenoidSupplementBase = 'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41438-020-0287-3/MediaObjects/';
  const carotenoidSupplements = Array.from({ length: 17 }, (_, index) => {
    const number = index + 1;
    const extension = number <= 2 ? 'pdf' : 'xlsx';
    return link(
      `Supplementary MOESM${number} (${extension.toUpperCase()})`,
      `${carotenoidSupplementBase}41438_2020_287_MOESM${number}_ESM.${extension}`,
      'data'
    );
  });

  const tetraploidSupplements = [
    ...Array.from({ length: 5 }, (_, index) => {
      const number = index + 1;
      return link(
        `Dataset S${number} (XLSX)`,
        `https://pmc.ncbi.nlm.nih.gov/articles/instance/8498940/bin/dataset_s${number}_tpab039.xlsx`,
        'data'
      );
    }),
    ...Array.from({ length: 5 }, (_, index) => {
      const number = index + 1;
      return link(
        `Supplemental table ${number} (XLSX)`,
        `https://pmc.ncbi.nlm.nih.gov/articles/instance/8498940/bin/supplemental_table_${number}_tpab039.xlsx`,
        'data'
      );
    })
  ];

  const datasets = [
    {
      id: 'msv000097037',
      omicsType: 'metabolomics',
      speciesIds: ['chinense', 'tulipifera'],
      title: 'Twig sesquiterpene-lactone LC–MS/MS metabolome',
      titleZh: '鹅掌楸枝条倍半萜内酯 LC-MS/MS 代谢组',
      type: 'Untargeted LC–MS/MS',
      accession: 'MSV000097037',
      year: 2025,
      source: 'MassIVE / GNPS',
      doi: '10.25345/C5833N97F',
      articleDoi: '10.1021/acs.jnatprod.5c00620',
      dataLevel: 'Raw and converted spectra',
      availability: 'raw-public',
      technique: 'LC–MS/MS (LTQ XL)',
      sampleType: 'Methanolic twig extracts',
      fileCount: 14,
      size: '~1.99 GB',
      license: 'CC0 1.0',
      description: 'Public vendor RAW and mzXML files from methanolic twig extracts of L. chinense and L. tulipifera, generated to study specialization of sesquiterpene lactones in plant defense.',
      downloads: [
        link('MassIVE project', 'https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000097037', 'repository'),
        link('FTP project directory', 'ftp://massive-ftp.ucsd.edu/v09/MSV000097037/', 'repository'),
        link('FTP raw directory', 'ftp://massive-ftp.ucsd.edu/v09/MSV000097037/raw/', 'repository'),
        link('Project parameters', 'ftp://massive-ftp.ucsd.edu/v09/MSV000097037/ccms_parameters/params.xml', 'metadata'),
        link('Publication (ACS)', 'https://pubs.acs.org/doi/10.1021/acs.jnatprod.5c00620', 'article'),
        link('Publication (PMC)', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12369000/', 'article')
      ]
    },
    {
      id: 'msv000089948',
      omicsType: 'metabolomics',
      speciesIds: ['tulipifera'],
      title: 'Tulip-tree branch LC–MS/MS chemical-profile dataset',
      titleZh: '北美鹅掌楸枝条 LC-MS/MS 代谢组',
      type: 'Untargeted LC–MS/MS',
      accession: 'MSV000089948',
      year: 2022,
      source: 'MassIVE / GNPS',
      articleDoi: '10.1021/acsomega.2c03539',
      dataLevel: 'Raw and converted spectra',
      availability: 'raw-public',
      technique: 'LC–MS/MS',
      sampleType: 'Twig and branch extracts',
      fileCount: 8,
      size: '~0.71 GB',
      license: 'MassIVE public dataset',
      description: 'The MassIVE project includes Magnolia controls; the curated file view retains only Tulip-labelled L. tulipifera files and the corresponding blanks.',
      downloads: [
        link('MassIVE project', 'https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000089948', 'repository'),
        link('FTP project directory', 'ftp://massive-ftp.ucsd.edu/v04/MSV000089948/', 'repository'),
        link('FTP original raw directory', 'ftp://massive-ftp.ucsd.edu/v04/MSV000089948/raw/', 'repository'),
        link('FTP updated raw directory', 'ftp://massive-ftp.ucsd.edu/v04/MSV000089948/updates/2022-07-22_mbertin_f8ff202c/raw/', 'repository'),
        link('Project parameters', 'ftp://massive-ftp.ucsd.edu/v04/MSV000089948/ccms_parameters/params.xml', 'metadata'),
        link('Publication (ACS Omega)', 'https://pubs.acs.org/doi/10.1021/acsomega.2c03539', 'article')
      ]
    },
    {
      id: 'msv000090615',
      omicsType: 'metabolomics',
      speciesIds: ['tulipifera'],
      title: 'Mycorrhizal root and leaf UHPLC–Orbitrap–MS/MS metabolome',
      titleZh: '菌根/非菌根根与叶 UHPLC-Orbitrap-MS/MS 代谢组',
      type: 'Untargeted UHPLC–MS/MS',
      accession: 'MSV000090615',
      year: 2023,
      source: 'MassIVE / GNPS',
      doi: '10.25345/C5JH3D69S',
      articleDoi: '10.1111/1365-2745.14049',
      dataLevel: 'Converted spectra',
      availability: 'raw-public',
      technique: 'UHPLC–Orbitrap Fusion MS/MS',
      sampleType: 'Roots, leaves, blanks and pooled QC',
      fileCount: 33,
      size: '~2.29 GB',
      license: 'CC0 1.0',
      description: 'Open mzML files for mycorrhizal and non-mycorrhizal seedling root/leaf metabolomes. LITU files are L. tulipifera; JUVI_LITU files are shared blanks, pooled QC or identification mixtures.',
      downloads: [
        link('MassIVE project', 'https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000090615', 'repository'),
        link('FTP project directory', 'ftp://massive-ftp.ucsd.edu/v05/MSV000090615/', 'repository'),
        link('FTP Liriodendron data directory', 'ftp://massive-ftp.ucsd.edu/v05/MSV000090615/peak/UHPLC-Orbitrap-MS_MS/', 'repository'),
        link('Project parameters', 'ftp://massive-ftp.ucsd.edu/v05/MSV000090615/ccms_parameters/params.xml', 'metadata'),
        link('Associated publication', 'https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2745.14049', 'article')
      ]
    },
    {
      id: 'msv000090616',
      omicsType: 'metabolomics',
      speciesIds: ['tulipifera'],
      title: 'Mycorrhizal root and leaf GC–QTOF–MS primary metabolome',
      titleZh: '菌根/非菌根根与叶 GC-QTOF-MS 初生代谢组',
      type: 'GC–QTOF–MS',
      accession: 'MSV000090616',
      year: 2023,
      source: 'MassIVE / GNPS',
      doi: '10.25345/C5DR2PD64',
      articleDoi: '10.1111/1365-2745.14049',
      dataLevel: 'Converted spectra',
      availability: 'raw-public',
      technique: 'Agilent 7250 GC/Q-TOF MS',
      sampleType: 'Roots, leaves and pooled QC',
      fileCount: 24,
      size: '~10.66 GB',
      license: 'CC0 1.0',
      description: 'Open mzML files for the primary metabolome of mycorrhizal and non-mycorrhizal L. tulipifera roots and leaves, including pooled quality-control files.',
      downloads: [
        link('MassIVE project', 'https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000090616', 'repository'),
        link('FTP project directory', 'ftp://massive-ftp.ucsd.edu/v05/MSV000090616/', 'repository'),
        link('FTP Liriodendron data directory', 'ftp://massive-ftp.ucsd.edu/v05/MSV000090616/peak/QTOF-GC-MS/', 'repository'),
        link('Project parameters', 'ftp://massive-ftp.ucsd.edu/v05/MSV000090616/ccms_parameters/params.xml', 'metadata'),
        link('Associated publication', 'https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2745.14049', 'article')
      ]
    },
    {
      id: 'lchinense-pistil-proteome-2014',
      omicsType: 'proteomics',
      speciesIds: ['chinense'],
      title: 'Post-pollination pistil iTRAQ and 2-DE proteome',
      titleZh: '中国鹅掌楸授粉后雌蕊 iTRAQ/2-DE 蛋白质组',
      type: 'iTRAQ / 2-DE proteomics',
      accession: 'DOI:10.1371/journal.pone.0099970',
      year: 2014,
      source: 'PLOS ONE',
      doi: '10.1371/journal.pone.0099970',
      dataLevel: 'Processed identification tables',
      availability: 'processed-public',
      technique: 'iTRAQ, 2-DE and mass spectrometry',
      sampleType: 'Pistils before and after pollination',
      proteins: '493 differential proteins reported',
      description: 'Morphological and proteomic analysis of the L. chinense pistil after pollination. Public supporting spreadsheets contain the processed differential-protein results.',
      downloads: [
        link('Publication (PLOS ONE)', 'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0099970', 'article'),
        link('Supporting information S3 (XLSX)', 'https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0099970.s003', 'data'),
        link('Supporting information S4 (XLSX)', 'https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0099970.s004', 'data'),
        link('Publication (PMC)', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4055720/', 'article')
      ]
    },
    {
      id: 'ltulipifera-nectar-proteome-2016',
      omicsType: 'proteomics',
      speciesIds: ['tulipifera'],
      title: 'Floral nectar 2-DE and LC–MS/MS proteome',
      titleZh: '北美鹅掌楸花蜜蛋白质组',
      type: 'Secreted proteome',
      accession: 'DOI:10.3389/fpls.2016.00826',
      year: 2016,
      source: 'Frontiers in Plant Science',
      doi: '10.3389/fpls.2016.00826',
      dataLevel: 'Processed identification tables',
      availability: 'processed-public',
      technique: '2-DE, MALDI and nano LC–MS/MS',
      sampleType: 'Floral nectar',
      proteins: '42 identified nectar proteins',
      description: 'Proteomic characterization of L. tulipifera floral nectar, including 42 identified nectar proteins and public supplementary annotation tables.',
      downloads: [
        link('Publication (Frontiers)', 'https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2016.00826/full', 'article'),
        link('Supplementary Table 1 (DOCX)', 'https://pmc.ncbi.nlm.nih.gov/articles/instance/4905952/bin/Table_1.DOCX', 'data'),
        link('Supplementary Table 2 (XLSX)', 'https://pmc.ncbi.nlm.nih.gov/articles/instance/4905952/bin/Table_2.XLSX', 'data'),
        link('Supplementary Table 3 (XLSX)', 'https://pmc.ncbi.nlm.nih.gov/articles/instance/4905952/bin/Table_3.XLSX', 'data'),
        link('Publication (PMC)', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4905952/', 'article')
      ]
    },
    {
      id: 'hybrid-calli-proteome-2015',
      omicsType: 'proteomics',
      speciesIds: ['hybrid_2x'],
      title: 'Embryogenic versus non-embryogenic callus proteome',
      titleZh: '杂交鹅掌楸胚性与非胚性愈伤组织蛋白质组',
      type: 'Comparative 2-DE proteomics',
      accession: 'DOI:10.1007/s11738-015-1963-z',
      year: 2015,
      source: 'Acta Physiologiae Plantarum',
      doi: '10.1007/s11738-015-1963-z',
      dataLevel: 'Publication; raw accession not located',
      availability: 'publication-only',
      technique: '2-DE and mass spectrometry',
      sampleType: 'Embryogenic and non-embryogenic calli',
      description: 'Comparative proteomics of embryogenic and non-embryogenic calli from a Liriodendron hybrid. No dedicated PRIDE/PXD or MassIVE raw-data accession was located during curation.',
      downloads: [
        link('Publication DOI', 'https://doi.org/10.1007/s11738-015-1963-z', 'article')
      ]
    },
    {
      id: 'hybrid-phosphoproteome-2020',
      omicsType: 'proteomics',
      speciesIds: ['hybrid_2x'],
      title: 'Phosphoproteome of embryogenic-competence acquisition',
      titleZh: '杂交鹅掌楸胚性能力获得磷酸化蛋白质组',
      type: '2-DE phosphoproteomics',
      accession: 'DOI:10.13271/j.mpb.018.000001',
      year: 2020,
      source: 'Molecular Plant Breeding',
      doi: '10.13271/j.mpb.018.000001',
      dataLevel: 'Open publication and reported identifications',
      availability: 'processed-public',
      technique: '2-DE, Pro-Q staining and mass spectrometry',
      sampleType: 'Embryogenic and non-embryogenic calli',
      proteins: '41 differential phosphoproteins reported',
      description: 'Open study of protein phosphorylation during acquisition of embryogenic competence in hybrid Liriodendron callus; 41 differentially expressed phosphoproteins were identified.',
      downloads: [
        link('Article page', 'https://molplantbreed.org/index.php/mpbopa/article/view/16002', 'article'),
        link('Open article PDF', 'https://molplantbreed.org/files/upfiles/file/5e6737d15c127.pdf', 'article')
      ]
    },
    {
      id: 'hybrid-al-gaba-itraq-2021',
      omicsType: 'proteomics',
      speciesIds: ['hybrid_2x'],
      title: 'Aluminum-stress and GABA-response iTRAQ proteome',
      titleZh: '杂交鹅掌楸铝胁迫与 GABA 响应 iTRAQ 蛋白质组',
      type: 'Quantitative iTRAQ proteomics',
      accession: 'DOI:10.1038/s41438-021-00517-y',
      year: 2021,
      source: 'Horticulture Research',
      doi: '10.1038/s41438-021-00517-y',
      dataLevel: 'Processed supplementary tables',
      availability: 'processed-public',
      technique: '8-plex iTRAQ LC–MS/MS',
      sampleType: 'Leaves under Al and GABA treatments',
      proteins: '198 differentially expressed proteins reported',
      description: 'Quantitative proteomics of hybrid Liriodendron leaves under aluminum stress, with and without GABA treatment. Supplementary files include the processed protein results.',
      downloads: [
        link('Publication (Nature)', 'https://www.nature.com/articles/s41438-021-00517-y', 'article'),
        link('Publication (PMC)', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8012378/', 'article'),
        link('Supplementary MOESM1 (PDF)', 'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41438-021-00517-y/MediaObjects/41438_2021_517_MOESM1_ESM.pdf', 'data'),
        link('Supplementary MOESM2 (XLSX)', 'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41438-021-00517-y/MediaObjects/41438_2021_517_MOESM2_ESM.xlsx', 'data'),
        link('Supplementary MOESM3 (XLSX)', 'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41438-021-00517-y/MediaObjects/41438_2021_517_MOESM3_ESM.xlsx', 'data')
      ]
    },
    {
      id: 'tetraploid-hybrid-proteome-2021',
      omicsType: 'proteomics',
      speciesIds: ['hybrid_4x'],
      title: 'Tetraploid hybrid transcriptome–proteome comparison',
      titleZh: '四倍体杂交鹅掌楸转录组与 iTRAQ 蛋白质组',
      type: 'iTRAQ proteomics',
      accession: 'DOI:10.1093/treephys/tpab039',
      year: 2021,
      source: 'Tree Physiology',
      doi: '10.1093/treephys/tpab039',
      dataLevel: 'Processed peptide, protein and expression tables',
      availability: 'processed-public',
      technique: 'iTRAQ LC–MS/MS and RNA-seq',
      sampleType: 'Diploid and tetraploid hybrid tissues',
      proteins: '4,018 proteins identified',
      description: 'Integrated transcriptome and proteome comparison of diploid and tetraploid L. sino-americanum. Ten public XLSX files cover peptide, protein, annotation and differential-expression results.',
      downloads: [
        link('Publication (Tree Physiology)', 'https://academic.oup.com/treephys/article/41/10/1953/6206298', 'article'),
        link('Publication (PMC)', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8498940/', 'article'),
        ...tetraploidSupplements
      ]
    },
    {
      id: 'ltulipifera-carotenoid-metabolome-2020',
      omicsType: 'metabolomics',
      speciesIds: ['tulipifera', 'hybrid_2x'],
      title: 'Petal and sepal carotenoid metabolic profiling',
      titleZh: '北美鹅掌楸花瓣/萼片类胡萝卜素代谢组',
      type: 'Untargeted and targeted metabolomics',
      accession: 'DOI:10.1038/s41438-020-0287-3',
      year: 2020,
      source: 'Horticulture Research',
      doi: '10.1038/s41438-020-0287-3',
      dataLevel: 'Processed metabolite and expression tables',
      availability: 'processed-public',
      technique: 'LC–ESI–MS/MS and QTRAP carotenoid profiling',
      sampleType: 'Petals, sepals and hybrid petals',
      compounds: 'Untargeted features and 18 targeted carotenoids',
      description: 'Time-course and tissue-comparison metabolomics of L. tulipifera floral coloration, with carotenoid quantification in two Liriodendron hybrids. Seventeen public supplementary files are indexed.',
      downloads: [
        link('Publication (Nature)', 'https://www.nature.com/articles/s41438-020-0287-3', 'article'),
        link('Publication (PMC)', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7193617/', 'article'),
        ...carotenoidSupplements,
        link('Figshare sequences and annotations', 'https://doi.org/10.6084/m9.figshare.11674020.v1', 'data')
      ]
    },
    {
      id: 'liriodendron-pigmentation-metabolites-2025',
      omicsType: 'metabolomics',
      speciesIds: ['chinense', 'tulipifera', 'hybrid_2x'],
      title: 'Cross-taxon petal pigment targeted metabolite dataset',
      titleZh: '鹅掌楸属花瓣色素靶向代谢物数据',
      type: 'Targeted pigment metabolomics',
      accession: 'PMC12441795',
      year: 2025,
      source: 'Forestry Research',
      dataLevel: 'Processed targeted-metabolite tables',
      availability: 'processed-public',
      technique: 'Targeted carotenoid and chlorophyll quantification',
      sampleType: 'Petals of L. chinense, L. tulipifera and hybrid cultivars',
      compounds: '13 pigment compounds reported',
      description: 'Integrated transcriptomic and targeted metabolite comparison of petal pigmentation across both Liriodendron species and hybrid cultivars. The public ZIP includes Supplementary Table S9.',
      downloads: [
        link('Publication (PMC)', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12441795/', 'article'),
        link('Complete supplementary data (ZIP)', 'https://pmc.ncbi.nlm.nih.gov/articles/instance/12441795/bin/FR-2025-5-0013-Supplementary.zip', 'data'),
        link('Open article PDF', 'https://www.maxapress.com/data/article/forres/preview/pdf/forres-0025-0013.pdf', 'article')
      ]
    },
    {
      id: 'liriodendron-chlorogenic-acid-2024',
      omicsType: 'metabolomics',
      speciesIds: ['chinense', 'tulipifera', 'hybrid_2x'],
      title: 'Petal chlorogenic-acid untargeted metabolome',
      titleZh: '鹅掌楸花瓣绿原酸非靶向代谢组',
      type: 'Untargeted LC–MS metabolomics',
      accession: 'DOI:10.1016/j.scienta.2023.112791',
      year: 2024,
      source: 'Scientia Horticulturae',
      doi: '10.1016/j.scienta.2023.112791',
      dataLevel: 'Publication; raw accession not located',
      availability: 'publication-only',
      technique: 'Untargeted LC–MS and transcriptomics',
      sampleType: 'Petals of L. chinense, L. tulipifera and L. × sinoamericanum',
      compounds: '6,097 metabolite features reported',
      description: 'Comparative petal metabolomics across the two Liriodendron species and their hybrid, focused on chlorogenic-acid biosynthesis and differential accumulation. No dedicated public raw-data accession was located during curation.',
      downloads: [
        link('Publication (ScienceDirect)', 'https://www.sciencedirect.com/science/article/pii/S0304423823009597', 'article'),
        link('Publication DOI', 'https://doi.org/10.1016/j.scienta.2023.112791', 'article')
      ]
    }
  ];

  const fileGroups = [
    {
      datasetId: 'msv000097037',
      accession: 'MSV000097037',
      baseUrl: 'ftp://massive-ftp.ucsd.edu/v09/MSV000097037/raw/',
      files: [
        ['Blank_Tulip.mzXML', 138.2, 'blank', 'blank'],
        ['Blank_Tulip.raw', 165.4, 'blank', 'blank'],
        ['Chin_A.mzXML', 152.0, 'biological_sample', 'chinense'],
        ['Chin_A.raw', 175.3, 'biological_sample', 'chinense'],
        ['Chin_A_iso.mzXML', 88.1, 'biological_sample', 'chinense'],
        ['Chin_A_iso.raw', 104.8, 'biological_sample', 'chinense'],
        ['Chin_D.mzXML', 151.1, 'biological_sample', 'chinense'],
        ['Chin_D.raw', 174.6, 'biological_sample', 'chinense'],
        ['Tulip_3.mzXML', 152.5, 'biological_sample', 'tulipifera'],
        ['Tulip_3.raw', 175.6, 'biological_sample', 'tulipifera'],
        ['Tulip_B.mzXML', 148.8, 'biological_sample', 'tulipifera'],
        ['Tulip_B.raw', 173.0, 'biological_sample', 'tulipifera'],
        ['Tulip_B_iso.mzXML', 88.6, 'biological_sample', 'tulipifera'],
        ['Tulip_B_iso.raw', 105.2, 'biological_sample', 'tulipifera']
      ]
    },
    {
      datasetId: 'msv000089948',
      accession: 'MSV000089948',
      baseUrl: 'ftp://massive-ftp.ucsd.edu/v04/MSV000089948/raw/',
      files: [
        ['Tulip_Branch_3.mzXML', 69.8, 'biological_sample', 'tulipifera'],
        ['Tulip_Branch_3.raw', 100.1, 'biological_sample', 'tulipifera'],
        ['Blank_TP_2021_11_18.mzXML', 76.9, 'blank', 'blank'],
        ['Blank_TP_2021_11_18.raw', 105.8, 'blank', 'blank']
      ]
    },
    {
      datasetId: 'msv000089948',
      accession: 'MSV000089948',
      baseUrl: 'ftp://massive-ftp.ucsd.edu/v04/MSV000089948/updates/2022-07-22_mbertin_f8ff202c/raw/',
      files: [
        ['T_P Branch_3_Gradient.mzXML', 73.5, 'biological_sample', 'tulipifera'],
        ['T_P Branch_3_Gradient.raw', 113.3, 'biological_sample', 'tulipifera'],
        ['Blank_TP_Gradient.mzXML', 63.2, 'blank', 'blank'],
        ['Blank_TP_Gradient.raw', 104.6, 'blank', 'blank']
      ]
    },
    {
      datasetId: 'msv000090615',
      accession: 'MSV000090615',
      baseUrl: 'ftp://massive-ftp.ucsd.edu/v05/MSV000090615/peak/UHPLC-Orbitrap-MS_MS/',
      files: [
        ['JUVI_LITU_Blank1.mzML', null, 'blank', 'mixed_qc'],
        ['JUVI_LITU_Blank2.mzML', null, 'blank', 'mixed_qc'],
        ['JUVI_LITU_POOL_IDENTIFICATION_MS2_CID.mzML', null, 'identification_pool', 'mixed_qc'],
        ['JUVI_LITU_POOL_IDENTIFICATION_MS2_HCD.mzML', null, 'identification_pool', 'mixed_qc'],
        ['JUVI_LITU_POOL_QC_2.mzML', null, 'quality_control', 'mixed_qc'],
        ['JUVI_LITU_POOL_QC_4.mzML', null, 'quality_control', 'mixed_qc'],
        ['JUVI_LITU_POOL_QC_6.mzML', null, 'quality_control', 'mixed_qc'],
        ['JUVI_LITU_POOL_QC_8.mzML', null, 'quality_control', 'mixed_qc'],
        ['JUVI_LITU_POOL_QC_10.mzML', null, 'quality_control', 'mixed_qc'],
        ['JUVI_LITU_POOL_QC_12.mzML', null, 'quality_control', 'mixed_qc'],
        ['JUVI_LITU_POOL_QC_14.mzML', null, 'quality_control', 'mixed_qc'],
        ['LITU_FM_11R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_12R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_14R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_22R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_23R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_24R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_31R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_32R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_33R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_21R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_31R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_32R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_33R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_35R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_11R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_12R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_21R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_22R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_23R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_31R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_32R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_33R.mzML', null, 'biological_sample', 'tulipifera']
      ]
    },
    {
      datasetId: 'msv000090616',
      accession: 'MSV000090616',
      baseUrl: 'ftp://massive-ftp.ucsd.edu/v05/MSV000090616/peak/QTOF-GC-MS/',
      files: [
        ['LITU_FM_11R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_12R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_14R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_22R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_23R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_24R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_31R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_32R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_FM_33R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_21R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_31R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_32R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_33R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_GM_35R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_11R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_12R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_21R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_22R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_23R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_31R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_32R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_NM_33R.mzML', null, 'biological_sample', 'tulipifera'],
        ['LITU_POOL_QC_1.mzML', null, 'quality_control', 'tulipifera'],
        ['LITU_POOL_QC_2.mzML', null, 'quality_control', 'tulipifera']
      ]
    }
  ];

  const files = fileGroups.flatMap(group => group.files.map(file => ({
    datasetId: group.datasetId,
    accession: group.accession,
    name: file[0],
    sizeMb: file[1],
    role: file[2],
    speciesScope: file[3],
    format: file[0].split('.').pop(),
    url: `${group.baseUrl}${encodeURIComponent(file[0])}`
  })));

  const summary = {
    curatedStudies: datasets.length,
    proteomicsStudies: datasets.filter(item => item.omicsType === 'proteomics').length,
    metabolomicsStudies: datasets.filter(item => item.omicsType === 'metabolomics').length,
    rawDatasets: datasets.filter(item => item.availability === 'raw-public').length,
    rawFileLinks: files.length,
    rawDataSize: '~15.65 GB',
    supplementaryAssets: datasets.flatMap(item => item.downloads || []).filter(item => item.kind === 'data').length,
    speciesGroups: Object.keys(species).length
  };

  window.LMDB_OMICS_CATALOG = {
    version: '2026.08',
    curationDate: '2026-08-19',
    scope: 'Public Liriodendron proteomics and metabolomics resources',
    species,
    datasets,
    files,
    summary,
    notes: [
      'MassIVE project directories may contain non-Liriodendron controls; the file browser is restricted to Liriodendron-labelled files plus matched blanks and pooled quality-control files.',
      'LITU denotes L. tulipifera. Chin denotes L. chinense. Blank, pooled QC and identification files are quality-control resources and are not biological replicates.',
      'Some browsers do not open FTP links. Use an FTPES-capable client with host massive-ftp.ucsd.edu, port 21, anonymous login.',
      'Publication-only records are retained for completeness and are explicitly distinguished from studies with public raw spectra or downloadable processed tables.'
    ]
  };
})();
