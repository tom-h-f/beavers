import argparse
from core.orchestrator import Orchestrator, OrchestratorConfig


def main(count, render_enabled, episodes):
    config = OrchestratorConfig()
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
        default=100,
        help="Number of episodes to run",
    )
    parser.add_argument(
        "--render", action="store_true", help="Show the pygame render window"
    )
    args = parser.parse_args()
    main(args.count, args.render, args.episodes)
