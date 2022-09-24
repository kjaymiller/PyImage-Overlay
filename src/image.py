import logging

from PIL import Image, ImageDraw, ImageFont


class ImageCard:
    """Represents an image with text overlayed on it. The required background
    value should be a path to an image file.
    """

    def __init__(self, background: str):
        self.background = Image.open(background)
        self.card_size = self.background.size
        self.canvas = Image.new("RGBA", self.card_size, (0, 0, 0, 0))

    def render_card(self):
        """Composite the background and the canvas together and return
        the image.

        Returns:
            _type_: PIL.Image object.
        """
        self.background.paste(self.canvas, (0, 0), self.canvas)
        return self.background

    def text_bounding_box_size(self,
                               lines: list[str], font) -> tuple[int, int]:
        """Checks the size of a rendered block of text.

        Args:
            lines (list[str]): list of strings that represent lines of text.
            font (_type_): Font object from PIL.ImageFont.

        Returns:
            tuple[int,int]: _description_
        """
        return font.getsize_multiline("\n".join(lines))

    def wrap_text_to_width(self, text: str, font, max_width: int) -> list[str]:
        """Takes a string and a font and returns a list of strings that
        represents lines of text that will fit in the given width when rendered
        in the given font.

        Args:
            text (str): String to be wrapped. Newlines will not be preserved.
            font (_type_): Font object from PIL.ImageFont.
            max_width (int): Width in pixels that the text should be wrapped
            to.

        Returns:
            list[str]: List of strings representing lines of text.
        """
        words = text.split()
        lines = [words[0]]
        for word in words[1:]:
            # try putting this word in last line then measure
            test_lines = lines[:-1] + [" ".join([lines[-1], word])]
            (w, h) = self.text_bounding_box_size(test_lines, font)
            if w > max_width:  # too wide
                # take it back out, put it on the next line
                lines = lines + [word]
            else:
                lines = test_lines
        return lines

    def draw_scaled_text(
        self,
        text: str,
        scale: tuple,
        pos: tuple,
        color: str = "#ffffff",
        font_face: str = "assets/Lato-BoldItalic.ttf",
    ):
        """Takes a text string, scales it to a bounding box and draws it on the
        canvas at a given position.

        Args:
            text (str): Text to draw
            scale (tuple): Size of the bounding box scaled to background size.
                (x percent of background width, y percent of background height)
            pos (tuple): Position of the top left corner of the bounding box
                scaled to background size. (x percent of background width,
                y percent of background height)
            color (str, optional): _description_. Defaults to "#ffffff".
            font_face (str, optional): _description_. Defaults to
                "assets/Lato-BoldItalic.ttf".
        """
        # Initializing the scaled box sizes, font size, and current text
        # bounding box size
        x_dim, y_dim = (self.card_size[0] * scale[0],
                        self.card_size[1] * scale[1])
        x_pos, y_pos = (pos[0] * self.card_size[0], pos[1] * self.card_size[1])
        font_size = 1
        current_x, current_y = 1, 1
        # Need these variables to be defined outside of the while loop
        font_obj = ImageFont.truetype(font_face, font_size)
        wrapped_text = self.wrap_text_to_width(text, font_obj, x_dim)

        logging.info(
            f"adding [{text}] to image in box size {x_dim, y_dim} \
            and position: text"
        )
        # Loop will keep bumping up the font size until the text vertically
        # does not fit in the bounding box
        while current_y < y_dim:
            # Make a font object with the current font size
            font_obj = ImageFont.truetype(font_face, font_size)
            # Given that font and size, wrap the text to the width of the box
            wrapped_text = self.wrap_text_to_width(text, font_obj, x_dim)
            # Check the size of the wrapped text, note the current_x should
            # always be less than x_dim which is why the while loop does not
            # check it.
            current_x, current_y = font_obj.getsize_multiline(
                "\n".join(wrapped_text))
            # Make it bigger since we didn't overflow
            font_size += 1

        # Now that we have scaled the font size up as large as possible to
        # fit in our text box, we need to draw the text on the canvas
        draw = ImageDraw.Draw(self.canvas)
        draw.multiline_text((x_pos, y_pos),
                            "\n".join(wrapped_text), color, font_obj)
