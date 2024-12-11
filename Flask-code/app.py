from flask import (
    Flask,
    render_template, redirect, url_for,
    flash, request, session
)
from Summarization.summary_app import app_summary
from QA.qa_app import app_qa
from Image_caption.caption_app import app_caption
from Translation.translation_app import app_translation

# Use the Framework
app = Flask(__name__)
app.config["SECRET_KEY"] = "ITA_SECRETE_KEY"

app.register_blueprint(app_summary, url_prefix="/summarize")
app.register_blueprint(app_qa, url_prefix="/question_answering")
app.register_blueprint(app_caption, url_prefix="/generate_caption")
app.register_blueprint(app_translation, url_prefix="/translate")


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/select_option", methods=["GET", "POST"])
def select_option():
    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option == "qa_system":
            return redirect(url_for("app_qa.index"))  # Redirect to QA System
        elif selected_option == "summarization":
            return redirect(url_for("app_summary.index"))  # Redirect to Summarization
        elif selected_option == "image_captioning":
            return redirect(url_for("app_caption.index"))
        elif selected_option == "translation":
            return redirect(url_for("app_translation.index"))

    return render_template("select_option.html")


if __name__ == "__main__":
    app.run(debug=True,port=7000)
