import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import PyPDF2
import os
from difflib import SequenceMatcher
from PIL import ImageTk, Image


def pdf_to_text(pdf_path):
    pdf_text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()
    except Exception as e:
        messagebox.showerror("Error", f"Error extracting text from {pdf_path}: {e}")
    return pdf_text

def similarity_ratio(text1, text2):
    similarity = SequenceMatcher(None, text1, text2).ratio()
    return similarity

def check_plagiarism(pdf_dir):
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    num_files = len(pdf_files)

    if num_files < 2:
        messagebox.showinfo("Info", "There are not enough PDF files to compare.")
        return

    for i in range(num_files):
        for j in range(i + 1, num_files):
            file1 = os.path.join(pdf_dir, pdf_files[i])
            file2 = os.path.join(pdf_dir, pdf_files[j])

            text1 = pdf_to_text(file1)
            text2 = pdf_to_text(file2)

            similarity = similarity_ratio(text1, text2)

            result_text = f"Comparing {pdf_files[i]} and {pdf_files[j]}:\n"
            result_text += f"Similarity Ratio: {similarity:.2%}\n"
            result_text += "=" * 50

            result_label.config(text=result_label.cget("text") + "\n" + result_text)

def browse_directory():
    pdf_directory = filedialog.askdirectory()
    if pdf_directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, pdf_directory)

def start_plagiarism_check():
    pdf_directory = directory_entry.get()
    check_plagiarism(pdf_directory)

# Create the main window
root = tk.Tk()
root.title("Copy Detective")

# Create and configure widgets
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

title_label = tk.Label(frame, text="Assignment Plagiarism Checker", font=("Helvetica", 16))
title_label.pack()

directory_label = tk.Label(frame, text="Select Assignment Directory:")
directory_label.pack()

directory_entry = tk.Entry(frame)
directory_entry.pack()

browse_button = tk.Button(frame, text="Browse", command=browse_directory)
browse_button.pack()

check_button = tk.Button(frame, text="Check Plagiarism", command=start_plagiarism_check)
check_button.pack()

result_label = tk.Label(frame, text="", justify="left")
result_label.pack()

root.mainloop()
