import sys
import click
from .groups.cli_tools import cli_tools

# Main CLI Group
@click.group()
@click.version_option("0.1")
def main():
    """A CVE Search and Lookup CLI"""
    pass

# Add groups
main.add_command(cli_tools)

# Initialize CLI
if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("CVE")
    main()
