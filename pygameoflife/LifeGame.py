import sys, pygame, random

BOARD_SIZE = WIDTH, HEIGHT = 640, 480
CELL_SIZE = 10
DEAD_COLOR = 0, 0, 0
ALIVE_COLOR = 0, 255, 255

MAX_FPS = 8


class LifeGame:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        self.clear_screen()
        pygame.display.flip()

        self.last_update_completed = 0
        self.desired_milliseconds_between_updates = (1.0 / MAX_FPS) * 1000.0

        self.active_grid = 0
        self.num_cols = int(WIDTH / CELL_SIZE)
        self.num_rows = int(HEIGHT / CELL_SIZE)
        self.grids = []
        self.init_grids()
        self.set_grid()

    def init_grids(self):
        # self.num_cols = int(WIDTH / CELL_SIZE)
        # self.num_rows = int(HEIGHT / CELL_SIZE)
        # print("Columns: %d\nRows: %d" % (self.num_cols, self.num_rows))
        # self.grids = [[[0] * self.num_rows] * self.num_cols,
        #               [[0] * self.num_rows] * self.num_cols]
        # self.active_grid = 0
        #
        # self.set_grid()
        # print(self.grids[0])
        def create_grid():
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows
        self.grids.append(create_grid())
        self.grids.append(create_grid())

        self.set_grid()

    def set_grid(self, value=None, grid=0):
        """
        Examples:
        # set_grid(0) # all dead
        # set_grid(1) # all alive
        # set_grid() # random
        # set_grid(None) # random

        :param value:
        :return:
        """
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if value is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value

    def draw_grid(self):
        """
        Given the grid and cell states, draw the cells on the screen
        :return:
        """
        self.clear_screen()
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if self.grids[self.active_grid][r][c] == 1:
                    color = ALIVE_COLOR
                else:
                    color = DEAD_COLOR
                pygame.draw.circle(self.screen,
                                   color,
                                   (int(c * CELL_SIZE + (CELL_SIZE / 2)),
                                    int(r * CELL_SIZE + (CELL_SIZE / 2))),
                                   int(CELL_SIZE / 2),
                                   0)
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(DEAD_COLOR)

    def update_generation(self):
        # Inspect the current active generation
        # update the inactive grid to store next generation
        # swap out the active grid
        # self.set_grid(0, self.inactive_grid())
        # for r in range(self.num_rows - 1):
        #     for c in range(self.num_cols - 1):
        #         next_gen_state = self.check_cell_neighbors
        pass

    def inactive_grid(self):
        """
        Helper function to get the index of the inactive grid
        If active grid is 0 will return 1 and vice-versa.

        :return:
        """
        return (self.active_grid + 1) % 2

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
            self.set_grid()
            self.draw_grid()
            self.cap_frame_rate()

            # cap framerate at 60 fps, if time since the last frame draw < 1/60th of a second, sleep for remaining time

    def cap_frame_rate(self):
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now


if __name__ == "__main__":
    game = LifeGame()
    game.run()
