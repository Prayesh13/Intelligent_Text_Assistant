import os
from flask import Flask, request, render_template, Blueprint
from Image_caption.caption import generate_caption

app_caption = Blueprint('app_caption', __name__)

@app_caption.route('/')
def index():
    return render_template('caption.html')

@app_caption.route('/generate_caption', methods=['GET','POST'])
def generate_caption_view():
    caption = None
    error = None

    # Check if an image was uploaded
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        image_path = os.path.join("uploads", file.filename)
        file.save(image_path)

        # Generate a caption for the uploaded image
        caption = generate_caption(image_path)

        # Optionally, remove the uploaded image file after processing
        os.remove(image_path)
    else:
        error = "Please upload an image file."

    return render_template('caption.html', caption=caption, error=error)

os.makedirs("uploads", exist_ok=True)
