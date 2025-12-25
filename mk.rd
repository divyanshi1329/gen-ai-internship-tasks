# AI Video Generation Tool – Internship Assignment Report  
**Name:** Divyanshi  
**Date:** (Today’s date)  
**Duration:** ~1 day  
**Tech Stack:** Python, NewsAPI, Pexels API, OpenAI (optional), gTTS, MoviePy, Streamlit  

---

## 1. Objective
The objective of this project is to build an AI-based tool that automatically generates short videos (30–60 seconds) from trending news articles.  
The tool fetches trending news, generates a script, downloads relevant images, generates narration audio, and compiles everything into a video with text overlays.

---

## 2. Pipeline Overview
The pipeline follows these steps:

1. **Fetch trending news articles** (NewsAPI)  
2. **Extract full article content** (newspaper3k)  
3. **Generate a short script** (OpenAI API + fallback)  
4. **Fetch relevant images** (Pexels API)  
5. **Generate voiceover audio** (gTTS)  
6. **Generate final video** (MoviePy: slideshow + captions + voiceover)

---

## 3. Step-by-Step Implementation

### Step 1: Scraping Trending News Articles (NewsAPI)
- Used `NewsAPI /top-headlines` endpoint.
- Extracted Title, Description, URL, Published Date and Source.
- Saved output in:
  - `output/trending_news.json`

**Module:** `modules/fetch_news.py`

---

### Step 2: Extract Full Article Text
- Extracted full article content using `newspaper3k`.
- Saved enriched data containing full text and metadata:
  - `output/trending_news_with_text.json`

**Module:** `modules/extract_article.py`

---

### Step 3: Script Generation (OpenAI + Fallback)
- Used OpenAI model `gpt-4o-mini` to generate a 30–60 sec spoken narration script.
- Due to quota limits, a fallback script generator was implemented for uninterrupted execution.
- Saved output scripts:
  - `output/scripts.json`

**Module:** `modules/script_generator.py`

---

### Step 4: Image Collection (Pexels API)
- Used Pexels API to fetch images related to each news topic.
- Stored images locally per article:
  - `assets/images/{index}/image_1.jpg ...`
- Metadata saved in:
  - `output/image_metadata.json`

**Module:** `modules/image_fetcher.py`

---

### Step 5: Voiceover Generation (gTTS)
- Converted generated scripts to audio narration (MP3) using `gTTS`.
- Saved output:
  - `assets/audio/{index}/voice.mp3`
- Metadata saved:
  - `output/voice_metadata.json`

**Module:** `modules/tts_generator.py`

---

### Step 6: Video Generation (MoviePy)
- Created a video slideshow from images.
- Added text overlay captions based on script chunks.
- Synced audio narration to match total duration.
- Saved videos in:
  - `output/videos/video_{index}.mp4`
- Metadata saved:
  - `output/video_outputs.json`

**Module:** `modules/video_builder.py`

---

## 4. Output / Results
The system generated multiple 30–60 second videos based on trending news topics.

Generated Videos:
- `output/videos/video_0.mp4`
- `output/videos/video_1.mp4`
- `output/videos/video_2.mp4`
(etc.)

---

## 5. Tools & Libraries Used
- **NewsAPI** – trending news source  
- **newspaper3k** – full article extraction  
- **OpenAI API** – script generation (optional with fallback)  
- **Pexels API** – images collection  
- **gTTS** – voiceover text-to-speech  
- **MoviePy + FFmpeg** – video generation  
- **Streamlit** – application UI  

---

## 6. Challenges Faced & Solutions
### 1) OpenAI quota issue
- Encountered API quota error (429 insufficient_quota).
- Implemented fallback script generator.

### 2) MoviePy version mismatch
- `moviepy.editor` not available due to MoviePy v2 changes.
- Updated code to use MoviePy v2 methods:
  - `with_duration`, `with_audio`, `resized`, etc.

---

## 7. Future Improvements
- Use a better TTS engine like ElevenLabs for realistic narration.
- Add background music automatically.
- Use AI video generation tools (Runway/Pika/Luma) for dynamic visuals.
- Add subtitles (.srt generation) and transitions.
- Improve keyword extraction for better image selection.

---

## 8. Conclusion
This tool successfully demonstrates an automated pipeline that scrapes trending news, generates scripts, collects media assets, and produces short AI-generated videos.  
It can be extended further into a full content-generation platform for short video news content.

---
