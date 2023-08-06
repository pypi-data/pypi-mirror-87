import os
from pathlib import Path
from shutil import copyfile


def read_file(path):
    if isinstance(path, Path):
        path = str(path)
    if path.endswith("yml"):
        with open(path, 'r') as stream:
            import yaml
            # We let the user handle exceptions
            return yaml.safe_load(stream)
    elif path.endswith("ini"):
        from configparser import ConfigParser
        cp = ConfigParser()
        cp.read(path)
        return cp
    elif path.endswith("json"):
        import json
        with open(path, 'r') as stream:
            return json.loads(stream.read())
    else:
        raise ValueError(f"Unknown config extension: {path}")


def parse_config(template="config.ini"):
    # Get paths.
    config_example_path = template
    config_path = os.getenv("CONFIG_PATH", template)

    if not os.path.exists(config_path):
        dirname = os.path.dirname(config_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        copyfile(config_example_path, config_path)

    cfg = read_file(config_path)

    return cfg
