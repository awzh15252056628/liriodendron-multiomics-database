Liriodendron database compact GitHub Pages version

This folder is a smaller copy of the final static website.

What was changed:
- Large embedded base64 images/pages were extracted into the assets/ folder.
- Large raw reference/result text files were gzip-compressed as .gz files.
- API keys were not written into the HTML. DeepSeek keys are saved only in the local browser via localStorage after the page prompts for them.
- Omics Data is organized into four prominent peer layers: Genomics, Transcriptomics, Proteomics and Metabolomics; multiomics.html remains the file-level detail view for public proteomics and metabolomics records.
- The omics catalog indexes 13 studies, 4 MassIVE projects and 79 file-level spectrum links without duplicating the ~15.65 GB source files in this repository.

Notes:
- The website entry page is index.html.
- Compressed .gz files are suitable for download/archive. Unzip them first if you need to inspect the raw FASTA/GFF/GTF/PAF/CSV text directly.
- For GitHub Pages, upload this folder's contents, not the zip file alone.
- Any API key that has appeared in chat history or an HTML file should be rotated before public release.

Public AI assistant:
- The frontend now calls /api/deepseek-chat first.
- Deploy this folder with Vercel if you want every visitor to use the AI assistant without entering an API key.
- In Vercel Project Settings -> Environment Variables, set DEEPSEEK_API_KEY to your DeepSeek key.
- Optional variables:
  - DEEPSEEK_MODEL=deepseek-v4-flash
  - RATE_LIMIT_PER_MINUTE=30
  - MAX_TOKENS=2048
- If you keep the site on pure GitHub Pages, GitHub Pages cannot run /api/deepseek-chat. In that case visitors must use their own local DeepSeek API key, or you must deploy the API proxy elsewhere and set window.LMDB_AI_PROXY_URL to that proxy URL.
