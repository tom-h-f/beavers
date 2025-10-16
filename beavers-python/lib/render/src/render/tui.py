import os
import time
from core.terrain.tile import Tile


class TerminalRenderer:
    TILE_CHARS = {
        Tile.WATER: '~',
        Tile.TREE: 'T',
        Tile.GROUND: '.',
        Tile.DAM: 'D',
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.last_frame = None

    def render(self, runner, action=None, agent=None):
        # Clear the terminal
        os.system('clear' if os.name == 'posix' else 'cls')

        grid = runner.env.grid.raw()
        agents = runner.alive_agents()

        # Print the grid
        print(f"Episode: {getattr(runner, 'current_episode', 'N/A')} | Step: {getattr(runner, 'step_count', 0)}")
        print("-" * (self.width * 2 + 3))

        for x in range(self.height):
            row = []
            for y in range(self.width):
                tile = grid[x, y]
                char = self.TILE_CHARS.get(tile, '?')

                # Check if there's an agent here
                for a in agents:
                    if a.beaver.x == x and a.beaver.y == y:
                        char = 'B'  # Beaver
                        break

                row.append(char)
            print(" ".join(row))

        print("-" * (self.width * 2 + 3))

        # Brief pause for visibility
        time.sleep(0.1)

        # Check for quit input (non-blocking)
        import select
        import sys
        if select.select([sys.stdin], [], [], 0.0)[0]:
            quit_input = sys.stdin.read(1)
            if quit_input.lower() == 'q':
                return False  # Stop rendering
        return True
