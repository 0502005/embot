import random
import json
import os
from atproto import Client
from dotenv import load_dotenv
import time

load_dotenv()

USERNAME = os.getenv("BSKY_USERNAME")
PASSWORD = os.getenv("BSKY_PASSWORD")

MAX_LENGTH = 300

def load_poems():
    with open('emily-dickinson.json', 'r', encoding='utf-8') as f:
        poems = json.load(f)
    return poems

def pick_poem(poems):
    return random.choice(poems)

def split_poem(poem_text, reserve_chars=0):
    lines = poem_text.strip().split('\n')
    parts = []
    current_part = ''

    for line in lines:
        next_part = current_part + ('\n' if current_part else '') + line
        if len(next_part) <= MAX_LENGTH - reserve_chars:
            current_part = next_part
        else:
            parts.append(current_part)
            current_part = line

    if current_part:
        parts.append(current_part)

    return parts

def add_numbering_if_needed(parts):
    if len(parts) <= 1:
        return parts  # No need to number a single post

    total = len(parts)
    numbered_parts = [
        f"({i+1}/{total})\n{part}" for i, part in enumerate(parts)
    ]
    return numbered_parts

def post_poem_thread(poem_parts):

    client = Client()
    client.login(USERNAME, PASSWORD)

    post_ref = None
    root_ref = None

    for index, part in enumerate(poem_parts):
        if post_ref:
            reply_ref = {
                "$type": "app.bsky.feed.post#replyRef",
                "root": {
                    "cid": root_ref.cid,
                    "uri": root_ref.uri
                },
                "parent": {
                    "cid": post_ref.cid,
                    "uri": post_ref.uri
                }
            }
            post_ref = client.send_post(text=part, reply=reply_ref)
            time.sleep(1)
        else:
            post_ref = client.send_post(text=part)
            time.sleep(1)
            root_ref = post_ref  # set root_ref to the first post

        print(f"Posted part {index + 1}: {post_ref.uri}")



def main():
    poems = load_poems()
    poem_obj = pick_poem(poems)
    title = poem_obj['title']
    content = poem_obj['content']

    full_poem = f"{title}\n\n{content}"

    # Check if we need to reserve characters for numbering
    temp_parts = split_poem(full_poem)
    reserve_chars = 10 if len(temp_parts) > 1 else 0
    poem_parts = split_poem(full_poem, reserve_chars=reserve_chars)

    # Add numbering only if needed
    final_parts = add_numbering_if_needed(poem_parts)

    post_poem_thread(final_parts)

if __name__ == '__main__':
    main()

