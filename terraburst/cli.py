import click
import asyncio
import logging
import subprocess
import os
from .executor import run_parallel_terraform
from .validator import validate_plan

logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@click.command()
@click.option('--directory', '-d', required=False, help="Root directory containing Terraform projects")
@click.option('--concurrency', '-c', default=3, help="Number of Terraform plans to run in parallel")
@click.option('--terraburst-config', '-tc', required=False, help="Path to Terraburst configuration file")
@click.option('--project', '-p', required=False, help="Project name to run Terraform plans")
def plan(directory, concurrency, terraburst_config, project):
    if not terraburst_config and not directory:
        logging.error("Please provide either Terraburst configuration file or directory path.")
        return

    if terraburst_config and directory:
        logging.error("Please provide either Terraburst configuration file or directory path, not both.")
        return

    if terraburst_config:
        logging.info(f"Running Terraform plans with Terraburst configuration: {terraburst_config}")

    logging.info(f"Running Terraform plans in {directory} with concurrency {concurrency}...")

    loop = asyncio.get_event_loop()
    try:
        if terraburst_config:
            loop.run_until_complete(run_parallel_terraform(False, terraburst_config, project, concurrency))
        else:
            loop.run_until_complete(run_parallel_terraform(directory, False, project, concurrency))
    except Exception as e:
        logging.error(f"Error running Terraform plans: {str(e)}")
    finally:
        loop.close()


@click.command()
@click.option('--plan-file', '-p', required=True, help="Path to Terraform plan file (binary format)")
def validate(plan_file):
    logging.info(f"Converting Terraform plan file to JSON: {plan_file}")

    json_plan_file = f"{plan_file}.json"
    try:
        subprocess.run(["terraform", "show", "-json", plan_file], stdout=open(json_plan_file, "w"), check=True)
        logging.info(f"Validation started on {json_plan_file}")
        validation_results = validate_plan(json_plan_file)
        if validation_results:
            logging.info(f"Validation results: {validation_results}")
        else:
            logging.error("Validation failed or invalid plan file.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to convert plan file: {str(e)}")
    finally:
        if os.path.exists(json_plan_file):
            os.remove(json_plan_file)  # Clean up after validation


cli.add_command(plan)
cli.add_command(validate)

if __name__ == "__main__":
    cli()
