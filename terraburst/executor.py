import os
import asyncio
import logging
from .config import load_config, load_main_config
from .runner import run_terraform_plan

logging.basicConfig(level=logging.INFO)


async def run_parallel_terraform(root_dir, terraburst_config, project, concurrency):
    if root_dir:
        terraform_dirs = [
            os.path.join(root_dir, d) for d in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, d))
        ]
        valid_dirs = [(d, load_config(d)) for d in terraform_dirs]
        valid_dirs = [(d, cfg) for d, cfg in valid_dirs if cfg is not None]
    else:
        valid_dirs = load_main_config(terraburst_config, project)
        logging.info(valid_dirs)

    if not valid_dirs:
        logging.error("No valid Terraform projects found.")
        return

    logging.info(f"Found {len(valid_dirs)} Terraform projects. Running with {concurrency} runners")

    semaphore = asyncio.Semaphore(concurrency)

    async def limited_run(directory, config):
        async with semaphore:
            await run_terraform_plan(directory, config)

    tasks = [limited_run(d, cfg) for d, cfg in valid_dirs]
    await asyncio.gather(*tasks)
