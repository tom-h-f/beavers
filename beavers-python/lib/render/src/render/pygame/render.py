import pygame
from core.terrain.tile import Tile, TILE_SIZE_PX
from core.agent import Beaver


class PygameRenderer:
    COLOURS = {
        Tile.WATER: (68, 184, 242),
        Tile.TREE: (163, 86, 86),
        Tile.GROUND: (0, 125, 29),
    }

    def __init__(self, width, height):
        pygame.init()
        self.display = pygame.display.set_mode(
            (width*TILE_SIZE_PX, height*TILE_SIZE_PX))
        self.running = True
        self.clock = pygame.time.Clock()
        pass

    def draw_grid(self, env):
        rows, cols = env.world_grid.shape

        for r in range(rows):
            for c in range(cols):
                self.draw_tile(env.world_grid, r, c)

        self.draw_agents(env)

    def draw_agents(self, env):
        for a in env.agents:
            t = (255, 0, 255)
            pygame.draw.rect(
                self.display,
                t,
                (a.y * TILE_SIZE_PX, a.x * TILE_SIZE_PX,
                 TILE_SIZE_PX, TILE_SIZE_PX)
            )

    def draw_tile(self, grid, x, y):
        assert (grid[x, y] in self.COLOURS)
        t = self.index_to_color(grid[x, y])
        pygame.draw.rect(
            self.display,
            t,
            (y * TILE_SIZE_PX, x * TILE_SIZE_PX,
             TILE_SIZE_PX, TILE_SIZE_PX)
        )

    def render(self, env):
        # TODO should the env get passed somewhere else rather than every render call?
        # TODO this while running loop should be what calls the render rather than inside of it
        self.draw_grid(env)
        pygame.display.flip()
        self.clock.tick(60)

    def index_to_color(self, v):
        return self.COLOURS[v]
