import os
import json

from modules.fetch_news import fetch_trending_news
from modules.extract_article import extract_full_article
from modules.script_generator import generate_script
from modules.image_fetcher import search_images, download_images
from modules.tts_generator import generate_voiceover
from modules.video_builder import build_video



if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    # -------------------------
    # STEP 1: Fetch Trending News
    # -------------------------
    print("📌 Step 1: Fetching trending news...")
    articles = fetch_trending_news(category="technology", country="us", page_size=5)

    with open("output/trending_news.json", "w") as f:
        json.dump(articles, f, indent=2)

    print("✅ Saved: output/trending_news.json")

    # -------------------------
    # STEP 2: Extract Full Article Text
    # -------------------------
    print("\n📌 Step 2: Extracting full article text from URLs...")
    enriched_articles = []

    for i, article in enumerate(articles):
        print(f"➡️ Extracting ({i+1}/{len(articles)}): {article['title'][:60]}...")
        extracted = extract_full_article(article["url"])
        enriched_article = {**article, **extracted}
        enriched_articles.append(enriched_article)

    with open("output/trending_news_with_text.json", "w") as f:
        json.dump(enriched_articles, f, indent=2)

    print("✅ Saved: output/trending_news_with_text.json")

    # -------------------------
    # STEP 3: Generate Scripts using OpenAI
    # -------------------------
    print("\n📌 Step 3: Generating scripts using OpenAI...")
    scripts = []

    for i, article in enumerate(enriched_articles):
        print(f"✍️ Script ({i+1}/{len(enriched_articles)}): {article['title'][:60]}...")

        script = generate_script(
            title=article["title"],
            description=article["description"],
            full_text=article.get("full_text"),
            duration_seconds=45
        )

        scripts.append({
            "title": article["title"],
            "url": article["url"],
            "script": script
        })

    with open("output/scripts.json", "w") as f:
        json.dump(scripts, f, indent=2)

    print("✅ Saved: output/scripts.json")

    

print("\n📌 Step 4: Fetching images from Pexels...")

# Load scripts output
with open("output/scripts.json", "r") as f:
    scripts = json.load(f)

image_metadata = []

for i, item in enumerate(scripts):
    title = item["title"]

    # Use first few words of title as query keyword
    query = " ".join(title.split()[:4])  # simple keyword extraction

    print(f"🖼️ Fetching images ({i+1}/{len(scripts)}): {query}")

    try:
        images = search_images(query=query, per_page=8)
        save_dir = f"assets/images/{i}"
        downloaded_paths = download_images(images, save_dir)

        image_metadata.append({
            "title": title,
            "query": query,
            "images": images,
            "downloaded_paths": downloaded_paths
        })

    except Exception as e:
        print(f"⚠️ Failed for {query}: {e}")

# Save metadata
os.makedirs("output", exist_ok=True)
with open("output/image_metadata.json", "w") as f:
    json.dump(image_metadata, f, indent=2)

print("\n✅ Saved: output/image_metadata.json")
print("✅ Images downloaded into assets/images/")




print("\n📌 Step 5: Generating voiceovers using gTTS...")

# Load scripts
with open("output/scripts.json", "r") as f:
    scripts = json.load(f)

voice_metadata = []

for i, item in enumerate(scripts):
    script_text = item["script"]

    save_path = f"assets/audio/{i}/voice.mp3"
    print(f"🎙️ Generating voiceover ({i+1}/{len(scripts)})...")

    try:
        audio_path = generate_voiceover(script_text, save_path)

        voice_metadata.append({
            "title": item["title"],
            "audio_path": audio_path
        })

    except Exception as e:
        print(f"⚠️ Failed voiceover generation for {item['title']}: {e}")

# Save metadata
with open("output/voice_metadata.json", "w") as f:
    json.dump(voice_metadata, f, indent=2)

print("\n✅ Saved: output/voice_metadata.json")
print("✅ Voiceovers saved inside assets/audio/")




print("\n📌 Step 6: Building videos using MoviePy...")

# Load scripts
with open("output/scripts.json", "r") as f:
    scripts = json.load(f)

video_outputs = []

for i, item in enumerate(scripts):
    print(f"🎬 Generating video ({i+1}/{len(scripts)})...")

    images_dir = f"assets/images/{i}"
    audio_path = f"assets/audio/{i}/voice.mp3"
    script_text = item["script"]

    output_video_path = f"output/videos/video_{i}.mp4"

    try:
        result_path = build_video(
            images_dir=images_dir,
            audio_path=audio_path,
            script=script_text,
            output_path=output_video_path
        )

        video_outputs.append({
            "title": item["title"],
            "video_path": result_path
        })

    except Exception as e:
        print(f"⚠️ Failed video generation for {item['title']}: {e}")

# Save final metadata
with open("output/video_outputs.json", "w") as f:
    json.dump(video_outputs, f, indent=2)

print("\n✅ Saved: output/video_outputs.json")
print("✅ Videos saved inside output/videos/")


