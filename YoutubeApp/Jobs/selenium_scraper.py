import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import openai
from dotenv import load_dotenv, find_dotenv
import os
import requests
import xml.etree.ElementTree as ET



def summary(text):
    load_dotenv(find_dotenv())
    openai.organization = os.environ.get("OPENAI_ORG")
    openai.api_key = os.environ.get("OPENAI_KEY")
    result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {"role":"system","content":"You are a helpful assistant"},
        {"role":"user","content":f"Summarize the video transcript in 150 words: {text} "}
    ]

    )
    return result


   
def ToText(element:ET.Element):

    return element.text
def youtube_trans_requests(url:str):

    with requests.session() as http_client:
        value = http_client.get(url)
        
        split_value = value.text.split('"captions":')
        captions_json = json.loads(
            split_value[1].split(',"videoDetails')[0].replace('\n', '')
        )
        urls =captions_json["playerCaptionsTracklistRenderer"]["captionTracks"][0]["baseUrl"]

        transcript=http_client.get(urls)
        tree = ET.fromstring(transcript.text)
        text_iter = tree.findall(".//text")


        
        for text in text_iter:
            print(text.text)
        list_of_text = ' '.join(list(map(ToText,text_iter)))

        return list_of_text
