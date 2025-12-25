import streamlit as st
import json
import os

from modules.fetch_news import fetch_trending_news
from modules.extract_article import extract_full_article
from modules.script_generator import generate_script
from modules.image_fetcher import search_images, download_images
from modules.tts_generator import generate_voiceover
from modules.video_builder import build_video


st.set_page_config(page_title="AI News Video Generator", layout="wide")

st.title("🎥 AI News Video Generator Tool")
st.write("Generate short 30–60 sec videos from trending news articles (NewsAPI + Pexels + TTS + MoviePy).")

# Sidebar inputs
st.sidebar.header("Settings")
category = st.sidebar.selectbox("Select Category", ["technology", "business", "general", "health", "sports"])
country = st.sidebar.selectbox("Select Country", ["us", "in", "gb", "ca", "au"])
num_articles = st.sidebar.slider("Number of articles", 1, 10, 5)

# Fetch news
if st.button("📌 Fetch Trending News"):
    articles = fetch_trending_news(category=category, country=country, page_size=num_articles)
    st.session_state["articles"] = articles
    st.success("✅ Trending news fetched successfully!")

# Show articles
if "articles" in st.session_state:
    articles = st.session_state["articles"]
    st.subheader("📰 Trending Articles")

    selected_index = st.selectbox(
        "Select an article to generate video",
        range(len(articles)),
        format_func=lambda i: articles[i]["title"]
    )

    selected_article = articles[selected_index]

    st.write("### Selected Article")
    st.write("**Title:**", selected_article["title"])
    st.write("**Source:**", selected_article["source"])
    st.write("**Published:**", selected_article["publishedAt"])
    st.write("**Description:**", selected_article["description"])
    st.write("**URL:**", selected_article["url"])

    if st.button("🎬 Generate Video"):
        with st.spinner("Generating video... please wait"):
            # Step 2: Extract full article text
            extracted = extract_full_article(selected_article["url"])
            full_text = extracted.get("full_text")

            # Step 3: Script generation
            script = generate_script(
                title=selected_article["title"],
                description=selected_article["description"],
                full_text=full_text,
                duration_seconds=45
            )

            st.write("## 📝 Generated Script")
            st.write(script)

            # Step 4: Fetch images
            query = " ".join(selected_article["title"].split()[:4])
            images = search_images(query=query, per_page=8)
            images_dir = "assets/images/ui"
            downloaded_paths = download_images(images, images_dir)

            st.write("## 🖼️ Downloaded Images")
            cols = st.columns(4)
            for idx, img_path in enumerate(downloaded_paths[:8]):
                cols[idx % 4].image(img_path)

            # Step 5: Voiceover
            audio_path = "assets/audio/ui/voice.mp3"
            generate_voiceover(script, audio_path)

            st.write("## 🎙️ Voiceover")
            st.audio(audio_path)

            # Step 6: Video build
            video_output = "output/videos/ui_generated_video.mp4"
            build_video(images_dir, audio_path, script, video_output)

            st.write("## ✅ Final Video")
            st.video(video_output)

        st.success("🎉 Video generated successfully!")
