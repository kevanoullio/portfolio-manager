# Purpose: Import portfolio from PDF file

# Standard Libraries

# Third-party Libraries
from PyPDF2 import PdfReader # Extract text from PDFs

# Load the PDF
reader = PdfReader("monthly_report.pdf")

# Extract text from each page
for page in reader.pages:
    print(page.extract_text())



# Purpose: Import portfolio from PDF file

# Standard Libraries

# Third-party Libraries
import pdfplumber # Extract text and tables from PDFs

# Open the PDF
with pdfplumber.open("monthly_report.pdf") as pdf:
    for page in pdf.pages:
        # Extract text
        print(page.extract_text())

        # Extract tables
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)  # Each row is a list of cell values
