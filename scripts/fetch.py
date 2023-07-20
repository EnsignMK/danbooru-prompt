import gradio as gr
from modules import scripts


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
                text_box = gr.Textbox(label="tags", lines=5)

            if is_img2img:
                fetch_tags.click(fn=fetchTags, inputs=[link], outputs=[text_box])
            else:
                fetch_tags.click(fn=fetchTags, inputs=[link], outputs=[text_box])

        return [link, fetch_tags]
