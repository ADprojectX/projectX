from discoart import create
import os
da = create(
    text_prompts='A painting of sea cliffs in a tumultuous storm, Trending on ArtStation.',
    init_image='https://d2vyhzeko0lke5.cloudfront.net/2f4f6dfa5a05e078469ebe57e77b72f0.png',
    skip_steps=100,
)

da[0].chunks.save_gif(
    f'{os.getcwd()}/lighthouse.gif', show_index=True, inline_display=True, size_ratio=0.5
)