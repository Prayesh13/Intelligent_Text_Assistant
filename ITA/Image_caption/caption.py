from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# MODEL_PATH =
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path):
    """Generate a caption for the provided image."""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=50, num_beams=5)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption
