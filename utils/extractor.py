from PyPDF2 import PdfReader
from typing import Optional

class PaperExtractor:
    @staticmethod
    def extract_section(pdf_path: str, section_name: str) -> Optional[str]:
        """Extracts specific section from PDF"""
        reader = PdfReader(pdf_path)
        text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        section = text.lower().find(section_name.lower())
        next_section = text.lower().find("\n1 ", section)  # Find next section
        return text[section:next_section].strip() if section != -1 else None

    @staticmethod
    def extract_abstract(pdf_path: str) -> str:
        """Extracts abstract with fallback"""
        abstract = PaperExtractor.extract_section(pdf_path, "abstract")
        return abstract or " ".join(PdfReader(pdf_path).pages[0].extract_text().split()[:200])