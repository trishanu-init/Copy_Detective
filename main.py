import os
import PyPDF2
from difflib import SequenceMatcher
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

# Function to calculate text similarity using SequenceMatcher
def text_similarity(text1, text2):
    text1 = text1.lower()
    text2 = text2.lower()
    seq_matcher = SequenceMatcher(None, text1, text2)
    return seq_matcher.ratio()

# Function to preprocess text (tokenization and removal of stopwords)
def preprocess_text(text):
    tokens = word_tokenize(text)
    stopwords_set = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stopwords_set]
    return ' '.join(tokens)

# Main function to check for plagiarism
def check_plagiarism(main_pdf_path, pdf_directory):
    main_text = extract_text_from_pdf(main_pdf_path)
    main_text = preprocess_text(main_text)

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            other_text = extract_text_from_pdf(pdf_path)
            other_text = preprocess_text(other_text)

            similarity = text_similarity(main_text, other_text)

            print(f"Similarity with {filename}: {similarity * 100:.2f}%")

if __name__ == "__main__":
    main_pdf_path = "main_document.pdf"  # Path to the main PDF document
    pdf_directory = "pdf_files"  # Directory containing other PDF files to compare

    check_plagiarism(main_pdf_path, pdf_directory)
