# image_caption_generator.py
import os
import json
import csv
import time
from PIL import Image, UnidentifiedImageError, ImageDraw, ImageFont
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import gradio as gr

# ========== CONFIG ==========
IMAGE_FOLDER = "sample_images"
OUTPUT_FOLDER = "captioned_images"
CSV_FILE = "captions.csv"
JSON_FILE = "captions.json"
IMAGE_SIZE = (384, 384)
FONT_PATH = "arial.ttf"  # Update for system if needed

# ========== SETUP MODEL ==========
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# ========== FUNCTION TO GENERATE CAPTION ==========
def generate_caption(image: Image.Image, style="default") -> str:
    image = image.resize(IMAGE_SIZE)
    inputs = processor(images=image, return_tensors="pt").to(device)
    if style == "creative":
        out = model.generate(**inputs, num_beams=3, max_length=30, do_sample=True, top_k=50)
    elif style == "factual":
        out = model.generate(**inputs, num_beams=5, max_length=20)
    else:
        out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

# ========== HASHTAG SUGGESTION ==========
def suggest_hashtags(caption: str) -> list:
    keywords = caption.lower().split()
    hashtags = [f"#{word.strip(',.!?')}" for word in keywords if word.isalpha()]
    return hashtags[:5]

# ========== OVERLAY CAPTION ON IMAGE ==========
def overlay_caption(image: Image.Image, caption: str) -> Image.Image:
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(FONT_PATH, 18)
    except:
        font = ImageFont.load_default()
    draw.text((10, 10), caption, font=font, fill="white")
    return image

# ========== MAIN BULK PROCESSOR ==========
def process_images():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    data = []
    start_time = time.time()
    total = 0

    for filename in os.listdir(IMAGE_FOLDER):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(IMAGE_FOLDER, filename)
        try:
            image = Image.open(path).convert("RGB")
        except UnidentifiedImageError:
            print(f"❌ {filename} is not a valid image.")
            continue

        caption = generate_caption(image, style="creative")
        hashtags = suggest_hashtags(caption)
        captioned = overlay_caption(image.copy(), caption)

        # Save image and data
        captioned.save(os.path.join(OUTPUT_FOLDER, filename))
        data.append({"filename": filename, "caption": caption, "hashtags": hashtags})

        print(f"✅ {filename} | {caption}")
        total += 1

    # Export CSV
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "caption", "hashtags"])
        writer.writeheader()
        for row in data:
            writer.writerow({"filename": row["filename"], "caption": row["caption"], "hashtags": ', '.join(row["hashtags"])})

    # Export JSON
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print("\n📊 Summary:")
    print(json.dumps({
        "total_images": total,
        "total_time_sec": round(time.time() - start_time, 2),
        "avg_time_per_image_sec": round((time.time() - start_time) / max(total, 1), 2)
    }, indent=4))

# ========== GRADIO INTERFACE (Bonus Feature) ==========
def gradio_caption(image, style):
    pil_image = Image.fromarray(image).convert("RGB")
    caption = generate_caption(pil_image, style)
    hashtags = suggest_hashtags(caption)
    return f"{caption}\n\nSuggested Hashtags: {' '.join(hashtags)}"

gr.Interface(
    fn=gradio_caption,
    inputs=[gr.Image(type="numpy"), gr.Radio(["default", "creative", "factual"], label="Caption Style")],
    outputs="text",
    title="BLIP Image Caption Generator",
    description="Upload an image and get a creative caption with hashtags."
).launch(share=True)

# ========== RUN CLI ==========
if __name__ == "__main__":
    process_images()
