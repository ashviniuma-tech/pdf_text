"""
Test script to verify PDF processor installation
Creates a sample PDF and processes it
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os


def create_sample_pdf(filename="test_paper.pdf"):
    """Create a sample academic paper PDF for testing"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("The Impact of Machine Learning on Academic Research", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Authors (will be removed)
    authors = Paragraph("John Doe, Jane Smith<br/>University of Example<br/>email@example.com", styles['Normal'])
    story.append(authors)
    story.append(Spacer(1, 20))
    
    # Abstract
    abstract_heading = Paragraph("<b>Abstract</b>", styles['Heading2'])
    story.append(abstract_heading)
    
    abstract_text = """
    This paper examines the transformative impact of machine learning algorithms on 
    contemporary academic research methodologies. We analyze various applications across 
    multiple disciplines and demonstrate significant improvements in data processing efficiency. 
    Our findings suggest that machine learning tools have become indispensable in modern research.
    For more information, visit http://example.com/research.
    """
    abstract_para = Paragraph(abstract_text, styles['Normal'])
    story.append(abstract_para)
    story.append(Spacer(1, 20))
    
    # Introduction
    intro_heading = Paragraph("<b>1. Introduction</b>", styles['Heading2'])
    story.append(intro_heading)
    
    intro_text = """
    Machine learning has revolutionized the way researchers approach complex problems. 
    Traditional methods often struggled with large datasets, but modern ML algorithms 
    can process millions of data points efficiently. See DOI: 10.1234/example for details.
    
    The equation for linear regression is: y = mx + b, where m is the slope and b is the intercept.
    
    This study explores these developments in detail and provides recommendations for future research.
    Link to dataset: https://data.example.com/dataset
    """
    intro_para = Paragraph(intro_text, styles['Normal'])
    story.append(intro_para)
    story.append(Spacer(1, 12))
    
    # Methods
    methods_heading = Paragraph("<b>2. Methods</b>", styles['Heading2'])
    story.append(methods_heading)
    
    methods_text = """
    We employed a mixed-methods approach combining quantitative analysis with qualitative 
    case studies. Our dataset included 10,000 research papers published between 2018 and 2023.
    
    Table 1 shows the distribution of papers by discipline. The neural network architecture
    followed the equation: f(x) = σ(Wx + b), where σ is the activation function.
    
    More details at: www.research-methods.com
    """
    methods_para = Paragraph(methods_text, styles['Normal'])
    story.append(methods_para)
    story.append(Spacer(1, 12))
    
    # Results
    results_heading = Paragraph("<b>3. Results</b>", styles['Heading2'])
    story.append(results_heading)
    
    results_text = """
    Our analysis revealed significant patterns in the adoption of machine learning across 
    disciplines. Computer science led with 45% adoption, followed by biology at 30%, 
    and social sciences at 25%.
    
    The improvement in processing time followed a logarithmic pattern: T = log(n) * k,
    where n is the dataset size and k is a constant factor.
    """
    results_para = Paragraph(results_text, styles['Normal'])
    story.append(results_para)
    story.append(Spacer(1, 12))
    
    # Conclusion
    conclusion_heading = Paragraph("<b>4. Conclusion</b>", styles['Heading2'])
    story.append(conclusion_heading)
    
    conclusion_text = """
    This study demonstrates the pervasive influence of machine learning in academic research.
    Future work should focus on making these tools more accessible to researchers across all
    disciplines. Contact us at research@university.edu for collaboration opportunities.
    """
    conclusion_para = Paragraph(conclusion_text, styles['Normal'])
    story.append(conclusion_para)
    
    # Build PDF
    doc.build(story)
    print(f"✓ Sample PDF created: {filename}")


def test_installation():
    """Test if all required packages are installed"""
    print("\n" + "="*50)
    print("Testing PDF Processor Installation")
    print("="*50 + "\n")
    
    errors = []
    
    # Test imports
    print("Checking required packages...")
    
    try:
        import pdfplumber
        print("✓ pdfplumber installed")
    except ImportError:
        errors.append("pdfplumber not installed")
        print("✗ pdfplumber NOT installed")
    
    try:
        from pypdf import PdfReader
        print("✓ pypdf installed")
    except ImportError:
        errors.append("pypdf not installed")
        print("✗ pypdf NOT installed")
    
    try:
        from reportlab.pdfgen import canvas
        print("✓ reportlab installed")
    except ImportError:
        errors.append("reportlab not installed")
        print("✗ reportlab NOT installed")
    
    try:
        import anthropic
        print("✓ anthropic installed")
    except ImportError:
        errors.append("anthropic not installed")
        print("✗ anthropic NOT installed")
    
    print()
    
    if errors:
        print("Installation incomplete! Missing packages:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease run: pip install -r requirements.txt")
        return False
    else:
        print("✓ All required packages are installed!")
        return True


def run_test():
    """Run a complete test of the PDF processor"""
    print("\n" + "="*50)
    print("Running PDF Processor Test")
    print("="*50 + "\n")
    
    # Check if processor exists
    if not os.path.exists("pdf_processor.py"):
        print("✗ pdf_processor.py not found!")
        print("Make sure you're in the correct directory.")
        return
    
    # Create sample PDF
    print("Step 1: Creating sample PDF...")
    create_sample_pdf("test_paper.pdf")
    
    # Import and test processor
    print("\nStep 2: Testing PDF processor...")
    try:
        from pdf_processor import PDFProcessor
        
        processor = PDFProcessor()
        
        print("  - Extracting text...")
        text = processor.extract_text_from_pdf("test_paper.pdf")
        if text:
            print("  ✓ Text extraction successful")
        else:
            print("  ✗ Text extraction failed")
        
        print("  - Extracting title...")
        title = processor.extract_title(text)
        print(f"    Title found: {title[:50]}...")
        
        print("  - Extracting abstract...")
        abstract = processor.extract_abstract(text)
        if abstract:
            print(f"  ✓ Abstract extraction successful ({len(abstract)} chars)")
        else:
            print("  ✗ Abstract extraction failed")
        
        print("\nStep 3: Processing complete PDF...")
        processor.process_pdf("test_paper.pdf", "test_output.pdf")
        
        if os.path.exists("test_output.pdf"):
            print("\n✓ Test successful! Output created: test_output.pdf")
            print("\nYou can now:")
            print("  1. Open test_output.pdf to see the results")
            print("  2. Process your own PDFs with:")
            print("     python pdf_processor.py your_paper.pdf output.pdf")
        else:
            print("\n✗ Test failed: Output PDF not created")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure all dependencies are installed")
        print("  2. Check that pdf_processor.py is in the current directory")
        print("  3. Try running: pip install -r requirements.txt")


def main():
    """Main test function"""
    print("\n" + "="*60)
    print("PDF PROCESSOR - INSTALLATION TEST")
    print("="*60)
    
    # Test installation
    if not test_installation():
        print("\nPlease install missing packages before continuing.")
        return
    
    # Run processor test
    response = input("\nRun processor test? (y/n): ").lower()
    if response == 'y':
        run_test()
    else:
        print("\nTest skipped. You can run it later with: python test_processor.py")
    
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()