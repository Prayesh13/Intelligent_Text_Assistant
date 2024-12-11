import os
from flask import Flask, request, render_template, Blueprint
from Summarization.summarization import summarize_text, extract_text_from_pdf

app_summary = Blueprint('app_summary', __name__)

@app_summary.route('/')
def index():
    return render_template('summary.html')

@app_summary.route('/summarize', methods=['POST'])
def summarize():
    text = None
    summary = None
    error = None

    # Check if a file was uploaded
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        pdf_path = os.path.join("uploads", file.filename)
        file.save(pdf_path)

        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(pdf_path)

        # Optionally, remove the uploaded PDF file after processing
        os.remove(pdf_path)
    elif 'text' in request.form and request.form['text'].strip() != '':
        # If text is provided directly
        text = request.form['text']
    else:
        error = "Please upload a PDF file or enter text."

    if text:
        # Summarize the extracted text or entered text
        summary = summarize_text(text)

    return render_template('summary.html',summary=summary, error=error)

os.makedirs("uploads", exist_ok=True)
