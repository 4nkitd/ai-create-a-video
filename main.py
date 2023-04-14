import requests
import openai
#---------------------------   
import re, os
from requests import get
import urllib.request
from gtts import gTTS
from moviepy.editor import *

API_KEY="##################"
NEWS_API_KEY = "###################48b2a"

openai.api_key = API_KEY

# define a function to get latest news stories about tech from the new api
def get_news():
    response = []
    _api_url = "https://newsapi.org/v2/top-headlines?language=en&sortBy=popularity&apiKey=" + NEWS_API_KEY
    return http_get(_api_url, None).json()

def http_post(_url, _data, _headers):
    try:
        response = requests.post(_url, data=_data, headers=_headers)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

def http_get(_url, _headers):
    try:
        response = requests.get(_url, headers=_headers)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

#---------------------------------------------------------------------------------------------------------------------------

# use chatgpt to generate a video script for the news story in MKBHD style
def generate_video_script(news_stories):
    prompt = "Write a script for a video about the following news story: "
    for story in news_stories["articles"]:
        prompt += story["title"] + " "
    prompt += " in MKBHD style."

    model_engine = "text-davinci-003" #gpt-3.5-turbo

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Print the generated text
    generated_text = completions.choices[0].text

    return generated_text


if __name__ == "__main__":
    text = ""
    # try:

        #Create Necessary Folders
        # os.makedirs("audio")
        # os.makedirs("images")
        # os.makedirs("videos")
        
    articles_resp = get_news()
    topics = []
    for story in articles_resp["articles"]:
        topics += str(story["title"]) + " "

    text = generate_video_script(topics)

    # except Exception as e:
    #     print(e)
    #     exit(1)
    #         # read all context of a file
    #     # with open("script.txt", "r") as f:
    #     #     text = f.read()
    print(text)
    exit(10)

    # Split the text by , and .
    paragraphs = re.split(r"[,.]", text)



    # Loop through each paragraph and generate an image for each
    i=1
    for para in paragraphs[:-1]:
        that_para = para.strip()
        response = openai.Image.create(
            prompt=para.strip(),
            n=1,
            size="1024x1024"
        )
        print("Generate New AI Image From Paragraph...")
        image_url = response['data'][0]['url']
        urllib.request.urlretrieve(image_url, f"images/image{i}.jpg")
        print("The Generated Image Saved in Images Folder!")

        # Create gTTS instance and save to a file
        tts = gTTS(text=para, lang='en', slow=False)
        tts.save(f"audio/voiceover{i}.mp3")
        print("The Paragraph Converted into VoiceOver & Saved in Audio Folder!")

        # Load the audio file using moviepy
        print("Extract voiceover and get duration...")
        audio_clip = AudioFileClip(f"audio/voiceover{i}.mp3")
        audio_duration = audio_clip.duration

        # Load the image file using moviepy
        print("Extract Image Clip and Set Duration...")
        image_clip = ImageClip(f"images/image{i}.jpg").set_duration(audio_duration)

        # Use moviepy to create a text clip from the text
        print("Customize The Text Clip...")
        text_clip = TextClip(that_para, fontsize=50, color="white")
        text_clip = text_clip.set_pos('center').set_duration(audio_duration)

        # Use moviepy to create a final video by concatenating
        # the audio, image, and text clips
        print("Concatenate Audio, Image, Text to Create Final Clip...")
        clip = image_clip.set_audio(audio_clip)
        video = CompositeVideoClip([clip, text_clip])

        # Save the final video to a file
        video = video.write_videofile(f"videos/video{i}.mp4", fps=24)
        print(f"The Video{i} Has Been Created Successfully!")
        i+=1


    clips = []
    l_files = os.listdir("videos")
    for file in l_files:
        clip = VideoFileClip(f"videos/{file}")
        clips.append(clip)

    print("Concatenate All The Clips to Create a Final Video...")
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.write_videofile("final_video.mp4")
    print("The Final Video Has Been Created Successfully!")