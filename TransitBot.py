import requests
from bs4 import BeautifulSoup
from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio
import json
import time

from typing import List
from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import PageElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()

class TrafficBot:
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_message(self, message):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
            print("Message sent successfully.")
        except Exception as e:
            print(f"Error sending message: {e}")



class TransitCrawler:
    def __init__(self, url: str):
        self.options = Options()
        # self.options.add_experimental_option("detach", True)
        self.options.add_argument("--headless")
        self.options.add_argument("'--no-sandbox'")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=self.options
        )
        
        self.url = url

    def fetch_html(self) -> None:
        try:
            self.driver.get(self.url)
            # response = requests.get(self.url)
            # response.raise_for_status()  # Raise an HTTPError for bad responses
            # return response.text
            return self.driver.page_source
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching HTML: {e}")
            return None

    def extract_data(self, html_content):
        if html_content is not None:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Customize this part to extract the data you're interested in
            # For example, let's extract all the text from paragraph tags
            paragraphs = soup.find_all('p')
            return [p.get_text() for p in paragraphs]
        else:
            return []

async def main():
    
    target_url = "https://cit.transit.gencat.cat/cit/AppJava/views/incidents.xhtml"
    transit_crawler = TransitCrawler(target_url)
    
    html = transit_crawler.fetch_html()
    data = transit_crawler.extract_data(html)
    print(data)
    
    
    transit_bot = TrafficBot(token=os.getenv("TELEGRAM_BOT_TOKEN"), chat_id=os.getenv("TELEGRAM_CHAT_ID"))
    
    message_text = f"🚦 Traffic Update 🚦\n\n{data}"
    
    await transit_bot.send_message(message_text)  


if __name__ == "__main__":
    asyncio.run(main())
