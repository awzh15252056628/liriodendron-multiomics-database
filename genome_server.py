# -*- coding: utf-8 -*-
"""
鹅掌楸基因组序列查询服务器 (便携版)
Liriodendron Genome Sequence Query Server - Portable Edition
=============================================================
此脚本使用相对路径，将服务器文件和基因组数据放在同一文件夹即可运行。
启动方法: python genome_server.py  (双击 启动.bat 自动运行)
访问地址: http://localhost:7788
"""

import os, sys, re, json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# ─── 路径自动检测 (相对路径，便于移植) ─────────────────────────────────────
# 服务器所在目录就是数据根目录
BASE = os.path.dirname(os.path.abspath(__file__))

SPECIES_FILES = {
    'chinense': {
        'genome':  os.path.join(BASE, '中国鹅掌楸参考基因组', 'Liriodendronchinense_Genome.fasta'),
        'cds':     os.path.join(BASE, '中国鹅掌楸参考基因组', 'Liriodendron_cds.fasta'),
        'protein': os.path.join(BASE, '中国鹅掌楸参考基因组', 'Lchi_protein.fasta'),
        'gff':     os.path.join(BASE, '中国鹅掌楸参考基因组', 'Liriodendronchinense.gff'),
        'label':   'L. chinense (中国鹅掌楸)',
    },
    'tulipifera': {
        'genome':  os.path.join(BASE, '北美鹅掌楸参考基因组', 'LtulipiferaYP108A_766_v1.0.fa'),
        'cds':     os.path.join(BASE, '北美鹅掌楸参考基因组', 'LtulipiferaYP108A_766_v1.1.cds.fa'),
        'protein': os.path.join(BASE, '北美鹅掌楸参考基因组', 'Ltulipifera_protein'),
        'gff':     os.path.join(BASE, '北美鹅掌楸参考基因组', 'Ltulipifera.gff'),
        'label':   'L. tulipifera (北美鹅掌楸)',
    },
}

PORT = 7788

# ─── FASTA 字节偏移索引器 ───────────────────────────────────────────────────
class FastaIndex:
    def __init__(self, fasta_path):
        self.path = fasta_path
        self.index = {}   # KEY.upper() -> (seq_byte_offset, header_str)
        self._built = False

    def build(self):
        if self._built:
            return
        if not os.path.exists(self.path):
            print(f'  [WARN] Missing: {os.path.basename(self.path)}')
            self._built = True
            return
        print(f'  Indexing {os.path.basename(self.path)} ...')
        count = 0
        with open(self.path, 'rb') as f:
            while True:
                raw = f.readline()
                if not raw:
                    break
                if raw.startswith(b'>'):
                    header = raw.decode('utf-8', errors='replace').strip()
                    seq_offset = f.tell()
                    key = header.lstrip('>').split()[0]
                    self._add(key, seq_offset, header)
                    locus = re.sub(r'(\.\d+)+\.?p?$', '', key)
                    if locus != key:
                        self._add_secondary(locus, seq_offset, header)
                    count += 1
        self._built = True
        print(f'  Done: {count} seqs in {os.path.basename(self.path)}')

    def _add(self, key, offset, header):
        self.index[key.upper()] = (offset, header)

    def _add_secondary(self, key, offset, header):
        if key.upper() not in self.index:
            self.index[key.upper()] = (offset, header)

    def fetch(self, gene_id, max_len=None):
        if not self._built:
            self.build()
        key = gene_id.strip().upper()
        if key not in self.index:
            return None, None
        seq_offset, header = self.index[key]
        parts = []
        total = 0
        with open(self.path, 'rb') as f:
            f.seek(seq_offset)
            while True:
                raw = f.readline()
                if not raw or raw.startswith(b'>'):
                    break
                chunk = raw.decode('utf-8', errors='replace').strip()
                parts.append(chunk)
                total += len(chunk)
                if max_len and total >= max_len:
                    break
        seq = ''.join(parts)
        if max_len:
            seq = seq[:max_len]
        return header, seq


# ─── GFF 解析器 ───────────────────────────────────────────────────────────────
class GFFStore:
    def __init__(self, gff_path):
        self.path = gff_path
        self.genes = {}   # KEY.upper() -> info dict
        self._built = False

    def build(self):
        if self._built:
            return
        if not os.path.exists(self.path):
            print(f'  [WARN] Missing GFF: {os.path.basename(self.path)}')
            self._built = True
            return
        print(f'  Parsing {os.path.basename(self.path)} ...')
        count = 0
        with open(self.path, encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('\t')
                if len(parts) == 9:
                    seqid, src, ftype, start, end, score, strand, phase, attrs = parts
                    ad = {}
                    for tok in attrs.split(';'):
                        if '=' in tok:
                            k, v = tok.strip().split('=', 1)
                            ad[k] = v
                    gene_id = ad.get('ID') or ad.get('Parent', '')
                    gene_id = gene_id.split(';')[0].strip()
                    if not gene_id:
                        continue
                    uk = gene_id.upper()
                    if uk not in self.genes:
                        self.genes[uk] = {
                            'id': gene_id, 'chr': seqid,
                            'start': int(start), 'end': int(end),
                            'strand': strand, 'type': ftype,
                            'features': []
                        }
                    else:
                        g = self.genes[uk]
                        g['start'] = min(g['start'], int(start))
                        g['end']   = max(g['end'],   int(end))
                    self.genes[uk]['features'].append({
                        'type': ftype,
                        'start': int(start), 'end': int(end),
                        'strand': strand
                    })
                    count += 1
                elif len(parts) == 4:
                    try:
                        seqid, start, end, gene_id = parts
                        gene_id = gene_id.strip()
                        uk = gene_id.upper()
                        if uk not in self.genes:
                            self.genes[uk] = {
                                'id': gene_id, 'chr': seqid,
                                'start': int(start), 'end': int(end),
                                'strand': '.', 'type': 'gene',
                                'features': []
                            }
                        count += 1
                    except ValueError:
                        continue
        self._built = True
        print(f'  Done: {count} GFF records -> {len(self.genes)} genes')

    def get(self, gene_id):
        if not self._built:
            self.build()
        return self.genes.get(gene_id.strip().upper())

    def search(self, keyword, limit=20):
        if not self._built:
            self.build()
        kw = keyword.strip().upper()
        hits = [v['id'] for k, v in self.genes.items() if kw in k]
        return hits[:limit], len(hits)


# ─── 基因组随机访问 ────────────────────────────────────────────────────────────
class GenomeStore:
    def __init__(self, genome_path):
        self.path = genome_path
        self.index = {}   # CHROM.upper() -> byte offset of first seq line
        self._built = False

    def build(self):
        if self._built:
            return
        if not os.path.exists(self.path):
            print(f'  [WARN] Missing genome: {os.path.basename(self.path)}')
            self._built = True
            return
        print(f'  Indexing genome {os.path.basename(self.path)} (chromosome headers only)...')
        with open(self.path, 'rb') as f:
            while True:
                raw = f.readline()
                if not raw:
                    break
                if raw.startswith(b'>'):
                    name = raw.decode('utf-8', errors='replace').strip().lstrip('>').split()[0]
                    self.index[name.upper()] = f.tell()
        self._built = True
        print(f'  Done: {len(self.index)} chromosomes/scaffolds indexed')

    def fetch_region(self, chrom, start, end):
        """Fetch 1-based [start, end] from chrom."""
        if not self._built:
            self.build()
        key = chrom.strip().upper()
        if key not in self.index:
            return None
        seq_offset = self.index[key]
        target_start_0 = start - 1
        target_len = end - start + 1
        collected = []
        total = 0
        skip = target_start_0
        with open(self.path, 'rb') as f:
            f.seek(seq_offset)
            while total < target_len:
                raw = f.readline()
                if not raw or raw.startswith(b'>'):
                    break
                chunk = raw.decode('utf-8', errors='replace').strip()
                if not chunk:
                    continue
                if skip > 0:
                    if skip >= len(chunk):
                        skip -= len(chunk)
                        continue
                    chunk = chunk[skip:]
                    skip = 0
                needed = target_len - total
                collected.append(chunk[:needed])
                total += min(len(chunk), needed)
        return ''.join(collected)


# ─── 全局存储 ─────────────────────────────────────────────────────────────────
stores = {}

def get_store(species):
    if species not in stores:
        cfg = SPECIES_FILES[species]
        stores[species] = {
            'cds':     FastaIndex(cfg['cds']),
            'protein': FastaIndex(cfg['protein']),
            'gff':     GFFStore(cfg['gff']),
            'genome':  GenomeStore(cfg['genome']),
        }
    return stores[species]

def ensure_built(species, *keys):
    s = get_store(species)
    for k in keys:
        s[k].build()
    return s


# ─── 核心查询函数 ──────────────────────────────────────────────────────────────
def query_gene(species, gene_id, seq_types):
    result = {'gene_id': gene_id, 'species': species, 'found': False, 'data': {}}
    if species not in SPECIES_FILES:
        result['error'] = f'Unknown species "{species}"'
        return result

    ensure_built(species, 'gff')
    s = stores[species]
    gene_info = s['gff'].get(gene_id)

    if gene_info:
        result['found'] = True
        feats = gene_info['features']
        cds_feats  = [f for f in feats if f['type'] == 'CDS']
        utr5_feats = [f for f in feats if 'five' in f['type'].lower() or 'utr5' in f['type'].lower()]
        utr3_feats = [f for f in feats if 'three' in f['type'].lower() or 'utr3' in f['type'].lower()]
        result['data']['gene_info'] = {
            'id':          gene_info['id'],
            'chromosome':  gene_info['chr'],
            'start':       gene_info['start'],
            'end':         gene_info['end'],
            'strand':      gene_info['strand'],
            'gene_length': gene_info['end'] - gene_info['start'] + 1,
            'cds_exons':   len(cds_feats),
            'cds_coords':  [(f['start'], f['end']) for f in sorted(cds_feats, key=lambda x: x['start'])],
            'utr5':        [(f['start'], f['end']) for f in utr5_feats],
            'utr3':        [(f['start'], f['end']) for f in utr3_feats],
        }

    if 'cds' in seq_types:
        ensure_built(species, 'cds')
        header, seq = s['cds'].fetch(gene_id)
        if seq:
            result['found'] = True
            result['data']['cds'] = {
                'header':      header,
                'length':      len(seq),
                'sequence':    seq[:3000],
                'truncated':   len(seq) > 3000,
                'full_length': len(seq),
            }

    if 'protein' in seq_types:
        ensure_built(species, 'protein')
        header, seq = s['protein'].fetch(gene_id)
        if seq:
            result['found'] = True
            result['data']['protein'] = {
                'header':      header,
                'length':      len(seq),
                'sequence':    seq[:1500],
                'truncated':   len(seq) > 1500,
                'full_length': len(seq),
            }

    if ('promoter' in seq_types or 'upstream' in seq_types) and gene_info:
        ensure_built(species, 'genome')
        g = gene_info
        chrom, gstart, gend, strand = g['chr'], g['start'], g['end'], g['strand']
        prom_len = 2000
        if strand == '-':
            prom_start = gend + 1
            prom_end   = gend + prom_len
        else:
            prom_start = max(1, gstart - prom_len)
            prom_end   = gstart - 1
        if prom_end >= prom_start:
            seq = s['genome'].fetch_region(chrom, prom_start, prom_end)
            if seq:
                result['found'] = True
                result['data']['promoter'] = {
                    'region':   f'{chrom}:{prom_start}-{prom_end}',
                    'strand':   strand,
                    'length':   len(seq),
                    'sequence': seq,
                    'note':     '2000 bp upstream of gene start (potential promoter region)',
                }

    if not result['found']:
        result['error'] = f'Gene "{gene_id}" not found in {SPECIES_FILES[species]["label"]}'

    return result


# ─── HTTP 处理器 ──────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f'  [{args[1]}] {args[0]}')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors(); self.end_headers()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._cors(); self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        qs     = parse_qs(parsed.query)
        path   = parsed.path
        def p(k, d=None): return qs.get(k, [d])[0]

        try:
            if path == '/ping':
                self.send_json({'status': 'ok', 'port': PORT,
                                'species': list(SPECIES_FILES.keys()),
                                'base_dir': BASE})

            elif path == '/stats':
                sp  = p('species', 'chinense')
                cfg = SPECIES_FILES.get(sp, {})
                info = {'species': cfg.get('label', sp), 'files': {}}
                for k in ('genome', 'cds', 'protein', 'gff'):
                    fp = cfg.get(k, '')
                    info['files'][k] = {
                        'exists':  os.path.exists(fp),
                        'size_mb': round(os.path.getsize(fp)/1e6, 1) if os.path.exists(fp) else 0,
                    }
                if sp in stores:
                    g = stores[sp]['gff']
                    if g._built: info['gene_count'] = len(g.genes)
                    c = stores[sp]['cds']
                    if c._built: info['cds_count'] = len(c.index)
                self.send_json(info)

            elif path == '/gene':
                gene_id = p('id', '')
                species = p('species', 'chinense')
                types   = [t.strip() for t in p('types', 'gene_info,cds,protein,promoter').split(',')]
                if not gene_id:
                    self.send_json({'error': 'Missing ?id='}, 400); return
                self.send_json(query_gene(species, gene_id, types))

            elif path == '/search':
                kw      = p('q', '')
                species = p('species', 'chinense')
                limit   = int(p('limit', '20'))
                if not kw:
                    self.send_json({'error': 'Missing ?q='}, 400); return
                ensure_built(species, 'gff')
                hits, total = stores[species]['gff'].search(kw, limit)
                self.send_json({'query': kw, 'species': species,
                                'matches': hits, 'total_found': total})

            elif path == '/preload':
                sp    = p('species', 'chinense')
                types = [t.strip() for t in p('types', 'gff,cds,protein').split(',')]
                def _bg(): ensure_built(sp, *types)
                threading.Thread(target=_bg, daemon=True).start()
                self.send_json({'status': 'preloading', 'species': sp, 'types': types})

            else:
                self.send_json({'error': f'Unknown path: {path}'}, 404)

        except Exception as e:
            import traceback
            self.send_json({'error': str(e), 'trace': traceback.format_exc()}, 500)


# ─── 入口 ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('=' * 65)
    print('  鹅掌楸基因组序列查询服务器  v1.1 (便携版)')
    print(f'  数据目录: {BASE}')
    print(f'  http://localhost:{PORT}')
    print('=' * 65)
    missing_any = False
    for sp, cfg in SPECIES_FILES.items():
        print(f'\n  [{cfg["label"]}]')
        for k in ('genome', 'cds', 'protein', 'gff'):
            fp = cfg[k]
            ok = 'OK' if os.path.exists(fp) else 'MISSING!'
            sz = f'{os.path.getsize(fp)/1e6:.0f} MB' if os.path.exists(fp) else ''
            print(f'    {k:<9} {os.path.basename(fp):<50} {sz:>8}  {ok}')
            if not os.path.exists(fp):
                missing_any = True
    print()
    if missing_any:
        print('  [WARN] Some genome files are missing. Please ensure')
        print('         the genome folders are in the same directory as this script.')
        print()

    # 后台预加载 GFF + 小型 FASTA 索引
    def _preload():
        for sp in SPECIES_FILES:
            try:
                ensure_built(sp, 'gff', 'cds', 'protein')
            except Exception as e:
                print(f'  [WARN] Preload error ({sp}): {e}')
        print('  [INFO] Preload complete. Genome indexed on first promoter query.')
    threading.Thread(target=_preload, daemon=True).start()

    server = HTTPServer(('localhost', PORT), Handler)
    print(f'  Listening on http://localhost:{PORT}  (Ctrl+C to stop)\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Server stopped.')
