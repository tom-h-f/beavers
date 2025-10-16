import argparse
from core.orchestrator import Orchestrator, OrchestratorConfig


def main(args):
    config = OrchestratorConfig()
    config.number_of_agents = args.agent_count
    config.number_of_episodes = args.episodes
    config.render_enabled = args.render
    config.renderer_type = args.renderer
    config.batch_size = args.batch_size
    config.max_steps = args.max_steps
    config.model_path = args.model
    config.size = args.size
    o = Orchestrator(config)

    try:
        o.train()
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the agent environment simulation."
    )
    parser.add_argument(
        "--agent-count",
        type=int,
        default=3,
        help="Number of agents to spawn in the environment.",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=10,
        help="Number of episodes to run",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Batch Size for training purposes",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=1024,
        help="Maximum training steps per episode",
    )
    parser.add_argument(
        "--render", action="store_true", help="Enable rendering"
    )
    parser.add_argument(
        "--renderer",
        type=str,
        choices=["pygame", "tui"],
        default="tui",
        help="Renderer type: 'pygame' for graphical window, 'terminal' for text-based",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to the model file to load for training",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=16,
        help="Size of the training enviroment",
    )
    args = parser.parse_args()
    main(args)
