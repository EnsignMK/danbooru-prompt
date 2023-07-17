import contextlib

import gradio as gr
from modules import scripts
from modules import script_callbacks

import requests
from bs4 import BeautifulSoup

def fetchTags(ch):
    if ch:
        try:
            if "danbooru.donmai.us/posts" not in ch:
                return "unsupported url"
            page = requests.get(ch)

            soup = BeautifulSoup(page.content, "html.parser")

            info = soup.findAll("a", class_="search-tag")
            tags = [j.text for j in info]

            return ' ,'.join(tags)
        except Exception as err:
            # most likely an bad url
            return "Incomplete url OR unsupported url"
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

        with contextlib.suppress(AttributeError):
            if is_img2img:
                fetch_tags.click(fn=fetchTags, inputs=[link], outputs=[self.boxxIMG])
            else:
                fetch_tags.click(fn=fetchTags, inputs=[link], outputs=[self.boxx])



        return [link, fetch_tags]

    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_prompt":
            self.boxx=component
        if kwargs.get("elem_id") == "img2img_prompt":
            self.boxxIMG=component




script_callbacks.on_ui_settings(on_ui_settings)

# script_callbacks.on_ui_tabs(on_ui_tabs)
