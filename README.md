# PDF Academic Paper Processor

Automatically process academic papers: extract titles, remove unnecessary content, convert tables and equations to text, remove images and links, and generate a clean, formatted PDF.

## Features ✨

- 🎯 **Smart Title Extraction**: Automatically identifies paper titles
- 📄 **Clean Content**: Removes everything between title and abstract
- 🔍 **Section Detection**: Intelligently parses paper sections
- 🔗 **URL Removal**: Strips all links and URLs
- 📊 **Table Conversion**: Converts tables to descriptive text
- 📐 **Equation Descriptions**: Converts equations to plain language
- 🖼️ **Image Removal**: Automatically removes all images
- 🤖 **LLM-Powered**: Optional Claude AI integration for better accuracy
- 📝 **Professional Formatting**: Creates beautifully formatted PDFs

## Quick Start 🚀

### Option 1: Automated Setup (Recommended)

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
setup.bat
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage 📖

### Basic Usage
```bash
python pdf_processor.py input_paper.pdf output_paper.pdf
```

### With Default Output Name
```bash
python pdf_processor.py input_paper.pdf
# Creates: processed_output.pdf
```

### With Claude AI (Better Results)
```bash
# Set API key
export ANTHROPIC_API_KEY=your_key_here  # macOS/Linux
set ANTHROPIC_API_KEY=your_key_here     # Windows

# Run processor
python pdf_processor.py input_paper.pdf output_paper.pdf
```

## What It Does 🔧

1. **Extracts** the paper title and centers it
2. **Removes** author information, affiliations, and content before abstract
3. **Preserves** the abstract section
4. **Detects** and extracts all content sections
5. **Removes** all URLs, links, and DOIs
6. **Converts** tables to descriptive paragraphs
7. **Describes** equations in plain language
8. **Removes** all images and figures
9. **Creates** a clean, professionally formatted PDF

## Output Format 📄

The generated PDF includes:
- **Title**: Centered, bold (16pt)
- **Abstract**: With heading, justified text
- **Sections**: Left-aligned headings (12pt), justified content (10pt)
- **Spacing**: Proper line spacing throughout
- **Margins**: 1-inch margins on all sides
- **Clean**: No images, no URLs, no clutter

## Requirements 📋

- Python 3.8 or higher
- See `requirements.txt` for package dependencies

## Project Structure 📁

```
pdf_processor_project/
├── pdf_processor.py      # Main application
├── requirements.txt      # Python dependencies
├── SETUP_GUIDE.md       # Detailed setup instructions
├── README.md            # This file
├── setup.sh             # Auto setup script (Unix)
├── setup.bat            # Auto setup script (Windows)
└── venv/                # Virtual environment
```

## Examples 💡

### Process a Research Paper
```bash
python pdf_processor.py research_paper.pdf cleaned_paper.pdf
```

### Process Multiple Papers (Batch)
```python
from pdf_processor import PDFProcessor

processor = PDFProcessor()

for pdf_file in ["paper1.pdf", "paper2.pdf", "paper3.pdf"]:
    output = f"processed_{pdf_file}"
    processor.process_pdf(pdf_file, output)
    print(f"✓ Processed {pdf_file}")
```

### Python Module Usage
```python
from pdf_processor import PDFProcessor

# Initialize with API key (optional)
processor = PDFProcessor(api_key="your_key_here")

# Process PDF
processor.process_pdf("input.pdf", "output.pdf")

# Or use individual functions
text = processor.extract_text_from_pdf("paper.pdf")
title = processor.extract_title(text)
tables = processor.extract_tables_from_pdf("paper.pdf")
```

## Modes of Operation 🔄

### 1. LLM Mode (With API Key)
- Uses Claude AI for intelligent extraction
- Better title detection
- Accurate section parsing
- Smart table and equation descriptions
- **Recommended for best results**

### 2. Rule-Based Mode (Without API Key)
- Uses pattern matching and heuristics
- No API costs
- Faster processing
- Good for standard academic papers
- **Works offline**

## Troubleshooting 🔧

### Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"File not found"**
```bash
# Check file path
ls -la input.pdf  # macOS/Linux
dir input.pdf     # Windows
```

**Poor extraction quality**
- Try with Claude API key for better results
- Ensure PDF has text layer (not scanned)
- Check if PDF follows standard academic format

**Missing sections**
- Verify section headings are clear
- Use LLM mode for better detection
- Some PDFs may need manual review

See `SETUP_GUIDE.md` for detailed troubleshooting.

## Advanced Configuration ⚙️

### Change Page Size
```python
# In pdf_processor.py, modify create_formatted_pdf()
from reportlab.lib.pagesizes import A4
pagesize=A4  # instead of letter
```

### Adjust Margins
```python
rightMargin=50,  # instead of 72
leftMargin=50,
topMargin=50,
bottomMargin=50,
```

### Modify Fonts
```python
# In style definitions
fontSize=14,  # change title size
fontName='Times-Roman'  # change font
```

## Performance ⚡

| PDF Size | Processing Time |
|----------|----------------|
| < 10 pages | 10-30 seconds |
| 10-50 pages | 30-120 seconds |
| > 50 pages | 2-5 minutes |

*LLM mode is slower but more accurate*

## Limitations ⚠️

- Does not work with scanned PDFs (requires OCR pre-processing)
- Best results with standard academic paper format
- May need manual review for non-standard layouts
- Tables with complex formatting may need adjustment

## Contributing 🤝

Feel free to:
- Report bugs
- Suggest features
- Submit improvements
- Share feedback

## License 📜

This project is provided as-is for educational and research purposes.

## Support 💬

For detailed instructions, see `SETUP_GUIDE.md`

For issues:
1. Check error messages carefully
2. Verify file paths and Python version
3. Ensure dependencies are installed
4. Review troubleshooting section

## Acknowledgments 🙏

Built with:
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF extraction
- [pypdf](https://github.com/py-pdf/pypdf) - PDF manipulation
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [Anthropic Claude](https://www.anthropic.com/) - AI processing

---

**Ready to clean your academic papers?** 🎉

```bash
python pdf_processor.py your_paper.pdf cleaned_paper.pdf
```