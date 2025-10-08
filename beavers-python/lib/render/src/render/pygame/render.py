import pygame
from core.terrain.tile import Tile, TILE_SIZE_PX


class PygameRenderer:
    COLOURS = {
        Tile.WATER: (68, 184, 242),
        Tile.TREE: (163, 86, 86),
        Tile.GROUND: (0, 125, 29),
    }

    def __init__(self, width, height):
        pygame.init()
        self.display = pygame.display.set_mode(
            (width * TILE_SIZE_PX, height * TILE_SIZE_PX)
        )
        self.running = True
        self.clock = pygame.time.Clock()
        pass

    def draw_grid(self, trainer):
        rows, cols = trainer.env.grid.raw().shape

        for r in range(rows):
            for c in range(cols):
                self.draw_tile(trainer.env.grid.raw(), r, c)

        self.draw_agents(trainer.get_beaver_list())

    def draw_agents(self, agents):
        for a in agents:
            t = (255, 0, 255)
            pygame.draw.rect(
                self.display,
                t,
                (a.y * TILE_SIZE_PX, a.x * TILE_SIZE_PX, TILE_SIZE_PX, TILE_SIZE_PX),
            )

    def draw_tile(self, grid, x, y):
        assert grid[x, y] in self.COLOURS
        t = self.index_to_color(grid[x, y])
        pygame.draw.rect(
            self.display,
            t,
            (y * TILE_SIZE_PX, x * TILE_SIZE_PX, TILE_SIZE_PX, TILE_SIZE_PX),
        )

    def render(self, trainer):
        # TODO should the env get passed somewhere else rather than every render call?
        # TODO this while running loop should be what calls the render rather than inside of it
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
        self.draw_grid(trainer)
        pygame.display.flip()
        self.clock.tick(60)
        return self.running

    def index_to_color(self, v):
        return self.COLOURS[v]
