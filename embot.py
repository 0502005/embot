import random
import json
import os
from atproto import Client
from dotenv import load_dotenv

load_dotenv()  # Load .env file

USERNAME = os.getenv("BSKY_USERNAME")
PASSWORD = os.getenv("BSKY_PASSWORD")

#client=Client()
#client.login(USERNAME, PASSWORD)
#print("Logged in as", client.me)

def load_poems():
    with open('emily-dickinson.json', 'r', encoding='utf-8') as f:
        poems = json.load(f)
    return poems

def pick_poem(poems):
    return random.choice(poems)['content'].strip()

def post_poem(poem):
    client = Client()
    client.login(USERNAME, PASSWORD)
    if len(poem) > 300:
        poem = poem[:297] + '...'
    client.send_post(poem)

if __name__ == '__main__':
    poems = load_poems()
    poem = pick_poem(poems)
    post_poem(poem)
