
import gradio as gr
from modules import scripts
from modules import script_callbacks

import requests
from bs4 import BeautifulSoup

def fetchTags(ch):
    if ch:

        page = requests.get(ch)

        soup = BeautifulSoup(page.content, "html.parser")

        info = soup.findAll("a", class_="search-tag")
        tags = [j.text for j in info]

        return  ' ,'.join(tags)
    else:
        return []


def on_ui_settings():
    section = ('booru-link', "Gelbooru-link")


class BooruScript(scripts.Script):
    def __init__(self) -> None:
        super().__init__()

    def title(self):
        return ("Link fetcher")

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("DanBooru Link", open=False):
                fetch_tags = gr.Button(value='Get Tags', variant='primary')
                link= gr.Textbox(label="insert link")
                tags = gr.Textbox(value="", label="Tags", lines=5)

        fetch_tags.click(fn=fetchTags, inputs=[link], outputs=[tags])
        return [link, tags, fetch_tags]


script_callbacks.on_ui_settings(on_ui_settings)

# script_callbacks.on_ui_tabs(on_ui_tabs)
