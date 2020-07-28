import sys, pygame, random

BOARD_SIZE = WIDTH, HEIGHT = 640, 480
CELL_SIZE = 10
DEAD_COLOR = 0, 0, 0
ALIVE_COLOR = 0, 255, 255

class LifeGame:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        self.clear_screen()
        pygame.display.flip()

        self.init_grids()

    def init_grids(self):
        self.num_cols = int(WIDTH / CELL_SIZE)
        self.num_rows = int(HEIGHT / CELL_SIZE)
        print("Columns: %d\nRows: %d" % (self.num_cols, self.num_rows))
        self.grids = [[[0] * self.num_rows] * self.num_cols,
                      [[0] * self.num_rows] * self.num_cols]
        self.active_grid = 0

        self.randomize_grid()
        print(self.grids[0])

    """
    Examples:
    # set_grid(0) # all dead
    # set_grid(1) # all alive
    # set_grid() # random
    # set_grid(None) # random
    
    :param value:
    :return:
    """
    def set_grid(self, value=None):
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if value is None:
                    cell_value = random.choice([0, 1])
                else:
                    cell_value = value
                self.grids[self.active_grid][c][r] = cell_value

    def draw_grid(self):
        # circle_rect = pygame.draw.circle(self.screen, ALIVE_COLOR, (50, 50), 5, 0)
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                pygame.draw.circle(self.screen)
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(DEAD_COLOR)

    def update_generation(self):
        # Inspect the current active generation
        # update the inactive grid to store next generation
        # swap out the active grid
        pass

    def handle_events(self):
        for event in pygame.event.get():
            # if event is keypress of "s" then toggle game pause
            # if event is keypress of "r" then randomize grid
            # if event is keypress of "q" then quit
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.handle_events()
            # Time checking?
            self.update_generation()
            self.draw_grid()

if __name__ == "__main__":

    game = LifeGame()
    game.run()

