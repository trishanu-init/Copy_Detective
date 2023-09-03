import PyPDF2
import os
from difflib import SequenceMatcher

def pdf_to_text(pdf_path):
    """
    Extract text from a PDF file.
    """
    pdf_text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                pdf_text += page.extractText()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return pdf_text

def similarity_ratio(text1, text2):
    """
    Calculate the similarity ratio between two text strings.
    """
    similarity = SequenceMatcher(None, text1, text2).ratio()
    return similarity

def check_plagiarism(pdf_dir):
    """
    Check plagiarism among multiple PDF files in a directory.
    """
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    num_files = len(pdf_files)

    if num_files < 2:
        print("There are not enough PDF files to compare.")
        return

    for i in range(num_files):
        for j in range(i + 1, num_files):
            file1 = os.path.join(pdf_dir, pdf_files[i])
            file2 = os.path.join(pdf_dir, pdf_files[j])

            text1 = pdf_to_text(file1)
            text2 = pdf_to_text(file2)

            similarity = similarity_ratio(text1, text2)

            print(f"Comparing {pdf_files[i]} and {pdf_files[j]}:")
            print(f"Similarity Ratio: {similarity:.2%}")
            print("=" * 50)

if __name__ == "__main__":
    pdf_directory = "path_to_directory_containing_pdfs"
    check_plagiarism(pdf_directory)
