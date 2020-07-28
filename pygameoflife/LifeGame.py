import sys, pygame, random

# TODO write readme
# TODO package as pip package
# TODO push to pypi


class LifeGame:

    def __init__(self, screen_width=800, screen_height=600, cell_size=10, alive_color=(0,255,255),
                 dead_color=(0,0,0), max_fps=10):
        """
        Initialize grid, set default game state, initialize screen

        :param screen_width: Game window width
        :param screen_height: Game window height
        :param cell_size: Diameter of circles
        :param alive_color: RGB tuple e.g. (255,255,255) for cells
        :param dead_color: RGB tuple e.g. (255,255,255) for cells
        :param max_fps: Framerate cap to limit game speed
        """
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clear_screen()
        pygame.display.flip()

        self.last_update_completed = 0
        self.desired_milliseconds_between_updates = (1.0 / max_fps) * 1000.0

        self.active_grid = 0
        self.num_cols = int(self.screen_width / self.cell_size)
        self.num_rows = int(self.screen_height / self.cell_size)
        self.grids = []
        self.init_grids()
        self.set_grid()

        self.paused = False
        self.game_over = False

    def init_grids(self):
        """
        Create and stores the default active and inactive grid
        :return: None
        """
        def create_grid():
            """
            Generate an empty 2D grid
            :return:
            """
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
        Set an entire grid at once. Set to a single value or random 0/1.

        Examples:
          set_grid(0) # all dead
          set_grid(1) # all alive
          set_grid() # random
          set_grid(None) # random

        :param grid: Index of grid, for active/inactive (0 or 1)
        :param value: Value to set the cell to (0 or 1)
        :return: None
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

        :return: None
        """
        self.clear_screen()
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if self.grids[self.active_grid][r][c] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color
                pygame.draw.circle(self.screen,
                                   color,
                                   (int(c * self.cell_size + (self.cell_size / 2)),
                                    int(r * self.cell_size + (self.cell_size / 2))),
                                   int(self.cell_size / 2),
                                   0)
        pygame.display.flip()

    def clear_screen(self):
        """
        Fill whole screen with dead color

        :return: None
        """
        self.screen.fill(self.dead_color)

    def get_cell(self, row_num, col_num):
        """
        Get the alive/dead (0/1) state of a specific cell in active grid

        :param row_num:
        :param col_num:
        :return: 0 or 1 depending on state of cell. Defaults to 0 (dead)
        """
        try:
            cell_value = self.grids[self.active_grid][row_num][col_num]
        except:
            cell_value = 0
        return cell_value

    def check_cell_neighbors(self, row_index, col_index):
        """
        Get the number of alive neighbor cells and determine the state of the cell
        for the next generation. Determines whether it lives, dies, survives, or is born.

        :param row_index: Row number of cell to check
        :param col_index: Column number of cell to check
        :return: The state the cell should in the next generation (0 or 1)
        """
        num_alive_neighbors = 0
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        # Rules for life and death
        if self.grids[self.active_grid][row_index][col_index] == 1: # alive
            if num_alive_neighbors > 3:  # Overpopulation
                return 0
            if num_alive_neighbors < 2:  # Underpopulation
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:  # Survive
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0: # dead
            if num_alive_neighbors == 3:
                return 1 # come to life

        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        """
        Inspect current generation state, prepare next generation
        :return: None
        """
        self.set_grid(0, self.inactive_grid())
        for c in range(self.num_cols - 1):  # another solution sets this to self.num_cols - 1
            for r in range(self.num_rows - 1):  # another solution sets this to self.num_rows - 1
                next_gen_state = self.check_cell_neighbors(r, c)
                # set inactive grid future cell state
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        """
        Helper function to get the index of the inactive grid
        If active grid is 0 will return 1 and vice-versa.

        :return:
        """
        return (self.active_grid + 1) % 2

    def handle_events(self):
        """
        Handle any keypresses
        s - start/stop (pause) the game
        q - quit
        r - randomize grid

        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("key pressed")

                # if event is keypress of "s" then toggle game pause
                if event.unicode == 's':
                    print("Toggling pause.")
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True

                # if event is keypress of "r" then randomize grid
                elif event.unicode == 'r':
                    print("Randomizing grid.")
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid) # randomize
                    self.set_grid(0, self.inactive_grid()) # set to 0
                    self.draw_grid()

                # if event is keypress of "q" then quit
                elif event.unicode == 'q':
                    print("Exiting.")
                    self.game_over = True

            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        """
        Kick off the game, and loop forever until quit state

        :return: None
        """
        while True:
            if self.game_over:
                return

            self.handle_events()

            if self.paused:
                continue

            self.update_generation()
            self.draw_grid()

            self.cap_frame_rate()

    def cap_frame_rate(self):
        """
        If game is running too fast and updating frames too frequently,
        just wait to maintain stable framerate

        :return: None
        """
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now


if __name__ == "__main__":
    """
    Launch a game of life
    """
    game = LifeGame()
    game.run()
