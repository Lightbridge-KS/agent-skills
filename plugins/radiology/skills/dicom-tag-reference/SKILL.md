---
name: dicom-tag-reference
description: >
  Look up common DICOM data-element tags, their keywords, VRs, and meaning when
  reading, writing, or anonymizing DICOM. Use when the user mentions a DICOM tag
  (e.g. "0010,0010"), asks which tag holds a value, or works with pydicom /
  DICOM headers. Starter skill — extend as needed.
metadata:
  version: "2026-06-12"
---

# DICOM Tag Reference

A DICOM tag is a `(group,element)` pair in hexadecimal, e.g. `(0010,0010)`.
Odd-numbered groups are *private*. **VR** = Value Representation (the data type).

> Starter reference — add the tags you reach for most. For the full dictionary,
> see the DICOM standard PS3.6 or `pydicom.datadict`.

## Patient

| Tag | Keyword | VR | Meaning |
| --- | ------- | -- | ------- |
| (0010,0010) | PatientName | PN | Patient's full name |
| (0010,0020) | PatientID | LO | Primary patient identifier |
| (0010,0030) | PatientBirthDate | DA | Birth date (`YYYYMMDD`) |
| (0010,0040) | PatientSex | CS | `M` / `F` / `O` |

## Study / Series

| Tag | Keyword | VR | Meaning |
| --- | ------- | -- | ------- |
| (0020,000D) | StudyInstanceUID | UI | Unique study identifier |
| (0020,000E) | SeriesInstanceUID | UI | Unique series identifier |
| (0008,0020) | StudyDate | DA | Date the study started |
| (0008,0060) | Modality | CS | `CR`, `CT`, `MR`, `US`, … |
| (0008,103E) | SeriesDescription | LO | Human-readable series label |

## Image / pixel

| Tag | Keyword | VR | Meaning |
| --- | ------- | -- | ------- |
| (0028,0010) | Rows | US | Image height (px) |
| (0028,0011) | Columns | US | Image width (px) |
| (0028,0100) | BitsAllocated | US | Bits per sample (e.g. 16) |
| (0028,1050) | WindowCenter | DS | Display window level |
| (0028,1051) | WindowWidth | DS | Display window width |
| (7FE0,0010) | PixelData | OW/OB | The pixel buffer |

## Quick `pydicom` lookups

```python
from pydicom.datadict import keyword_for_tag, tag_for_keyword

keyword_for_tag(0x00100010)        # -> 'PatientName'
tag_for_keyword('StudyInstanceUID')  # -> 0x0020000D
```

## Anonymization note

When de-identifying, also clear/replace dates, accession number `(0008,0050)`,
institution `(0008,0080)`, referring physician `(0008,0090)`, and any private
tags — not just `PatientName` / `PatientID`. Follow DICOM PS3.15 Annex E for a
complete profile.
