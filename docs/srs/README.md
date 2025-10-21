# SRS Documentation

This folder contains the Software Requirements Specification documents for the Supplier Consumer Platform (SCP).

## Files

- `SCP_Executive_Summary.pdf` - High-level overview of the project
- `SRS_SCP(Supplier_Consumer_Platform)_v2.0.pdf` - Detailed requirements specification

## Converting PDFs to Markdown

For better LLM agent readability, PDFs should be converted to Markdown format.

### Recommended Method: marker-pdf

**marker-pdf** uses ML models for high-quality conversion with proper structure preservation.

```bash
# Install
pip install marker-pdf

# Convert Executive Summary
marker_single docs/srs/SCP_Executive_Summary.pdf docs/srs/SCP_Executive_Summary.md

# Convert Full SRS
marker_single "docs/srs/SRS_SCP(Supplier_Consumer_Platform)_v2.0.pdf" docs/srs/SRS_SCP_v2.0.md
```

**Features:**
- Preserves tables, headers, and formatting
- Detects document structure (H1, H2, H3, etc.)
- Handles multi-column layouts correctly
- Best for complex documents

### Alternative: pymupdf4llm (Lightweight)

If you prefer a simpler tool without ML dependencies:

```bash
# Install
pip install pymupdf4llm

# Convert using Python
python -c "import pymupdf4llm; pymupdf4llm.to_markdown('docs/srs/SCP_Executive_Summary.pdf', 'docs/srs/SCP_Executive_Summary.md')"
```

**Features:**
- Fast and lightweight
- Specifically optimized for LLM consumption
- No ML models required

### Alternative: Pandoc (Universal)

```bash
# Install (macOS)
brew install pandoc

# Convert
pandoc docs/srs/SCP_Executive_Summary.pdf -o docs/srs/SCP_Executive_Summary.md
pandoc "docs/srs/SRS_SCP(Supplier_Consumer_Platform)_v2.0.pdf" -o docs/srs/SRS_SCP_v2.0.md
```

**Features:**
- Universal document converter
- No dependencies
- Decent quality for most documents

## Why Convert to Markdown?

- **Better for LLMs**: Text format is easier for AI agents to parse and understand
- **Version Control**: Markdown diffs are readable in Git
- **Searchable**: Full-text search without PDF parsing
- **Editable**: Easy to update and maintain documentation
- **Lightweight**: Smaller file size than PDFs

## Recommendation

For the SRS documents in this project, **marker-pdf** is recommended due to the complex tables and multi-section structure in the full SRS document.

