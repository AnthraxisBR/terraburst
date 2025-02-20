import asyncio
import os
import shutil


async def run_command(command, directory):
    print(f"Executing: {command} (in {directory})")

    process = await asyncio.create_subprocess_shell(
        command, cwd=directory,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    async for line in process.stdout:
        print(f"{directory}: {line.decode().strip()}")

    async for line in process.stderr:
        print(f"{directory}: {line.decode().strip()}")

    await process.wait()


async def copy_plan_file(directory, plan_output_file):
    project_plan_path = os.path.join(directory, "terraburst_plan")
    current_plan_path = os.path.join(os.getcwd(), f"terraburst_plan_{os.path.basename(directory)}")

    try:
        for destination in [project_plan_path, current_plan_path]:
            shutil.copy2(os.path.join(directory, plan_output_file), destination)
            print(f"Terraform plan file copied to {destination}")

    except Exception as e:
        print(f"Error copying Terraform plan file in {directory}: {str(e)}")


async def run_terraform_plan(directory, config):
    if not os.path.exists(os.path.join(directory, "main.tf")):
        print(f"Skipping {directory}: No Terraform files found.")
        return

    print(f"Running 'terraform plan' in {directory} using workspace '{config['workspace']}'...")

    try:
        for command in config.get("before_plan", []):
            await run_command(command, directory)

        await run_command(f"terraform workspace select {config['workspace']}", directory)

        plan_output_file = config["output_file"]
        plan_command = f"terraform plan -out={plan_output_file}"

        if config["var_file"]:
            plan_command += f" -var-file={config['var_file']}"

        for var in config["variables"]:
            if isinstance(var, dict) and "name" in var and "value" in var:
                plan_command += f" -var {var['name']}={var['value']}"

        await run_command(plan_command, directory)

        await copy_plan_file(directory, plan_output_file)

        for command in config.get("after_plan", []):
            await run_command(command, directory)

        print(f"SUCCESS: Terraform plan completed in {directory}")

    except Exception as e:
        print(f"Failed to run Terraform in {directory}: {str(e)}")
