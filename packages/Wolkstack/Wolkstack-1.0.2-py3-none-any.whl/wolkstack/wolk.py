import sys
import click

@click.group()
@click.version_option("1.0.0")
def cli():
    """A CVE Search and Lookup CLI"""
    print("Hye")
    pass

@cli.command()
@click.argument('keyword', required=False)
def search(**kwargs):
    """Search through CVE Database for vulnerabilities"""
    click.echo(kwargs)
    pass

@cli.command()
@click.argument('name', required=False)
def look_up(**kwargs):
    """Get vulnerability details using its CVE-ID on CVE Database"""
    click.echo(kwargs)
    pass
cli = cli();

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("CVE")
    cli()
