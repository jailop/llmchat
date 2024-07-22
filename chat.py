#!/usr/bin/env python3


import sys
import os
import rlcompleter
import readline
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
from config import *

def read_input():
    try:
        a = input("> ")
    except EOFError:
        sys.exit(0)
    return a

readline.parse_and_bind("tab: complete")
if os.path.exists(QUESTION_HISTORY):
    readline.read_history_file(QUESTION_HISTORY)
readline.set_auto_history(True)

client = OpenAI(api_key=API_KEY)
console = Console()

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r', encoding='utf-8') as fd:
        console.print(Markdown(fd.read()))

conversation = [{
    "role": "system",
    "content": "DIRECTIVE_FOR_gpt-3.5-turbo",
}]

message = {
    "role":"user",
    "content": read_input(),
}

while (message["content"] != "###"):
    conversation.append(message)
    completion = client.chat.completions.create(
        model=AI_MODEL,
        messages=conversation
    )
    content = completion.choices[0].message.content
    print()
    console.print(Markdown(content))
    print()
    with open("log.txt", "a", encoding="utf-8") as fd:
        fd.write(f"\n{message['content']}\n")
        fd.write(f"\n{content}\n")
    message["content"] = read_input()
    print()
    conversation.append(completion.choices[0].message)
    readline.write_history_file("history.txt")

