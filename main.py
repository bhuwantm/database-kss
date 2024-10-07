import argparse
from db import seed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Takes argument to run corresponding function."
    )
    parser.add_argument("command", type=str, help="Command name")

    args = parser.parse_args()

    command = args.command

    if args.command == "seed":
        seed.seed()

    if args.command == "unseed":
        seed.unseed()
