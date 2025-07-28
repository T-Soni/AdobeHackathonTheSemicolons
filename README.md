# Adobe Hackathon - Round 1A Solution

## 🧠 Overview
This solution extracts:
- Title
- Headings (H1, H2, H3 with page numbers)

from each PDF file placed in `/app/input`, and saves JSON output into `/app/output`.

## 🛠 Approach
- Uses [PyMuPDF](https://pymupdf.readthedocs.io/) to read PDFs.
- Heuristics: combines font size, boldness, ALL CAPS, short length, and center alignment to detect headings (not just font size).
- Modular code: `get_baseline_style`, `classify_span`, `extract_outline`.

## 📦 Dependencies
- Python 3.9
- pymupdf

(All installed inside the container.)

---

## 🚀 Build & Run

### Build:
```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomid .
