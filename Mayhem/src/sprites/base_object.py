"""Authors: Narongchai Cherdchoo & Daniels Sliks, 2024."""
import pygame

class BaseObject(pygame.sprite.Sprite):

    """
    A class to represent Rectangle-objects, used to create the stationary objects.

    Attributes:
        id          : Unique id for debugging purposes
        pos         : Position [x,y]
        dimensions  : Size [x,y]
        image       : color
        rect        : Body

    """

    def __init__(self, id: int, pos: list[int, int], dimensions: list[int, int], color: tuple[int, int, int], *groups) -> None:

        """
        Initializes object.
        :param id: Unique id for debugging purposes
        :param pos: Coordinate
        :param dimensions: Size
        :param color: Color
        :param groups: sprite group
        """
        super().__init__(*groups)

        self.id = str(id)
        self.pos = [pos[0], pos[1]]
        self.dimensions = dimensions 
        self.image = pygame.Surface(dimensions)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
