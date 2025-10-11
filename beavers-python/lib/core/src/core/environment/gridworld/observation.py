import numpy as np

N_OBSERVATION_DIMENSIONS = 6


class Observer:
    def __init__(self, grid: np.ndarray, all_agents):
        self.grid = grid
        self.all_agents = all_agents

    def get_terrain_layer(self, agent) -> np.ndarray:
        x, y = agent.beaver.x, agent.beaver.y

        # Extract 3x3 patch using slicing (much faster than loops)
        x_start, x_end = x - 1, x + 2
        y_start, y_end = y - 1, y + 2

        x_start = max(0, x_start)
        x_end = min(self.grid.shape[0], x_end)
        y_start = max(0, y_start)
        y_end = min(self.grid.shape[1], y_end)

        local_grid = self.grid[x_start:x_end, y_start:y_end]

        # Pad if at boundary to ensure 3x3
        if local_grid.shape != (3, 3):
            padded = np.zeros((3, 3))
            # Calculate where to place the extracted patch
            pad_x = 1 - (x - x_start)
            pad_y = 1 - (y - y_start)
            padded[pad_x:pad_x + local_grid.shape[0],
                   pad_y:pad_y + local_grid.shape[1]] = local_grid
            return padded

        return local_grid

    def get_agent_layer(self, agent) -> np.ndarray:  # Add agent parameter
        # Create full grid with agent positions
        a = np.zeros_like(self.grid)
        for ag in self.all_agents:
            a[ag.beaver.x][ag.beaver.y] = 1.0

        # Extract 3x3 patch (same logic as terrain)
        x, y = agent.beaver.x, agent.beaver.y
        x_start, x_end = max(0, x - 1), min(self.grid.shape[0], x + 2)
        y_start, y_end = max(0, y - 1), min(self.grid.shape[1], y + 2)

        local_grid = a[x_start:x_end, y_start:y_end]

        # Pad if needed
        if local_grid.shape != (3, 3):
            padded = np.zeros((3, 3))
            pad_x = 1 - (x - x_start)
            pad_y = 1 - (y - y_start)
            padded[pad_x:pad_x + local_grid.shape[0],
                   pad_y:pad_y + local_grid.shape[1]] = local_grid
            return padded

        return local_grid

    def get_resource_layer(self, agent) -> np.ndarray:  # Add agent parameter
        # TODO: implement when you have resources
        return np.zeros((3, 3))  # Return 3x3, not full grid
