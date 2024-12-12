from flask import render_template, request, session, redirect, url_for, flash, Blueprint
import fitz  # pymupdf
import os
import sys
sys.path.append(os.path.abspath("QA"))

from qa_system import process_questions


# Initialize Flask app
app_qa = Blueprint('app_qa', __name__)



def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


@app_qa.route('/question_answering', methods=['GET', 'POST'])
def index():
    answers = []  # Store answers for multiple questions
    questions_input = []  # Store questions input from textarea
    context = session.get('context', '')  # Get context from session

    if request.method == 'POST':
        # Check if a PDF file was uploaded
        if 'pdf' in request.files and request.files['pdf'].filename != '':
            pdf_file = request.files['pdf']
            pdf_path = os.path.join('uploaded.pdf')

            # Save the uploaded PDF file temporarily
            pdf_file.save(pdf_path)

            # Extract text from the uploaded PDF and store it in session
            context = extract_text_from_pdf(pdf_path)
            session['context'] = context  # Store the context in session
            session['pdf_uploaded'] = True  # Flag indicating a PDF has been uploaded

            flash("Success!", "success")

        # Get pasted text input
        pasted_text = request.form.get('input_text', '').strip()

        # Use pasted text as context if provided
        if pasted_text:
            context = pasted_text
            session['context'] = context  # Store the pasted text in session
            session['pdf_uploaded'] = False  # Flag indicating no PDF is uploaded

        # Get questions input from the textarea
        questions_input = request.form.getlist('questions')

        # Process questions only if there's context (from PDF or pasted text)
        if questions_input:
            if context:
                answers = process_questions(questions_input, context)

    return render_template('qa.html', questions=questions_input, answers=answers, context=context)


@app_qa.route('/reset', methods=['POST'])
def reset():
    """Reset the session for a new PDF upload or text input."""
    session.clear()  # Clear all session data
    flash("Session has been reset. You can upload a new PDF or paste text.", "info")
    return redirect(url_for('app_qa.index'))  # Correct the endpoint name here

