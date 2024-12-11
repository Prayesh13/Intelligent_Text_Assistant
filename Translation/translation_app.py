import os
from flask import Flask, request, render_template, Blueprint
from Translation.translation import translate_m2m

# Define a blueprint for translation
app_translation = Blueprint('app_translation', __name__)

language_dict = {
    "English": "en",  # English
    "Hindi": "hi",  # Hindi
    "Korean": "ko",  # Korean
    "French": "fr",  # French
    "Spanish": "es",  # Spanish
    "Bengali": "bn",  # Bengali
    "Tamil": "ta",  # Tamil
    "German": "de" # German
}

@app_translation.route('/')
def index():
    # Set default languages
    default_src_lang = "English"
    default_tgt_lang = "Hindi"

    return render_template('translation.html',
                           language_dict=language_dict,
                           default_src_lang=default_src_lang,
                           default_tgt_lang=default_tgt_lang)


@app_translation.route('/translate', methods=['GET', 'POST'])
def translate_view():
    translation = None
    error = None

    if request.method == 'POST':
        text = request.form['text']
        src_lang = request.form.get('src_lang', None)  # Use get() to prevent key errors
        tgt_lang = request.form.get('tgt_lang', None)  # Use get() to prevent key errors

        # Debugging: Print received values
        print(f"Received text: {text}")
        print(f"Source language: {src_lang}")
        print(f"Target language: {tgt_lang}")

        # Ensure that the text is not empty
        if text and src_lang and tgt_lang:
            # Get the language codes from the dictionary
            src_lang_code = language_dict.get(src_lang)
            tgt_lang_code = language_dict.get(tgt_lang)

            # Debugging: Print language codes
            print(f"Source language code: {src_lang_code}")
            print(f"Target language code: {tgt_lang_code}")

            if src_lang_code and tgt_lang_code:
                try:
                    # Perform translation
                    translation = translate_m2m(text, src_lang_code, tgt_lang_code)
                except Exception as e:
                    error = f"Error during translation: {str(e)}"
            else:
                error = "Invalid source or target language selected."
        else:
            error = "Please provide valid text and select source/target languages."

    return render_template('translation.html',
                           translation=translation,
                           error=error,
                           language_dict=language_dict)
