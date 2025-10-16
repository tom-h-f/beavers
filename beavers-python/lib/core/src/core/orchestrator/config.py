from core.environment import EnvironmentType
from typing import Optional


class OrchestratorConfig:
    number_of_agents: int = 20
    number_of_episodes: int = 10
    size: int = 32
    batch_size: int = 16*16
    render_enabled: bool = False
    renderer_type: str = "tui"
    torch_device: str = "mps"
    max_steps: int = 1024
    env_type: EnvironmentType = EnvironmentType.GridWorld
    model_path: Optional[str] = None
