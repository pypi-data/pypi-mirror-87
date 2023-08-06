"""Console script for ipify_me."""
import sys
import click
from .ipify_me import print_ipify_ip


@click.command()
def main(args=None):
    print_ipify_ip()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
