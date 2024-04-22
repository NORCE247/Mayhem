"""Authors: Narongchai Cherdchoo & Daniels Sliks, 2024."""
import pygame.sprite
from typing import TYPE_CHECKING
from config import *
from sprites.bullets import *
from sprites.object import Object
from sprites.fuel_pad import FuelPad



class Player(pygame.sprite.Sprite):
    """A class used to represent a Player."""

    def __init__(self, id: int, pos: list[int, int], match: 'LocalGame', *groups) -> None:

        """
        Initializes a new Player

        Parameters:
            id (int)        : Defined player's controls.
            pos (vector)    : Player position.
            match           : Holds the current LocalGame Object that player is in.
            groups          : Group the object with other in the defined sprite group.

        """
        super().__init__(*groups)

        #Player identical 
        self.id = id
        self.SIZE = SIZE

        #Game screen
        self.match = match

        # Draw the default player shape 
        self.original_image = pygame.Surface(SIZE, pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, COLOR, [(self.SIZE[0]/2, 0), (0, self.SIZE[1]), self.SIZE])

        # Initialize the image and rect attributes
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)

        # Position & Direction
        self.pos = [pos[0], pos[1]]
        self.direction_vec = pygame.math.Vector2(0, -1)
        self.inertia_vec = pygame.math.Vector2()

        # Rotate the image to the correct angle
        self.updateRotation()

        # PLayer stats
        self.fuel = FUEL
        self.score = 0

        # Collision Variables
        self.collision_cooldown = 0
        self.bounces = 0
        self.stationary = False

        # Attack
        self.shoot_cooldown = 0
        self.attacking = False



    def update(self, keys: tuple[bool, ...]) -> None:

        """
        Method to update a player's position

        Parameters:
        :param keys (list)     : PLayer input controller

        Return:
            None

        """
        #Update player behavior 
        self.input(keys)
        self.move()
        self.spriteCollisions()

        # Activate the Fuel pad
        if self.stationary and self.fuel < FUEL:
            self.fuel += 5
        elif self.fuel > FUEL:
            self.fuel = FUEL

        # Decrease the cooldown time
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def scoreMinusOne(self) -> None:
        if self.score > 0:
            self.score -= 1

    def get_angle(self) -> float:
        """
        Returns the angle of the players direction vector.

        Returns:
            float: The angle of the players direction vector.
        """
        if self.direction_vec.length() == 0:
            return -1

        return (self.direction_vec.angle_to(pygame.math.Vector2(0, -1))+90) % 360

    def updateRotation(self) -> None:
        """
        Updates the players rotation to face the direction of its velocity vector.

        It rotates the players original image based of the angle of the players direction vector.
        Achieved by finding the vector's angle to the reference angle.
        """
        if self.image and self.rect and self.direction_vec.length() > 0 and self.original_image:
            angle = self.get_angle()
            self.image = pygame.transform.rotate(self.original_image, angle-90)
            self.rect = self.image.get_rect(center=self.rect.center)

    def input(self, keys: tuple[bool, ...]) -> None:

        """
        Controls for the player: Shoot, burns fuel, rotates.

        :param keys: A list of currently pressed keys.
        :return None:
        """
        # Player is boosting
        if keys[PLAYER_CONTROLS[self.id][0]]:

            if self.fuel > 0:
                self.fuel -= 3

                # Logic for accelerating the player
                if self.inertia_vec.length() == 0:
                    if not self.stationary:
                        self.inertia_vec = self.direction_vec.copy()
                        self.inertia_vec.scale_to_length(SPEED_ACCELERATION)
                    else:
                        self.inertia_vec = pygame.math.Vector2(0, -1)
                        self.inertia_vec.scale_to_length(SPEED_ACCELERATION)
                        self.stationary = False
                        self.bounces = 0
                        self.collision_cooldown = FPS
                else:
                    distance_to_max_speed = self.inertia_vec.distance_to(self.direction_vec)

                    if SPEED_ACCELERATION/distance_to_max_speed > 1:
                        self.inertia_vec.scale_to_length(MAX_SPEED)
                    else:
                        self.inertia_vec = self.inertia_vec.lerp(self.direction_vec, SPEED_ACCELERATION/distance_to_max_speed)
        # ROTATE
        if not self.stationary:
            if keys[PLAYER_CONTROLS[self.id][1]]:
                self.direction_vec = self.direction_vec.rotate(-5)

            if keys[PLAYER_CONTROLS[self.id][2]]:
                self.direction_vec = self.direction_vec.rotate(5)

        self.updateRotation()

        # ATTACK
        if keys[PLAYER_CONTROLS[self.id][3]]:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = SHOOT_COOLDOWN
                Bullets(self, self.match.bullets, self.match.all_sprites)

    def move(self) -> None:

        """
        Update the inertia vector by applying air resistance and gravity, 
        and change player's position based of the updated inertia vector.
        :return:
        """
        # The Logic for air resistance (slowing down over speed)
        if self.inertia_vec.length() != 0 and not self.stationary:
            new_length = self.inertia_vec.length() - AIR_FRICTION
            if new_length > 0:
                self.inertia_vec.scale_to_length(new_length)
            else:
                self.inertia_vec = pygame.math.Vector2()
        if not self.stationary:
            self.inertia_vec.y += G_ACCELERATION

        # Make sure the player is not falling faster than the limit
        if self.inertia_vec.y > TERMINAL_VELOCITY:
            self.inertia_vec.y = TERMINAL_VELOCITY

        # Update players position
        if not self.stationary:
            self.pos[0] += self.inertia_vec.x
            self.pos[1] += self.inertia_vec.y

        self.rect.center = (round(self.pos[0]), round(self.pos[1]))

    def respawn(self) -> None:
        """
        Respawn player back to their predefined start point.
        :return:
        """
        self.direction_vec = pygame.math.Vector2(0,-MAX_SPEED)
        self.inertia_vec = pygame.math.Vector2(0,0)
        self.stationary = False
        self.pos = RESPAWN_POINT[self.id].copy()
        self.scoreMinusOne()

    def playerCollisions(self) -> None:

        """
        + Bounce player back when colliding with other players.
        + If the colliding force is too low -> respawn
        :param opponent: Player
        :return:
        """
        #Bounce
        self.collision_cooldown = 60
        if self.inertia_vec[0] > 0.4 or self.inertia_vec[1] > 0.4 :

            self.inertia_vec[0] *= -1
            self.inertia_vec[1] *= -1

        else:
            self.respawn()

    def fuelPadCollisions(self, angle_from_up, colliding_fuel_pad) -> None:
        """
        This method is used to make player bounce a set amount of times before the success landing on the fuel pad,
        if player's speed is too hight or the landing angle is too wide, then player will be respawn.

        :param angle_from_up: The angle between players direction and the upward vector.
        :param colliding_fuel_pad: The current fuel pad that are collided with player.
        :return:
        """
        if -MAX_LANDING_ANGLE < angle_from_up < MAX_LANDING_ANGLE and self.inertia_vec.length() < MAX_LANDING_SPEED:

            # After some bounces set player to be stationary on the fuel pad
            if self.bounces == 3:
                self.bounces = 0
                self.direction_vec = pygame.math.Vector2(0, -MAX_SPEED)
                self.inertia_vec = pygame.math.Vector2()
                self.stationary = True
                self.pos[1] = colliding_fuel_pad.pos[1] - colliding_fuel_pad.dimensions[1] / 2 - self.SIZE[
                    1] / 2

            # Bounce the player with a certain % of its speed back up
            elif self.inertia_vec.length() > 0:
                self.inertia_vec.reflect_ip(pygame.math.Vector2(0, -1))
                self.inertia_vec.scale_to_length(self.inertia_vec.length() * 0.6)
                if angle_from_up > 0:
                    if angle_from_up == 180:
                        self.inertia_vec.rotate_ip(10)
                self.collision_cooldown = FPS / 15
                self.bounces += 1
        else:
            self.respawn()

    def spriteCollisions(self) -> None:

        """
        Collision detection for when a player collides with other non-player sprites :[ Fuel pad, Player, Object, Bullets ]

        :return:
        """
        # Get a list all colliding sprites with player
        colliding_sprite = pygame.sprite.spritecollide(self, self.match.all_sprites, False)
        if len(colliding_sprite) > 0:

            colliding_with_fuel_pad = False
            colliding_fuel_pad = None
            colliding_object = None
            colliding_bullet = None
            colliding_players = None

            # Detect with what the collision is taking place with
            for colliding in colliding_sprite:

                if isinstance(colliding, FuelPad):
                    colliding_with_fuel_pad = True
                    colliding_fuel_pad = colliding

                elif isinstance(colliding, Player):
                    colliding_players = colliding

                elif isinstance(colliding, Object):
                    colliding_object = colliding

                if isinstance(colliding, Bullets):
                    colliding_bullet = colliding

            # Bullet Collision
            if colliding_bullet and colliding_bullet.owner != self:
                colliding_bullet.owner.score += 1
                colliding_bullet.kill()
                self.scoreMinusOne()
                self.respawn()

            # Landing on fuel pad logic and collision
            if colliding_with_fuel_pad and not self.stationary:
                angle_from_up = self.direction_vec.angle_to(pygame.math.Vector2(0, -1))
                self.fuelPadCollisions(angle_from_up, colliding_fuel_pad)

            elif colliding_object and not self.stationary:
                self.respawn()

            if colliding_players and colliding_players != self:
                self.playerCollisions()
                colliding_players.playerCollisions()

        self.collision_cooldown += -1

if TYPE_CHECKING:
    from scenes.local_game import LocalGame