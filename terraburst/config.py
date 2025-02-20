import os
import yaml

CONFIG_FILENAMES = ["terraburst.yml", "terraburst.yaml"]


def load_config(directory):
    config_path = None
    for filename in CONFIG_FILENAMES:
        potential_path = os.path.join(directory, filename)
        if os.path.exists(potential_path):
            config_path = potential_path
            break

    if not config_path:
        print(f"Skipping {directory}: No terraburst.yml or terraburst.yaml found.")
        return None

    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        required_keys = ["workspace"] #, "var_file", "output_file", "variables"]
        missing_keys = [key for key in required_keys if key not in config]

        if missing_keys:
            print(f"Skipping {directory}: Missing keys in terraburst.yml: {', '.join(missing_keys)}")
            return None

        return config
    except Exception as e:
        print(f"Skipping {directory}: Error reading terraburst.yml - {str(e)}")
        return None
