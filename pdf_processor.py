"""
PDF Academic Paper Processor
Extracts, cleans, and reformats academic papers with LLM-powered content processing
"""

import re
import pdfplumber
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
import anthropic
import os
from typing import Dict, List, Tuple
import json


class PDFProcessor:
    """Process academic PDFs with LLM-powered intelligent extraction"""
    
    def __init__(self, api_key: str = None):
        """Initialize the PDF processor
        
        Args:
            api_key: Anthropic API key (optional, uses environment variable if not provided)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            # For demo purposes, we'll work without API key using rule-based extraction
            print("Warning: No Anthropic API key found. Using rule-based extraction.")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract all text from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        except Exception as e:
            print(f"Error extracting text with pdfplumber: {e}")
            # Fallback to pypdf
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            except Exception as e2:
                print(f"Error extracting text with pypdf: {e2}")
        
        return text
    
    def extract_tables_from_pdf(self, pdf_path: str) -> List[Dict]:
        """Extract tables from PDF with page information"""
        tables_data = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    tables = page.extract_tables()
                    for table_num, table in enumerate(tables, 1):
                        if table and len(table) > 0:
                            tables_data.append({
                                'page': page_num,
                                'table_num': table_num,
                                'data': table
                            })
        except Exception as e:
            print(f"Error extracting tables: {e}")
        
        return tables_data
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs and links from text"""
        # Remove http/https URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        # Remove www URLs
        text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        # Remove DOI links
        text = re.sub(r'doi:\s*[^\s]+', '', text)
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_title(self, text: str) -> str:
        """Extract title from the beginning of the paper - exact as in paper"""
        return self._extract_title_rule_based(text)
    
    def _extract_title_rule_based(self, text: str) -> str:
        """Rule-based title extraction - takes exact title from paper"""
        lines = text.split('\n')
        
        # Clean and filter lines
        potential_titles = []
        for i, line in enumerate(lines[:15]):  # Check first 15 lines
            line = line.strip()
            # Skip very short lines, URLs, emails, and common header text
            if len(line) < 10 or len(line) > 300:
                continue
            if any(x in line.lower() for x in ['http', 'www.', '@', 'arxiv', 'volume', 'journal', 'issn', 'doi:', 'page']):
                continue
            # Skip lines that look like dates or page numbers
            if re.search(r'\d{4}|\bpage\b|\bvol\b', line.lower()):
                continue
            # Skip lines with common paper metadata
            if any(x in line.lower() for x in ['abstract', 'author', 'university', 'department', 'published', 'received']):
                continue
            
            potential_titles.append(line)
        
        if potential_titles:
            # Return the first valid line as exact title
            return potential_titles[0]
        
        # Fallback: look for the longest line in first 5 lines
        longest = ""
        for line in lines[:5]:
            line = line.strip()
            if len(line) > len(longest) and len(line) > 15:
                longest = line
        
        return longest if longest else "Untitled Document"
    
    def _extract_title_with_llm(self, text: str) -> str:
        """Extract title using Claude API"""
        try:
            # Take first 2000 characters for title extraction
            excerpt = text[:2000]
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"""Extract ONLY the title of this academic paper. Return just the title text, nothing else.

Paper excerpt:
{excerpt}"""
                }]
            )
            
            title = message.content[0].text.strip()
            return title if title else "Untitled Document"
        except Exception as e:
            print(f"Error extracting title with LLM: {e}")
            return self._extract_title_rule_based(text)
    
    def find_abstract_section(self, text: str) -> Tuple[int, int]:
        """Find the start and end positions of the abstract section"""
        text_lower = text.lower()
        
        # Find abstract start
        abstract_patterns = [r'\babstract\b', r'\bsummary\b']
        abstract_start = -1
        for pattern in abstract_patterns:
            match = re.search(pattern, text_lower)
            if match:
                abstract_start = match.start()
                break
        
        if abstract_start == -1:
            return -1, -1
        
        # Find abstract end (usually Introduction or Keywords)
        end_patterns = [r'\bintroduction\b', r'\b1\s*\.?\s*introduction\b', r'\bkeywords\b']
        abstract_end = len(text)
        for pattern in end_patterns:
            match = re.search(pattern, text_lower[abstract_start:])
            if match:
                abstract_end = abstract_start + match.start()
                break
        
        return abstract_start, abstract_end
    
    def extract_abstract(self, text: str) -> str:
        """Extract abstract text"""
        start, end = self.find_abstract_section(text)
        if start == -1:
            return ""
        
        abstract = text[start:end]
        # Remove the word "abstract" from beginning
        abstract = re.sub(r'^\s*abstract\s*:?\s*', '', abstract, flags=re.IGNORECASE)
        return abstract.strip()
    
    def remove_content_before_abstract(self, text: str, title: str) -> str:
        """Remove everything between title and abstract"""
        # Find abstract position
        start, _ = self.find_abstract_section(text)
        if start == -1:
            return text
        
        # Find title position
        title_pos = text.lower().find(title.lower())
        if title_pos == -1:
            title_pos = 0
        
        # Remove content between title and abstract
        return text[start:]
    
    def parse_sections(self, text: str) -> List[Dict[str, str]]:
        """Parse text into sections"""
        if self.client:
            return self._parse_sections_with_llm(text)
        else:
            return self._parse_sections_rule_based(text)
    
    def _parse_sections_rule_based(self, text: str) -> List[Dict[str, str]]:
        """Rule-based section parsing - captures ALL sections including abstract"""
        sections = []
        
        # Enhanced section patterns to catch more variations
        section_patterns = [
            # Standard numbered sections: "1. Introduction", "1 Introduction", "1.1 Background"
            r'\n\s*(\d+\.?\d*\.?\s+[A-Z][^\n]{3,60})\s*\n',
            # All caps headers: "ABSTRACT", "INTRODUCTION"
            r'\n\s*([A-Z][A-Z\s]{3,50})\s*\n',
            # Title case headers: "Abstract", "Introduction", "Related Work"
            r'\n\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,4})\s*\n',
            # Common paper sections without numbers
            r'\n\s*(Abstract|Introduction|Related Work|Background|Methodology|Methods|Results|Discussion|Conclusion|References|Acknowledgments)\s*\n',
        ]
        
        matches = []
        for pattern in section_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                header = match.group(1).strip()
                # Skip very short matches or those with special chars
                if len(header) < 3 or any(c in header for c in [':', '(', ')', '[', ']']):
                    continue
                matches.append((match.start(), header))
        
        # Remove duplicates (same position)
        seen_positions = set()
        unique_matches = []
        for pos, header in sorted(matches, key=lambda x: x[0]):
            if pos not in seen_positions:
                unique_matches.append((pos, header))
                seen_positions.add(pos)
        
        # Sort by position
        unique_matches.sort(key=lambda x: x[0])
        
        # Extract content between headers
        for i, (pos, header) in enumerate(unique_matches):
            start = pos
            end = unique_matches[i + 1][0] if i + 1 < len(unique_matches) else len(text)
            content = text[start:end]
            
            # Remove the header from content and clean
            content = content[len(header):].strip()
            
            # Skip if content is too short (likely not a real section)
            if len(content) < 50:
                continue
            
            sections.append({
                'heading': header,
                'content': content
            })
        
        # If no sections found, create one big section
        if not sections:
            sections.append({
                'heading': 'Content',
                'content': text
            })
        
        return sections
    
    def _parse_sections_with_llm(self, text: str) -> List[Dict[str, str]]:
        """Parse sections using Claude API"""
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": f"""Parse this academic paper into sections. For each section, extract the heading and content.
Return as JSON array with format: [{{"heading": "Section Name", "content": "Section text..."}}]

Paper text:
{text[:15000]}"""  # Limit to avoid token limits
                }]
            )
            
            response_text = message.content[0].text
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                sections = json.loads(json_match.group())
                return sections
            else:
                return self._parse_sections_rule_based(text)
        except Exception as e:
            print(f"Error parsing sections with LLM: {e}")
            return self._parse_sections_rule_based(text)
    
    def describe_table(self, table_data: List[List]) -> str:
        """Convert table to descriptive text - uses LLM when available"""
        if self.client:
            return self._describe_table_with_llm(table_data)
        else:
            print("  Note: LLM not available for table description, using basic description")
            return self._describe_table_rule_based(table_data)
    
    def _describe_table_rule_based(self, table_data: List[List]) -> str:
        """Rule-based table description"""
        if not table_data or len(table_data) == 0:
            return ""
        
        rows = len(table_data)
        cols = len(table_data[0]) if table_data[0] else 0
        
        # Get headers
        headers = table_data[0] if table_data[0] else []
        header_text = ", ".join([str(h) for h in headers if h])
        
        description = f"Table with {rows} rows and {cols} columns. "
        if header_text:
            description += f"Columns include: {header_text}. "
        
        # Sample some data
        if len(table_data) > 1:
            sample_row = table_data[1]
            sample_text = ", ".join([str(x) for x in sample_row[:3] if x])
            description += f"Sample data: {sample_text}."
        
        return description
    
    def _describe_table_with_llm(self, table_data: List[List]) -> str:
        """Describe table using Claude API - returns single descriptive paragraph"""
        try:
            # Convert table to text (limit to first 20 rows for token efficiency)
            table_rows = table_data[:20]
            table_text = "\n".join([" | ".join([str(cell) if cell else "" for cell in row]) for row in table_rows])
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": f"""Describe this table in ONE comprehensive paragraph. Include:
- What type of data the table contains
- The main columns and what they represent
- Key findings or patterns in the data
- Any notable values or trends

Keep it to one flowing paragraph. Do not use bullet points or multiple paragraphs.

Table data:
{table_text}"""
                }]
            )
            
            description = message.content[0].text.strip()
            # Ensure it's a single paragraph by removing extra newlines
            description = " ".join(description.split())
            return description
        except Exception as e:
            print(f"  Warning: LLM table description failed ({e}), using fallback")
            return self._describe_table_rule_based(table_data)
    
    def describe_equation(self, equation_text: str) -> str:
        """Convert equation to descriptive text - uses LLM when available"""
        if self.client:
            return self._describe_equation_with_llm(equation_text)
        else:
            print("  Note: LLM not available for equation description, using basic description")
            return self._describe_equation_rule_based(equation_text)
    
    def _describe_equation_rule_based(self, equation_text: str) -> str:
        """Rule-based equation description"""
        # Simple description based on common patterns
        if '=' in equation_text:
            return f"Mathematical equation: {equation_text}"
        elif any(op in equation_text for op in ['+', '-', '*', '/', '^']):
            return f"Mathematical expression: {equation_text}"
        else:
            return f"Formula: {equation_text}"
    
    def _describe_equation_with_llm(self, equation_text: str) -> str:
        """Describe equation using Claude API - returns single descriptive paragraph"""
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{
                    "role": "user",
                    "content": f"""Describe this mathematical equation/formula in ONE clear paragraph. Explain:
- What the equation represents
- What each variable or symbol means
- What the equation is used for

Keep it to one flowing paragraph in plain English. Do not use mathematical notation in your description.

Equation: {equation_text}"""
                }]
            )
            
            description = message.content[0].text.strip()
            # Ensure it's a single paragraph
            description = " ".join(description.split())
            return description
        except Exception as e:
            print(f"  Warning: LLM equation description failed ({e}), using fallback")
            return self._describe_equation_rule_based(equation_text)
    
    def process_content(self, text: str, tables: List[Dict]) -> str:
        """Process content: remove URLs, replace tables/equations with descriptions"""
        # Remove URLs
        text = self.remove_urls(text)
        
        # Find and replace equations (LaTeX style)
        equation_pattern = r'\$\$.*?\$\$|\$.*?\$|\\begin\{equation\}.*?\\end\{equation\}'
        equations = re.finditer(equation_pattern, text, re.DOTALL)
        
        for match in equations:
            equation = match.group()
            description = self.describe_equation(equation)
            text = text.replace(equation, f"[Equation: {description}]")
        
        # Replace table references with descriptions
        for i, table_info in enumerate(tables):
            table_desc = self.describe_table(table_info['data'])
            # Insert table description in text
            table_marker = f"\n\n[Table {i+1}: {table_desc}]\n\n"
            # Try to find a good position (after table mention)
            table_ref = re.search(rf'Table\s+{i+1}', text, re.IGNORECASE)
            if table_ref:
                insert_pos = table_ref.end()
                text = text[:insert_pos] + table_marker + text[insert_pos:]
        
        return text
    
    def create_formatted_pdf(self, output_path: str, title: str, 
                           sections: List[Dict[str, str]]):
        """Create formatted PDF with proper styling - includes ALL sections"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Title style - centered
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.black,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Section heading style - left aligned
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.black,
            spaceAfter=12,
            spaceBefore=12,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Body text style - justified
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            fontName='Helvetica'
        )
        
        # Build document
        story = []
        
        # Add title
        story.append(Paragraph(self.clean_text_for_pdf(title), title_style))
        story.append(Spacer(1, 12))
        
        # Add all sections (including Abstract, Introduction, etc.)
        for i, section in enumerate(sections):
            heading = section.get('heading', '')
            content = section.get('content', '')
            
            # Add heading
            if heading:
                heading_clean = self.clean_text_for_pdf(heading)
                story.append(Paragraph(heading_clean, heading_style))
            
            # Add one line space after Abstract heading before content
            if heading and 'abstract' in heading.lower() and i == 0:
                story.append(Spacer(1, 12))
            
            # Add content
            if content:
                # Split long content into paragraphs
                paragraphs = content.split('\n\n')
                for para in paragraphs:
                    para = para.strip()
                    if para:
                        para_clean = self.clean_text_for_pdf(para)
                        story.append(Paragraph(para_clean, body_style))
                        story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
        print(f"  ✓ PDF created with {len(sections)} sections")
    
    def clean_text_for_pdf(self, text: str) -> str:
        """Clean text for PDF rendering - escape special characters"""
        # Remove or escape special characters that cause issues
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def process_pdf(self, input_path: str, output_path: str):
        """Main processing pipeline - extracts ALL sections"""
        print("Step 1: Extracting text from PDF...")
        full_text = self.extract_text_from_pdf(input_path)
        
        print("Step 2: Extracting title (exact from paper)...")
        title = self.extract_title(full_text)
        print(f"  Title: {title}")
        
        print("Step 3: Extracting tables...")
        tables = self.extract_tables_from_pdf(input_path)
        print(f"  Found {len(tables)} tables")
        
        print("Step 4: Removing content before abstract (authors, affiliations)...")
        # Find where abstract starts
        abstract_start, abstract_end = self.find_abstract_section(full_text)
        
        if abstract_start > 0:
            # Get everything from abstract onwards (includes abstract, intro, all sections)
            content_from_abstract = full_text[abstract_start:]
        else:
            # If no abstract found, try to skip initial metadata
            # Look for Introduction or numbered section
            intro_match = re.search(r'\b(introduction|1\s*\.?\s*introduction)\b', full_text, re.IGNORECASE)
            if intro_match:
                content_from_abstract = full_text[intro_match.start():]
            else:
                # Take everything after first 500 chars to skip header
                content_from_abstract = full_text[500:] if len(full_text) > 500 else full_text
        
        print("Step 5: Processing content (removing URLs, converting tables/equations)...")
        processed_content = self.process_content(content_from_abstract, tables)
        
        print("Step 6: Parsing ALL sections (abstract, introduction, methods, etc.)...")
        sections = self.parse_sections(processed_content)
        print(f"  Found {len(sections)} sections")
        
        # Print section names for verification
        if sections:
            print("  Sections detected:")
            for i, section in enumerate(sections[:10], 1):  # Show first 10
                heading = section.get('heading', 'Unknown')
                print(f"    {i}. {heading}")
            if len(sections) > 10:
                print(f"    ... and {len(sections) - 10} more")
        
        print("Step 7: Creating formatted PDF...")
        self.create_formatted_pdf(output_path, title, sections)
        
        print(f"\n✓ Processing complete! Output saved to: {output_path}")


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_processor.py <input_pdf> [output_pdf]")
        print("\nExample: python pdf_processor.py paper.pdf processed_paper.pdf")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else "processed_output.pdf"
    
    # Check if input file exists
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' not found!")
        sys.exit(1)
    
    # Initialize processor
    processor = PDFProcessor()
    
    # Process the PDF
    processor.process_pdf(input_pdf, output_pdf)


if __name__ == "__main__":
    main()