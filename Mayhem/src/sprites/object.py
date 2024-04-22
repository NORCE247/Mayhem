"""Authors: Narongchai Cherdchoo & Daniels Sliks, 2024."""
from sprites.base_object import BaseObject

class Object(BaseObject):
    """A Sub-class of BaseObject thats represent obstacles"""

    def __init__(self, id: int, pos: list[int, int], dimensions: list[int, int], *groups) -> None:
        """
        Create object

        :param id: Unique id for debugging purposes 
        :param pos: Position [x,y]
        :param dimensions: Size [x,y]
        :param groups: sprite group
        """
        super().__init__(id, pos, dimensions, (0, 0, 0), *groups)

