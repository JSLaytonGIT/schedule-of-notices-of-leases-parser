import os
from schedule_of_notices_of_leases_parser import schedule_of_notices_of_leases_parser

pdf_directory = './test_pdfs/'

try:
    pdf_files = os.listdir(pdf_directory)
    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the specified directory.")
    
    pdf_file = pdf_files[0]
    pdf_path = os.path.join(pdf_directory, pdf_file)
    
    extracted_text = schedule_of_notices_of_leases_parser(pdf_path)
    print(extracted_text)

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
