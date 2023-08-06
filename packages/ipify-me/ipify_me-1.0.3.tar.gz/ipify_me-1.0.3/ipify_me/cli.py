"""Console script for ipify_me."""
import sys
import click
import ipify_me

@click.command()
def main(args=None):
    ipify_me.print_ipify_ip()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
