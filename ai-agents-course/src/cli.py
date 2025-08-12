"""Command line interface for AI Agents Course."""
import argparse


def main() -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(description="AI Agents Course CLI")
    parser.add_argument("--version", action="version", version="0.1.0")
    parser.parse_args()
    print("TODO")


if __name__ == "__main__":
    main()
