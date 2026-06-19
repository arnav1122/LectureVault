from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os
from google import genai
from datetime import datetime
import json

load_dotenv()


def extract_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]
    elif parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    return None
def analyze_video(url):
    try:
        with open("history.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []


    video_id = extract_video_id(url)

    if not video_id:
        raise Exception("Invalid YouTube URL")

    transcript = YouTubeTranscriptApi().fetch(video_id, languages=["hi", "en"])
    print("\nTranscript fetched successfully!\n")

    transcript_text = " ".join([item.text for item in transcript])
    MAX_CHARS = 12000
    transcript_text = transcript_text[:MAX_CHARS]

    client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = f"""
        You are an AI study assistant.

        Analyze the following lecture transcript and return ONLY valid JSON.

        Required format:

        {{
            "title":""(here add video title in short)
            "subject": "",
            "chapter": "",
            "topic": "",
            "key_points": [],
            "next_topic": ""
        }}

        Transcript:

        {transcript_text}
        """

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
            "response_mime_type": "application/json"
        }
    )
    study_data = json.loads(response.text)
    study_data["video_id"] = video_id
    study_data["date"] = datetime.now().strftime("%d-%m-%Y")
    for video in data:
        if video.get("video_id") == video_id:
            print("This video has already been added!")
            exit()

    data.append(study_data)
    with open ("history.json","w") as file:
        json.dump(data, file, indent=4)
    print("added sucessfully")
    return study_data