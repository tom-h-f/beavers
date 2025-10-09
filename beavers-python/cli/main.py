import argparse
from core.orchestrator import Orchestrator, OrchestratorConfig


def main(args):
    config = OrchestratorConfig()
    config.number_of_agents = args.count
    config.number_of_episodes = args.episodes
    config.render_enabled = args.render
    config.batch_size = args.batch_size
    config.max_steps = args.max_steps
    print(config)
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
        "--count",
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
        "--render", action="store_true", help="Show the pygame render window"
    )
    args = parser.parse_args()
    main(args)
