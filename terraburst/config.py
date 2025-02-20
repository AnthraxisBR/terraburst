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