import os
import asyncio
from .config import load_config
from .runner import run_terraform_plan


async def run_parallel_terraform(root_dir, concurrency):
    terraform_dirs = [
        os.path.join(root_dir, d) for d in os.listdir(root_dir)
        if os.path.isdir(os.path.join(root_dir, d))
    ]

    valid_dirs = [(d, load_config(d)) for d in terraform_dirs]
    valid_dirs = [(d, cfg) for d, cfg in valid_dirs if cfg is not None]

    if not valid_dirs:
        print("No valid Terraform projects found.")
        return

    print(f"Found {len(valid_dirs)} Terraform projects. Running with {concurrency} runners")

    semaphore = asyncio.Semaphore(concurrency)

    async def limited_run(directory, config):
        async with semaphore:
            await run_terraform_plan(directory, config)

    tasks = [limited_run(d, cfg) for d, cfg in valid_dirs]
    await asyncio.gather(*tasks)
