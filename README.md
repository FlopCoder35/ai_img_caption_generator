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

### 1. Clone the Project
```bash
git clone https://github.com/FlopCoder35/ai_img_caption_generator.git
cd ai_img_caption_generator
```

### 2. Set Up Virtual Environment

#### 🪟 On Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### 🐧 On Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. 🧠 Run the Application

#### ▶️ To start the Gradio interface:
```bash
python caption_generate.py
```

#### 📦 To run in batch mode (for multiple images):
```bash
python caption_generate.py --batch
```

---

## ✅ Features Covered

- 📸 Image Processing & Caption Generation  
- 🌐 Web Interface using Gradio  
- 📂 CSV/JSON Export Support  
- 🧾 Batch Processing Mode  
- 📊 Performance Benchmarks  
- 🧠 Tested on 10+ Image Variations  

---

## 📂 Output

When you run the app:
- 🖼️ Captioned images are displayed or saved
- 🧾 Captions are printed on screen
- 📁 Results can be exported as `.csv` or `.json` (batch mode)

---


