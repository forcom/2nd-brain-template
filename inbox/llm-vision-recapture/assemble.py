#!/usr/bin/env python3
"""Assemble per-page LLM-vision transcriptions into a raw/papers capture.

SCHEMA.md "PDF page images are the evidence": the body is the transcription of the
rendered pages, never an OCR tool's output and never the embedded text layer.
Normalization: LF, form feeds -> numbered page markers, NUL/backspace removed, one
final LF. `sha256` covers the post-frontmatter body only.

Refuses to write unless every page of the source PDF has a transcription, so an
interrupted run cannot produce a silently short raw record.

    python3 assemble.py <pdf> <txt-dir> <out-name.md> "<doc id>" <lang> <ingested> [supersedes] [source-url]
"""
import hashlib, pathlib, re, subprocess, sys

WIKI = pathlib.Path(__file__).resolve().parents[2]


def build(pdf_path, txt_dir, out_name, doc_id, lang, ingested, supersedes='', source_url=''):
    pdf = pathlib.Path(pdf_path)
    raw = pdf.read_bytes()
    pdf_sha = hashlib.sha256(raw).hexdigest()
    npages = int(re.search(r'^Pages:\s+(\d+)$',
                           subprocess.run(['pdfinfo', str(pdf)], capture_output=True,
                                          text=True).stdout, re.M).group(1))
    td = pathlib.Path(txt_dir)
    missing = [i for i in range(1, npages + 1) if not (td / f'pg-{i:02d}.txt').exists()]
    if missing:
        sys.exit(f'refusing to assemble: {len(missing)} page(s) not transcribed: {missing}')

    parts = []
    for i in range(1, npages + 1):
        t = (td / f'pg-{i:02d}.txt').read_text(encoding='utf-8')
        t = t.replace('\r\n', '\n').replace('\r', '\n').replace('\x00', '').replace('\x08', '')
        parts.append(f'<!-- PDF page {i} -->\n\n{t.strip()}\n')
    extracted = '\n'.join(parts)
    extracted_sha = hashlib.sha256(extracted.encode()).hexdigest()

    origin = ''
    if source_url:
        origin = (f'- Retrieved from: {source_url} — the PDF is not an ISO-hosted copy; '
                  'iso.org refuses automated download. Provenance was checked against the '
                  'file itself (PDF Author `ISO`, ISO typesetting, ISO/IEC 2020 copyright '
                  'notice) before capture.\n')

    note = ''
    if supersedes:
        note = (f'- Supersedes: `{supersedes}` — same source PDF, captured earlier with '
                '`poppler-pdftotext-layout`. That record keeps its bytes and `sha256`; '
                'cite this one.\n')

    body = (
        f'# {doc_id}\n\n'
        '## Capture metadata\n\n'
        f'- Original PDF: `{pdf.name}`\n'
        f'- PDF SHA-256: `{pdf_sha}`\n'
        f'- Pages: {npages}\n'
        f'- Language: `{lang}`\n'
        '- Extraction: `llm-vision-transcription` — pages rendered with '
        '`pdftoppm -r 150 -png` and transcribed by reading each page image. No OCR tool '
        'was used and the PDF text layer was not used.\n'
        f'{origin}'
        f'{note}'
        '- Normalization: LF line endings, form feeds replaced by numbered page markers, '
        'NUL/backspace controls removed, final LF.\n'
        '- Figures, tables and multi-column layouts are described in square brackets where '
        'they cannot be transcribed as running text.\n\n'
        '## Extracted text\n'
        f'{extracted}'
    )
    if not body.endswith('\n'):
        body += '\n'
    body_sha = hashlib.sha256(body.encode()).hexdigest()

    fm = (
        '---\n'
        'source_type: local-pdf\n'
        f'source_file: "{pdf.name}"\n'
        + (f'source_url: "{source_url}"\n' if source_url else '') +
        f'standard_id: "{doc_id}"\n'
        f'language: {lang}\n'
        f'pages: {npages}\n'
        f'source_pdf_bytes: {len(raw)}\n'
        f'source_pdf_sha256: {pdf_sha}\n'
        'extraction_method: llm-vision-transcription\n'
        'extraction_quality: llm-vision-verbatim-unreviewed\n'
        f'extracted_text_sha256: {extracted_sha}\n'
        + (f'supersedes_capture: {supersedes}\n' if supersedes else '') +
        f'ingested: {ingested}\n'
        f'sha256: {body_sha}\n'
        '---\n'
    )
    target = WIKI / 'raw' / 'papers' / out_name
    target.write_text(fm + body, encoding='utf-8')
    print(f'wrote {target}')
    print(f'  pages: {npages}, bytes: {len(fm + body)}')
    print(f'  extracted_text_sha256: {extracted_sha}')
    print(f'  sha256 (post-frontmatter body): {body_sha}')


if __name__ == '__main__':
    build(*sys.argv[1:])
