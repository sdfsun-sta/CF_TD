"""Entry point for the CF_TD project."""
import argparse
from cf_td import get_greeting

def main() -> None:
    """Program entry point."""
    parser = argparse.ArgumentParser(description="CF_TD greeting program")
    parser.add_argument("--name", default="World", help="Name to greet")
    args = parser.parse_args()
    print(get_greeting(args.name))

if __name__ == "__main__":
    main()
