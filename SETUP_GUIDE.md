# PDF Academic Paper Processor - Setup Guide

## Overview
This application processes academic PDF papers by:
- Extracting the title and centering it
- Removing content between title and abstract
- Reading content section by section
- Removing all URLs and links
- Converting tables and equations to descriptive text
- Removing all images
- Creating a properly formatted PDF output

## Features
- **LLM-Powered Processing**: Uses Claude AI for intelligent content extraction (optional)
- **Rule-Based Fallback**: Works without API key using pattern matching
- **Professional Formatting**: Clean, justified text with proper spacing
- **Automatic Section Detection**: Intelligently identifies paper sections

---

## Step-by-Step Setup

### Step 1: System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Operating System: Windows, macOS, or Linux

### Step 2: Install Python (if needed)

#### Windows:
1. Download Python from https://www.python.org/downloads/
2. Run installer and check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

#### macOS:
```bash
# Install using Homebrew
brew install python3
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 3: Create Project Directory
```bash
# Create a new directory for the project
mkdir pdf_processor_project
cd pdf_processor_project
```

### Step 4: Download the Files
Place these files in your project directory:
- `pdf_processor.py` (main application)
- `requirements.txt` (dependencies)
- `SETUP_GUIDE.md` (this file)

### Step 5: Create Virtual Environment (Recommended)

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your command prompt.

### Step 6: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `pdfplumber` - PDF text and table extraction
- `pypdf` - PDF reading library
- `reportlab` - PDF creation library
- `anthropic` - Claude AI API client (optional)

### Step 7: (Optional) Set Up Claude API Key

For enhanced LLM-powered processing:

1. Get API key from: https://console.anthropic.com/
2. Set as environment variable:

#### Windows (Command Prompt):
```bash
set ANTHROPIC_API_KEY=your_api_key_here
```

#### Windows (PowerShell):
```bash
$env:ANTHROPIC_API_KEY="your_api_key_here"
```

#### macOS/Linux:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

**Note**: The application works without an API key using rule-based extraction!

---

## Usage Instructions

### Basic Usage

1. **Place your PDF file** in the project directory
   ```
   pdf_processor_project/
   ├── pdf_processor.py
   ├── requirements.txt
   ├── your_paper.pdf  ← Your input PDF
   └── venv/
   ```

2. **Run the processor**:
   ```bash
   python pdf_processor.py your_paper.pdf output_paper.pdf
   ```

3. **Find your output**: The processed PDF will be saved as `output_paper.pdf`

### Alternative Usage

**Default output name**:
```bash
python pdf_processor.py your_paper.pdf
# Creates: processed_output.pdf
```

**Full path examples**:
```bash
# Windows
python pdf_processor.py "C:\Users\YourName\Documents\paper.pdf" "C:\Users\YourName\Documents\processed.pdf"

# macOS/Linux
python pdf_processor.py ~/Documents/paper.pdf ~/Documents/processed.pdf
```

---

## Processing Steps Explained

The application performs these steps automatically:

1. **Extract Text**: Reads all text from the PDF
2. **Extract Title**: Identifies and extracts the paper title
3. **Extract Abstract**: Locates and extracts the abstract section
4. **Remove Intermediate Content**: Deletes author info, affiliations, etc.
5. **Extract Tables**: Finds all tables and converts them to descriptions
6. **Process Content**: 
   - Removes all URLs and links
   - Converts equations to text descriptions
   - Removes image references
7. **Parse Sections**: Identifies all paper sections
8. **Create PDF**: Generates formatted output with:
   - Centered title
   - Left-aligned section headings
   - Justified body text
   - Proper spacing

---

## Output Format

The generated PDF has:
- **Title**: Centered, bold, 16pt font
- **Abstract**: Justified text with heading
- **One line space** between abstract and content
- **Section headings**: Left-aligned, bold, 12pt font
- **Body text**: Justified, 10pt font
- **Margins**: 1 inch on all sides
- **No images, no URLs, no links**

---

## Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure virtual environment is activated and requirements are installed:
```bash
pip install -r requirements.txt
```

### Issue: "File not found" error
**Solution**: Check the PDF path is correct:
```bash
# Show current directory
pwd  # macOS/Linux
cd   # Windows

# List files
ls    # macOS/Linux
dir   # Windows
```

### Issue: PDF extraction fails
**Solution**: The PDF might be:
- Password protected (remove password first)
- Scanned images (OCR required - see Advanced Usage)
- Corrupted (try opening in PDF reader first)

### Issue: Poor formatting in output
**Solution**: 
- Make sure input PDF has clear structure
- LLM mode (with API key) gives better results
- Some PDFs may need manual review

### Issue: Missing sections
**Solution**:
- Check if input PDF has standard academic structure
- Verify section headings are clear (Introduction, Methods, etc.)
- Use LLM mode for better section detection

---

## Advanced Usage

### Using as a Python Module

```python
from pdf_processor import PDFProcessor

# Initialize
processor = PDFProcessor(api_key="your_api_key_here")  # or None for rule-based

# Process PDF
processor.process_pdf("input.pdf", "output.pdf")
```

### Custom Processing

```python
# Extract only text
text = processor.extract_text_from_pdf("paper.pdf")

# Extract only tables
tables = processor.extract_tables_from_pdf("paper.pdf")

# Get title
title = processor.extract_title(text)

# Parse sections
sections = processor.parse_sections(text)
```

### Batch Processing

Create a batch script:

```python
import os
from pdf_processor import PDFProcessor

processor = PDFProcessor()

# Process all PDFs in a directory
input_dir = "input_papers"
output_dir = "processed_papers"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"processed_{filename}")
        
        print(f"Processing {filename}...")
        processor.process_pdf(input_path, output_path)
```

---

## Configuration Options

### Modify Page Size

Edit `pdf_processor.py`, line ~400:
```python
# Change from letter to A4
pagesize=A4  # instead of letter
```

### Modify Margins

Edit `pdf_processor.py`, line ~400:
```python
rightMargin=50,   # Default: 72 (1 inch)
leftMargin=50,
topMargin=50,
bottomMargin=50,
```

### Modify Font Sizes

Edit styles in `create_formatted_pdf()` method:
```python
fontSize=14,  # Change from 16 for smaller title
```

---

## Performance Notes

- **Small PDFs** (< 10 pages): ~10-30 seconds
- **Medium PDFs** (10-50 pages): ~30-120 seconds
- **Large PDFs** (> 50 pages): ~2-5 minutes

LLM mode is slower but more accurate. Rule-based mode is faster.

---

## Examples

### Example 1: Process a research paper
```bash
python pdf_processor.py "AI_Research_Paper.pdf" "Cleaned_AI_Paper.pdf"
```

### Example 2: Quick processing with default output
```bash
python pdf_processor.py thesis.pdf
```

### Example 3: Process from different directory
```bash
python pdf_processor.py "../downloads/paper.pdf" "./outputs/processed.pdf"
```

---

## FAQ

**Q: Do I need the Claude API key?**  
A: No! The app works without it using rule-based extraction. API gives better results.

**Q: Can I process scanned PDFs?**  
A: Not directly. You need to OCR them first (use tools like Adobe Acrobat or pytesseract).

**Q: Will this work with any PDF?**  
A: Best results with academic papers that have clear structure. May not work well with:
- Scanned documents
- PDFs without text layer
- Non-standard formats

**Q: Can I keep the images?**  
A: Currently, no. The design removes images. You can modify the code to keep them.

**Q: What about references/bibliography?**  
A: They're included in the output but URLs in them are removed.

**Q: Can I process multiple PDFs at once?**  
A: Yes! See "Batch Processing" in Advanced Usage section.

---

## File Structure

After setup, your directory should look like:
```
pdf_processor_project/
├── pdf_processor.py          # Main application
├── requirements.txt          # Python dependencies
├── SETUP_GUIDE.md           # This guide
├── venv/                    # Virtual environment (if created)
├── your_input.pdf           # Your PDF to process
└── processed_output.pdf     # Generated output
```

---

## Getting Help

If you encounter issues:

1. **Check Error Messages**: Read the error output carefully
2. **Verify File Paths**: Ensure PDF exists and path is correct
3. **Check PDF Validity**: Open PDF in a reader to verify it's not corrupted
4. **Update Dependencies**: Run `pip install --upgrade -r requirements.txt`
5. **Python Version**: Ensure you're using Python 3.8+

---

## License

This code is provided as-is for educational and research purposes.

---

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] PDF file ready in project directory
- [ ] Run command: `python pdf_processor.py input.pdf output.pdf`
- [ ] Check output.pdf in your directory

---

**Ready to process your first PDF?**

```bash
# Activate environment (if not already active)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Process your PDF
python pdf_processor.py your_paper.pdf processed_paper.pdf
```

**Congratulations! You're all set! 🎉**