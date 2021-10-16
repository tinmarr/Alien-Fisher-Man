from rubato.sprite import Sprite
from rubato.utils import Vector, Color
from rubato.scenes import Camera
import pygame

class Text(Sprite):
    """
    A subclass of Sprite that handles Text.

    :param options: A dictionary of options
    """

    default_options = {
        "text": "default_text",
        "pos": Vector(),
        "size": 16,
        "z_index": 0,
        "font_name": 'Arial',
        "color": Color.red
    }

    def __init__(self, options=default_options):
        super().__init__(options.get("pos", Text.default_options["pos"]), options.get("z_index", Text.default_options["z_index"]))
        self.text = options.get("text", Text.default_options["text"])
        self.size = options.get("size", Text.default_options["size"])
        self.font_name = options.get("font_name", Text.default_options["font_name"])
        self.color = options.get("color", Text.default_options["color"])
        font = pygame.font.SysFont(self.font_name, self.size)
        self.image = font.render(self.text, True, self.color)
        

    def remake_image(self):
        font = pygame.font.SysFont(self.font_name, self.size)
        self.image = font.render(self.text, True, self.color)

    def draw(self, camera: Camera):
        """
        Draws the text if the z index is below the camera's.

        :param camera: The current Camera viewing the scene.
        """

        super().draw(self.image, camera)