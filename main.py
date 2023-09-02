import os
import PyPDF2
from difflib import SequenceMatcher
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from flask import Flask, request, render_template, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = '6772'  # Replace with a secure secret key

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

    results = []

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            other_text = extract_text_from_pdf(pdf_path)
            other_text = preprocess_text(other_text)

            similarity = text_similarity(main_text, other_text)

            results.append((filename, similarity))

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the PDF file uploads
        reference_pdf = request.files['reference_pdf']
        pdf_directory = 'pdfs'
        
        if reference_pdf and reference_pdf.filename.endswith('.pdf'):
            reference_pdf.save(os.path.join('uploads', 'reference_doc.pdf'))

            # Run the plagiarism check
            results = check_plagiarism(os.path.join('uploads', 'reference_doc.pdf'), pdf_directory)

            return render_template('result.html', results=results)
        else:
            flash('Please upload a valid PDF file.')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
