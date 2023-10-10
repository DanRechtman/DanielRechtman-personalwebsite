from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import openai
from dotenv import load_dotenv, find_dotenv
import os


def summary(text):
    load_dotenv(find_dotenv())
    openai.organization = os.environ.get("OPENAI_ORG")
    openai.api_key = os.environ.get("OPENAI_KEY")
    # openai.organization = "org-a7vqcLt9m3UhWIu7nYsiSeoI"
    # openai.api_key = "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"
    result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {"role":"system","content":"You are a helpful assistant"},
        {"role":"user","content":f"Summarize the video transcript in 150 words: {text} "}
    ]

)
    return result

def youtube_trans(url:str):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--mute-audio")

    driver = webdriver.Chrome(options)
    driver.delete_all_cookies()
    driver.execute_cdp_cmd(cmd="Network.clearBrowserCache",cmd_args={})

    # ApplicationCache(driver).UNCACHED
    driver.get(url)
    driver.implicitly_wait(30)
    element = driver.find_element(By.CSS_SELECTOR,"#bottom-row #description")
    element.click()

    button_trans = driver.find_element(By.CSS_SELECTOR,"#description-inline-expander [aria-label=\"Show transcript\"]")
    
    button_trans.click()

    transcript = driver.find_elements(By.CSS_SELECTOR,"#segments-container ytd-transcript-segment-renderer")

    listTrans = ""
    for tran in transcript:
        text = tran.get_attribute("innerText")
        strip_text = text[4:].replace("\n","")
        listTrans += strip_text + " "
    driver.close()
    sum = summary(listTrans)

    return sum.choices[0].message.content
   