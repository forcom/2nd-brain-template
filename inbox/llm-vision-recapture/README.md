# LLM-vision re-capture — staging

Per-page transcriptions in progress, staged here because `inbox/` is the schema's
temporary intake area and, unlike an agent scratchpad, it survives across sessions.
The agent scratchpad was wiped twice mid-job, losing ~7 pages of transcription each
time; page images are cheap to re-render, transcriptions are not.

Delete a `tx*/` directory once its document has been assembled into `raw/papers/`.

## Method

Per SCHEMA.md "PDF page images are the evidence":

```bash
pdftoppm -r 150 -png "<source.pdf>" <scratch>/pg     # images: regenerate freely
# read each pg-NN.png, transcribe verbatim -> tx<doc>/pg-NN.txt
python3 assemble.py "<source.pdf>" tx<doc> <out-name>.md "<doc id>" <lang> <date> [supersedes]
```

`assemble.py` refuses to write unless every page of the PDF has a transcription, so an
interrupted run cannot produce a silently short raw record.

## Queue

| # | document | pages | transcribed | assembled |
|---|---|---|---|---|
| 1 | ISO 14001:2026 (en) | 46 | 46 / 46 | done → `raw/papers/iso-14001-2026-en.md` |
| 2 | KS X ISO/IEC 27001 (ko) | 32 | see `tx27001/` | → `ks-x-iso-iec-27001-20241030-ko-llmvision.md` |
| 3 | KS Q ISO 9001 (ko) | 46 | — | → `ks-q-iso-9001-20241213-ko-llmvision.md` |
| 4 | KS X ISO/IEC 42001 (ko) | 68 | — | → `ks-x-iso-iec-42001-20251030-ko-llmvision.md` |
| 5 | KS I ISO 14001:2015 (ko) | 48 | — | → `ks-i-iso-14001-20210928-ko-llmvision.md` |

Superseding an existing capture: the new record sits beside the old one and carries
`supersedes_capture:` in its frontmatter. The old record keeps its bytes and `sha256` —
re-extraction is not one of SCHEMA.md's two permitted raw mutations.

## Open finding — document #2 designation

The cover and the body title page both read **`KS X ISO/IEC 27001:2013`**, and the 개요
states the standard is based on the 2013 second edition of ISO/IEC 27001. The running
header on every page instead reads `KS X ISO/IEC 27001:2014`, and the existing capture's
frontmatter took that value (`standard_id: "KS X ISO/IEC 27001:2014"`). The 목차 also
lists the commentary as `KS X ISO/IEC 27001:2013 해설`.

2014-12-12 is the 개정 date printed on the cover, not the designation. The new capture
should therefore use `KS X ISO/IEC 27001:2013`, and `.factlog` subjects built on the 2014
form need updating once it is assembled.
