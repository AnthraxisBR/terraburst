import click
import asyncio
import logging
from .executor import run_parallel_terraform

logging.basicConfig(level=logging.INFO)

@click.command()
@click.option('--directory', '-d', required=True, help="Root directory containing Terraform projects")
@click.option('--concurrency', '-c', default=3, help="Number of Terraform plans to run in parallel")
def cli(directory, concurrency):
    logging.info(f"Running Terraform plans in {directory} with concurrency {concurrency}...")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_parallel_terraform(directory, concurrency))
    except Exception as e:
        logging.error(f"Error running Terraform plans: {str(e)}")
    finally:
        loop.close()

if __name__ == "__main__":
    cli()