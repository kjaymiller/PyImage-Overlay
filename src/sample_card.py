from operator import index
from tkinter import font
import click

from image import ImageCard

# CLI wrapper for ImageCard
# `python .\src\sample_card.py --image="computer.png"`

@click.command()
@click.option('--image')
@click.option('--out-path', default = "test.png", 
                help = 'where to save the output image')
@click.option('--text', default = "This is a test", 
                help = "text to put on the image")
@click.option('--index', default = "1", help="Day number of the card")
@click.option('--campaign', default = "#31DaysofNeurodivergence",
                help = "tagline for the bottom of the card")
def create_card(image : str, out_path : str, text : str, index : int, campaign : str):
    card = ImageCard(image)
    card.draw_scaled_text(f"#{index}", scale = (0.05,0.05), pos=(0.05, 0.1), 
                          font_face="assets/Lato-BoldItalic.ttf")
    card.draw_scaled_text(text, scale = (0.9,0.6), pos=(0.1, 0.12), 
                          font_face="assets/Lato-BoldItalic.ttf")
    card.draw_scaled_text(campaign, scale = (0.1,0.05), pos=(0.3, 0.9),
                          font_face="assets/Lato-BoldItalic.ttf")
    card.render_card().save(out_path)

if __name__ == '__main__':
    create_card()
