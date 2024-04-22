"""Authors: Narongchai Cherdchoo & Daniels Sliks, 2024."""
import pygame
from config import *
from typing import TYPE_CHECKING
from sprites.object import Object


class Bullets(pygame.sprite.Sprite):
    """
    A class representing bullets.

    Attributes:
        all_sprites             : The group containing every other sprite in the current game.
        owner                   : The Player who shot the bullet.
        direction_vec           : bullets movement direction.
        pos                     : bullets position.
        distance_traveled       : Tracks the distance a bullet as traveled, used to limit its lifetime.
        image                   : Bullets model.
        rect                    : Body that can reacts with other objects.

    Methods:
    ------------------
     __init__   : Initializes bullet.
    update      : Update bullet position with the direction it has.
    """

    def __init__(self, owner: 'Player' , *groups) -> None:
        """
        Initializes bullet

        :param owner: A Player class.
        :param groups: The sprite group.
        """
        super().__init__(*groups)

        self.all_sprites = groups[1] # all_sprites group is always at index 1
        self.owner = owner
        self.direction_vec = self.owner.direction_vec.copy()
        self.direction_vec.scale_to_length(BULLET_SPEED + self.owner.inertia_vec.length())

        self.pos = self.owner.pos.copy()
        self.distance_traveled = 0

        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0,0,0), (BULLET_SIZE/2,BULLET_SIZE/2), BULLET_SIZE/2)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self) -> None:
        """
        + Update bullet position with the direction it has.
        + Remove the colliding bullets.
        :return:
        """
        self.pos[0] += self.direction_vec.x
        self.pos[1] += self.direction_vec.y
        self.distance_traveled += self.direction_vec.length()
        self.rect.center = (round(self.pos[0]), round(self.pos[1]))
        self.collision()

    def collision(self) -> None:
        """
        Handling collision with other objects.
        :return:
        """
        collision_all_sprite = pygame.sprite.spritecollide(self, self.all_sprites, False)

        for collision in collision_all_sprite:
            if isinstance(collision, Object):
                self.kill()

            if isinstance(collision, Bullets) and collision != self:
                self.kill()


if TYPE_CHECKING:
    from sprites.player import Player