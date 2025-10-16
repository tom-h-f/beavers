import pygame
from core.terrain.tile import Tile, TILE_SIZE_PX
from core.agent.action import Action


class PygameRenderer:
    COLOURS = {
        Tile.WATER: (68, 184, 242),
        Tile.TREE: (163, 86, 86),
        Tile.GROUND: (0, 125, 29),
        Tile.DAM: (163, 33, 55),
    }

    def __init__(self, width, height):
        pygame.init()
        self.display = pygame.display.set_mode(
            (width * TILE_SIZE_PX, height * TILE_SIZE_PX)
        )
        self.running = True
        self.clock = pygame.time.Clock()
        # Initialize font for text rendering
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 8)
        # Track text messages for agents: {agent_id: (message, remaining_ticks)}
        self.text_messages = {}
        # Load beaver image
        self.beaver_image = pygame.image.load(
            '/Users/tom/Code/beavers/beavers-python/lib/render/beaver.png')
        # Scale the image to fit the tile size
        self.beaver_image = pygame.transform.scale(
            self.beaver_image, (TILE_SIZE_PX, TILE_SIZE_PX))

    def draw_grid(self, trainer):
        rows, cols = trainer.env.grid.raw().shape

        for r in range(rows):
            for c in range(cols):
                self.draw_tile(trainer.env.grid.raw(), r, c)

        self.draw_agents(trainer.agents)

    def draw_agents(self, agents):
        for b in [x for x in agents if not x.done]:
            a = b.beaver
            # Draw agent as beaver image
            center_x = a.y * TILE_SIZE_PX + TILE_SIZE_PX // 2
            center_y = a.x * TILE_SIZE_PX + TILE_SIZE_PX // 2
            # Get the rect for the image, centered at the agent's position
            image_rect = self.beaver_image.get_rect(
                center=(center_x, center_y))
            self.display.blit(self.beaver_image, image_rect)

            # Render text above agent if present
            agent_id = id(a)  # Use object id as key
            if agent_id in self.text_messages:
                message, remaining_ticks = self.text_messages[agent_id]
                text_surf = self.font.render(message, True, (255, 255, 255))
                text_rect = text_surf.get_rect(
                    center=(center_x, center_y - TILE_SIZE_PX // 2 - 10))
                self.display.blit(text_surf, text_rect)
                # Decrement ticks and remove if expired
                self.text_messages[agent_id] = (message, remaining_ticks - 1)
                if self.text_messages[agent_id][1] <= 0:
                    del self.text_messages[agent_id]

    def draw_tile(self, grid, x, y):
        assert grid[x, y] in self.COLOURS
        t = self.index_to_color(grid[x, y])
        rect = pygame.Rect(y * TILE_SIZE_PX, x * TILE_SIZE_PX,
                           TILE_SIZE_PX, TILE_SIZE_PX)
        pygame.draw.rect(self.display, t, rect)
        # Add a subtle border for better visual separation
        pygame.draw.rect(self.display, (50, 50, 50), rect, 1)

    def render(self, runner, action: Action = None, agent=None):
        # TODO should the env get passed somewhere else rather than every render call?
        # TODO this while running loop should be what calls the render rather than inside of it
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
        self.draw_grid(runner)
        if agent is not None and action is not None:
            self.set_text_for_agent(agent.beaver, action.str())

        pygame.display.flip()
        self.clock.tick(60)
        return self.running

    def index_to_color(self, v):
        return self.COLOURS[v]

    def set_text_for_agent(self, agent, message, duration=5):
        """Set a text message above the given agent for a specified duration in ticks."""
        self.text_messages[id(agent)] = (message, duration)
