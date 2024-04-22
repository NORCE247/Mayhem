"""Authors: Narongchai Cherdchoo & Daniels Sliks, 2024."""
from scenes.local_game import LocalGame
from config import *


class Game:
    """
    A class representing the game itself.

    Methods:
    --------
        __init__    : Initializes game.
        run         : Game loop.
    """

    def __init__(self) -> None:
        """Initializes game"""
        #Screen size
        self.resolution = RESOLUTION

        # Define the Program Window
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption('ROCKETS!!!!')

        self.running = True
        self.clock = pygame.time.Clock()

        # Current Match
        self.current_scene = LocalGame(self)   

    def run(self) -> None:
        """
        Game loop
        :return:
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_scene.handle_events(pygame.key.get_pressed())
            self.current_scene.update()
            self.clock.tick(FPS)
            pygame.display.flip()

        pygame.quit()
