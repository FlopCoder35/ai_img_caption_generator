import os
import json
import csv
import time
from PIL import Image, UnidentifiedImageError, ImageDraw, ImageFont
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# ========== CONFIG ==========
IMAGE_FOLDER = "sample_images"
OUTPUT_FOLDER = "captioned_images"
CSV_FILE = "captions.csv"
JSON_FILE = "captions.json"
IMAGE_SIZE = (384, 384)
STYLES = ["default", "creative", "factual"]
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Change this for Windows if needed

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
    else:  # default
        out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

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
    except IOError:
        font = ImageFont.load_default()
    text_position = (10, 10)
    draw.text(text_position, caption, font=font, fill="white")
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

        image_path = os.path.join(IMAGE_FOLDER, filename)
        try:
            image = Image.open(image_path).convert("RGB")
        except UnidentifiedImageError:
            print(f"❌ Unable to process: {filename}")
            continue

        caption = generate_caption(image, style="creative")
        hashtags = suggest_hashtags(caption)
        caption_with_tags = f"{caption} {' '.join(hashtags)}"
        image_with_caption = overlay_caption(image.copy(), caption)

        # Save captioned image
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        image_with_caption.save(output_path)

        # Save metadata
        data.append({
            "filename": filename,
            "caption": caption,
            "hashtags": hashtags
        })

        print(f"✅ Processed: {filename} | Caption: {caption}")
        total += 1

    # Write CSV
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "caption", "hashtags"])
        writer.writeheader()
        for row in data:
            writer.writerow({
                "filename": row["filename"],
                "caption": row["caption"],
                "hashtags": ', '.join(row["hashtags"])
            })

    # Write JSON
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    total_time = time.time() - start_time
    print("\n✅ Bulk Processing Summary:")
    print(json.dumps({
        "total_images": total,
        "total_time_sec": round(total_time, 2),
        "avg_time_per_image_sec": round(total_time / max(total, 1), 2)
    }, indent=4))

# ========== RUN ==========
if __name__ == "__main__":
    process_images()
