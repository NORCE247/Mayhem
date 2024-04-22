"""Authors: Narongchai Cherdchoo & Daniels Sliks, 2024."""
import pygame
from config import*
from typing import TYPE_CHECKING
from sprites.player import Player
from sprites.object import Object
from sprites.fuel_pad import FuelPad

class LocalGame():
    """
    The class represents a game screen, where players and objects are defined.

    Attributes:
        game            : The main game class (would switch between other scenes if we had them)
        font            : front style & size
        players         : Defined players and added in sprite group
        bullets         : Sprite group for bullets
        objects         : Defined and insert objects in sprite group
        all_sprites     : Collected sprite group

    Methods:
    -------
    __init__            : Initializes objects to be include to the game screen.
    update              : Draw and update objects for each frame.
    handle_events       : Keys input for control the player.
    player_display      : Player status on fuel left and current score.
    map                 : Create Objects in the game as map.

    """

    def __init__(self, game: 'Game') -> None:
        """
        Initializes objects to be include to the game screen.
        :param game:
        """
        self.game = game

        # Create a font object
        self.font = pygame.font.SysFont("arial", 14)

        # Create player and add to group
        self.player = Player(0, [150, 750], self)
        self.player2 = Player(1, [850, 750], self)
        self.players = pygame.sprite.Group(self.player)
        self.players.add(self.player2)


        self.bullets = pygame.sprite.Group()

        # Border walls
        self.objects = pygame.sprite.Group(Object(1, (self.game.resolution[0]/2, self.game.resolution[1]+10), (self.game.resolution[0], 40)))
        Object(2, (-10, self.game.resolution[1]/2), (40, self.game.resolution[1]), self.objects)
        Object(3, (self.game.resolution[0]+10, self.game.resolution[1]/2), (40, self.game.resolution[1]), self.objects)
        Object(4, (self.game.resolution[0]/2, -10), (self.game.resolution[0], 40), self.objects)
        Object(5, (350, 450), (200, 50), self.objects)
        self.map()


        # Fuel pads
        self.fuel_pads = pygame.sprite.Group(FuelPad(1, (150, 795), (200, 10)))
        FuelPad(2, (850, 795), (200, 10), self.fuel_pads)

        # Add all sprite also to a single group
        self.all_sprites = self.objects.copy()
        self.all_sprites.add(self.players)
        self.all_sprites.add(self.fuel_pads)
        self.all_sprites.add(self.bullets)


    def update(self) -> None:
        """
        Draw and update objects each frame.
        :return:
        """
        self.game.screen.fill(BACKGROUND_COLOR)
        self.bullets.update()

        self.all_sprites.draw(self.game.screen)
        self.player_display()

        if SHOW_FPS:
            fps = self.font.render(str(int(self.game.clock.get_fps())), True, (0, 0, 0))
            self.game.screen.blit(fps, (10, fps.get_height()-40))

        if DEBUG_MODE:
            # CURSOR DEBUG
            cursor_pos = pygame.mouse.get_pos()
            cursor_pos_text = self.font.render(str(cursor_pos), True, (0,0,0))
            self.game.screen.blit(cursor_pos_text, (10, 50))

            # Player 1 DEBUG STATS
            player_debug_stats_str = self.font.render("("+str(round(self.player.pos[0]))+", "+str(round(self.player.pos[1]))+") "+str(round(self.player.get_angle()))+" "+str(self.player.inertia_vec.length()), True, (0,0,0))
            self.game.screen.blit(player_debug_stats_str, (400,40))


            # DEBUG VECTOR FOR INERTIA
            debug_vec = self.player.inertia_vec.copy()
            debug_length = debug_vec.length()
            if debug_length > 0.1:
                debug_vec.scale_to_length(debug_length*15)
            pygame.draw.aaline(self.game.screen, (255, 0, 0), self.player.pos, ((self.player.pos[0]+debug_vec.x), (self.player.pos[1]+debug_vec.y)), 1)

    def handle_events(self, keys: tuple[bool, ...]) -> None:
        """
        Handling the keyboard input for controlling the player
        :param keys: keyboard
        :return:
        """
        # Player Controls
        self.players.update(keys)

    def player_display(self) -> None:
        """
        Displays score and fuel of both players
        :return:
        """
        scores = self.font.render(
            "Player 1: " + str(self.player.score) + "       "
            "Player 2: " + str(self.player2.score), True, (0, 0, 0))

        fuel = self.font.render(
            "Fuel: " + str(round(self.player.fuel/FUEL*100)) + "%       " +
            "Fuel: " + str(round(self.player2.fuel/FUEL*100)) + "%", True, (0, 0, 0))


        self.game.screen.blit(scores, ((RESOLUTION[0] // 2) - 100, RESOLUTION[1] - 100))
        self.game.screen.blit(fuel,   ((RESOLUTION[0] // 2) - 100, RESOLUTION[1] - 80))

    def map(self) -> None:
        """
        Used Objects class that define the game map
        :return:
        """
        Object(6.0, (150,650), (200, 3), self.objects)
        Object(6.1, (330, 650), (3, 75), self.objects)
        Object(6.2, (330, 750), (3, 40), self.objects)
        Object(6.3, (170, 550), (3, 40), self.objects)

        Object(6.3, (455, 550), (300, 3), self.objects)
        Object(6.3, (670, 645), (300, 3), self.objects)

        Object(6.3, (898, 447), (3, 150), self.objects)
        Object(6.3, (623, 383), (200, 3), self.objects)
        Object(6.3, (160, 343), (200, 3), self.objects)
        Object(6.3, (341, 193), (3, 100), self.objects)

if TYPE_CHECKING:
    from game import Game
