import contextlib

import gradio as gr
from modules import scripts

import requests


def fetchTags(ch, art_box, char_box):
    if ch:
        try:
            if "danbooru.donmai.us/posts" not in ch:
                return "unsupported url"
            url = ch + ".json"

            with requests.get(url, headers={
                'user-agent': 'my-app/0.0.1'}) as r:  # it needs a user agent otherwise it doesn't work
                data = r.json()
                artist = data["tag_string_artist"]
                char = data["tag_string_character"]
                general_tags = data["tag_string_general"]

            format_tags = ""

            if art_box:
                format_tags += artist
            if char_box:
                if not art_box:
                    format_tags += char
                else:
                    format_tags += " " + char

            format_tags += " " + general_tags

            return format_tags.replace(" ", ", ")




        except Exception as err:
            # most likely an bad url
            return "Incomplete url OR unsupported url"
    else:
        return []


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
                link = gr.Textbox(label="insert link")

                with gr.Row():
                    includeartist = gr.Checkbox(value=True, label="Include artist tags in tag string", interactive=True)
                    includecharacter = gr.Checkbox(value=True, label="Include character tags in tag string",
                                                   interactive=True)

        with contextlib.suppress(AttributeError):
            if is_img2img:
                fetch_tags.click(fn=fetchTags, inputs=[link, includeartist, includecharacter], outputs=[self.boxxIMG])
            else:
                fetch_tags.click(fn=fetchTags, inputs=[link, includeartist, includecharacter], outputs=[self.boxx])

        return [link, fetch_tags, includeartist, includecharacter]

    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_prompt":
            self.boxx = component
        if kwargs.get("elem_id") == "img2img_prompt":
            self.boxxIMG = component
