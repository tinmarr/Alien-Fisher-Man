from rubato.sprite.sprite import Sprite
from pygame.image import load
from pygame.transform import scale, flip
from rubato.utils import Vector
from rubato.scenes import Camera


class Image(Sprite):
    """
    A subclass of Sprite that handles Images.

    :param image_location: The path to the image.
    :param pos: The position of the sprite.
    """
    def __init__(self, image_location: str, pos: Vector = Vector(), scale_factor: Vector = Vector(1, 1)):
        super().__init__(pos)
        if image_location == "" or image_location == "default":
            self.image = load("rubato/static/default.png")
        elif image_location == "empty":
            self.image = load("rubato/static/empty.png")
        else:
            self.image = load(image_location)
            
        self.scale(scale_factor)

    def update(self):
        pass

    def draw(self, camera: Camera):
        """
        Draws the image if the z index is below the camera's.

        :param camera: The current Camera viewing the scene.
        """
        super().draw(self.image, camera)

    def scale(self, scale_factor: Vector):
        """
        Let's you rescale the Image to a given scale factor.

        :param scale_factor: A Vector describing the scale in the x and y direction relative to its current size
        """
        if abs(new_x := self.image.get_width() * scale_factor.x) < 1:
            new_x = 1
        if abs(new_y := self.image.get_height() * scale_factor.y) < 1:
            new_y = 1
        self.image = flip(scale(self.image, (abs(new_x), abs(new_y))), new_x < 0, new_y < 0)