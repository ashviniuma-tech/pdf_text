# Quick Reference Guide

## Installation Commands

### First Time Setup
```bash
# Clone/download the project files
# Navigate to project directory
cd pdf_processor_project

# Run automated setup
./setup.sh          # macOS/Linux
setup.bat           # Windows

# OR manual setup
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Basic Commands

### Activate Environment
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Process PDF (Simple)
```bash
python pdf_processor.py input.pdf output.pdf
```

### Process PDF (Default Output)
```bash
python pdf_processor.py input.pdf
# Creates: processed_output.pdf
```

### With API Key
```bash
# Set key (one time per session)
export ANTHROPIC_API_KEY=sk-ant-...  # macOS/Linux
set ANTHROPIC_API_KEY=sk-ant-...     # Windows

# Then process
python pdf_processor.py input.pdf output.pdf
```

## File Paths

### Current Directory
```bash
python pdf_processor.py paper.pdf clean_paper.pdf
```

### Full Paths
```bash
# Windows
python pdf_processor.py "C:\Users\Name\paper.pdf" "C:\Users\Name\output.pdf"

# macOS/Linux
python pdf_processor.py ~/Documents/paper.pdf ~/Documents/output.pdf
```

### Relative Paths
```bash
python pdf_processor.py ../papers/input.pdf ./outputs/output.pdf
```

## Python Module Usage

### Basic Usage
```python
from pdf_processor import PDFProcessor

processor = PDFProcessor()
processor.process_pdf("input.pdf", "output.pdf")
```

### With API Key
```python
processor = PDFProcessor(api_key="sk-ant-...")
processor.process_pdf("input.pdf", "output.pdf")
```

### Extract Components
```python
# Get text only
text = processor.extract_text_from_pdf("paper.pdf")

# Get title
title = processor.extract_title(text)

# Get abstract
abstract = processor.extract_abstract(text)

# Get tables
tables = processor.extract_tables_from_pdf("paper.pdf")

# Get sections
sections = processor.parse_sections(text)
```

### Batch Processing
```python
import os
from pdf_processor import PDFProcessor

processor = PDFProcessor()

for file in os.listdir("input_folder"):
    if file.endswith(".pdf"):
        input_path = os.path.join("input_folder", file)
        output_path = os.path.join("output_folder", f"processed_{file}")
        processor.process_pdf(input_path, output_path)
```

## Testing

### Run Installation Test
```bash
python test_processor.py
```

### Create Sample PDF
```python
from test_processor import create_sample_pdf
create_sample_pdf("test.pdf")
```

## Common Issues & Fixes

### Module Not Found
```bash
pip install -r requirements.txt
```

### Wrong Directory
```bash
pwd    # Check current directory (macOS/Linux)
cd     # Check current directory (Windows)
ls     # List files (macOS/Linux)
dir    # List files (Windows)
```

### Permission Denied
```bash
chmod +x setup.sh          # Make script executable
chmod +x pdf_processor.py  # Make file executable
```

### Virtual Environment Not Active
```bash
# Look for (venv) in your prompt
# If not there, activate:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### API Key Issues
```bash
# Check if set
echo $ANTHROPIC_API_KEY  # macOS/Linux
echo %ANTHROPIC_API_KEY%  # Windows

# Set permanently (add to shell profile)
# macOS/Linux: ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY=sk-ant-...

# Windows: System Environment Variables
```

## Output Customization

### Change Page Size (A4 instead of Letter)
```python
# In pdf_processor.py, line ~400
from reportlab.lib.pagesizes import A4
pagesize=A4
```

### Change Margins
```python
# In pdf_processor.py, create_formatted_pdf()
rightMargin=50,   # smaller margins
leftMargin=50,
topMargin=50,
bottomMargin=50,
```

### Change Font Size
```python
# In pdf_processor.py, style definitions
title_style = ParagraphStyle(
    ...
    fontSize=14,  # change from 16
)
```

## Directory Structure

### Recommended Setup
```
pdf_processor_project/
├── pdf_processor.py       # Main script
├── requirements.txt       # Dependencies
├── README.md              # Overview
├── SETUP_GUIDE.md        # Detailed guide
├── QUICK_REFERENCE.md    # This file
├── test_processor.py     # Test script
├── setup.sh              # Auto setup (Unix)
├── setup.bat             # Auto setup (Windows)
├── venv/                 # Virtual environment
├── inputs/               # Input PDFs (optional)
│   └── paper1.pdf
└── outputs/              # Processed PDFs (optional)
    └── processed_paper1.pdf
```

## Processing Pipeline

```
Input PDF
    ↓
Extract Text
    ↓
Extract Title → Center in output
    ↓
Extract Abstract → Add to output
    ↓
Remove Content (authors, etc.)
    ↓
Extract Tables → Convert to text
    ↓
Extract Equations → Convert to text
    ↓
Parse Sections → Add to output
    ↓
Remove URLs & Images
    ↓
Format PDF
    ↓
Output PDF
```

## Performance Tips

### Speed Up Processing
- Use rule-based mode (no API key) for faster processing
- Process smaller PDFs first
- Batch similar papers together

### Improve Quality
- Use LLM mode (with API key) for better results
- Ensure input PDF has clear structure
- Check that PDF has text layer (not scanned)

## File Size Reference

| Input Size | Output Size | Time |
|------------|-------------|------|
| 1-2 MB     | ~500 KB     | 10-30s |
| 2-5 MB     | ~1 MB       | 30-60s |
| 5-10 MB    | ~2 MB       | 1-2m |
| 10+ MB     | ~3+ MB      | 2-5m |

## API Usage

### Without API Key
- Uses rule-based extraction
- Free
- Faster
- Good for standard papers

### With API Key
- Uses Claude AI
- Better accuracy
- More intelligent parsing
- Costs ~$0.01-0.05 per paper

## Environment Variables

### Set Temporarily (Current Session)
```bash
export ANTHROPIC_API_KEY=sk-ant-...  # macOS/Linux
set ANTHROPIC_API_KEY=sk-ant-...     # Windows
```

### Set Permanently
**macOS/Linux** - Add to `~/.bashrc` or `~/.zshrc`:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**Windows** - System Properties → Environment Variables

## Deactivate Environment

```bash
deactivate
```

## Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

## Uninstall

```bash
# Deactivate environment
deactivate

# Remove virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Remove other files as needed
```

## Getting Help

1. Read error messages carefully
2. Check this guide
3. See SETUP_GUIDE.md for details
4. Test installation: `python test_processor.py`
5. Verify file paths and Python version

## Keyboard Shortcuts

### Stop Running Process
- `Ctrl + C` (all platforms)

### Clear Terminal
- `clear` (macOS/Linux)
- `cls` (Windows)

---

## One-Line Commands

```bash
# Complete setup and first run
./setup.sh && source venv/bin/activate && python pdf_processor.py paper.pdf

# Process and open output
python pdf_processor.py paper.pdf output.pdf && open output.pdf

# Batch process all PDFs in folder
for f in *.pdf; do python pdf_processor.py "$f" "processed_$f"; done
```

---

**Keep this guide handy for quick reference!**