import os
import yaml
import logging

CONFIG_FILENAMES = ["terraburst.yml", "terraburst.yaml"]


def load_config(directory):
    config_path = next((os.path.join(directory, filename) for filename in CONFIG_FILENAMES if os.path.exists(os.path.join(directory, filename))), None)

    if not config_path:
        logging.error(f"No configuration file found in {directory}")
        return None

    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        required_keys = ["workspace"]
        missing_keys = [key for key in required_keys if key not in config]

        if missing_keys:
            logging.error(f"Missing required keys in config: {missing_keys}")
            return None

        return config
    except Exception as e:
        logging.error(f"Error reading {config_path} - {str(e)}")
        return None


def prepare_main_config(config, project_name=None):
    project_list = []

    for project in config.get('projects', []):
        for sub_project in project.get('projects', []):
            logging.info(f"Found project: {sub_project.get('name')}")
            project_path = sub_project.get('project_path')
            project_config = {
                'workspace': sub_project.get('workspace'),
                'var_file': sub_project.get('var_file'),
                'output_file': sub_project.get('output_file'),
                'variables': sub_project.get('variables'),
                'before_plan': sub_project.get('before_plan'),
                'after_plan': sub_project.get('after_plan')
            }
            project_list.append((project_path, project_config))

    return project_list


def load_main_config(config_path, project_name):
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        return prepare_main_config(config, project_name)
    except Exception as e:
        logging.error(f"Error reading {config_path} - {str(e)}")
        return None
