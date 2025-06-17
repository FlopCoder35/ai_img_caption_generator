# 📸 AI Image Caption Generator

A Python application that generates creative and descriptive captions for images using Hugging Face's **BLIP** model. Built as part of an AI assignment to explore multimodal AI and content automation basics.

---

## 🚀 Features

### ✅ Core Features
- Supports common image formats: **JPG, PNG**
- Automatically **resizes images** for optimal model input
- **Batch processing** of multiple images
- **Memory-efficient** loading using PIL
- Uses **Hugging Face's BLIP model** for caption generation
- Handles **multiple image types**: nature, products, people, etc.
- Saves outputs in both **CSV** and **JSON**
- Generates a **summary report** of performance

### 💎 Bonus Features
- **Drag-and-drop web interface** via Gradio
- **Instagram-ready captions** with hashtags (optional)
- Clean, modular code
- Performance metrics: total time, per-image processing time

---

## 🖼️ Sample Outputs

| Image Type | Caption |
|------------|---------|
| Landscape  | *"a dock sitting on top of a lake under a full moon"* |
| Animal     | *"an elephant standing in the middle of a field"* |
| People     | *"a man working on a laptop computer"* |
| Abstract   | *"a silhouette of a woman holding a flute in front of a full moon"* |

> More than **10 sample images** were processed. Check `output/` for JSON and CSV results.

---



## 🚀 Getting Started

### 1. Clone the project
git clone https://github.com/yourname/image-caption-generator.git  
cd image-caption-generator

### 2. Set up virtual environment

#### Windows:
python -m venv venv  
venv\Scripts\activate

#### Linux/macOS:
python3 -m venv venv  
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. 🧠 Run the Application

**Start Gradio Interface**  
python caption_generate.py

**Run in Batch Mode**  
python caption_generate.py --batch

---

