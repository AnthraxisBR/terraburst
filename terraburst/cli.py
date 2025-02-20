import click
import asyncio
from .executor import run_parallel_terraform


@click.command()
@click.option('--directory', '-d', required=True, help="Root directory containing Terraform projects")
@click.option('--concurrency', '-c', default=3, help="Number of Terraform plans to run in parallel")
def cli(directory, concurrency):
    click.echo(f"Running Terraform plans in {directory} with concurrency {concurrency}...")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_parallel_terraform(directory, concurrency))


if __name__ == "__main__":
    cli()
