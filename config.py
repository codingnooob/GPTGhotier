import os
import yaml

def load_config(file_path):
    with open(file_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    config["token"] = os.getenv('LICHESS_API_KEY')

    with open(file_path, "w") as file:
        config = yaml.dump(
            config, stream=file, default_flow_style=False, sort_keys=False
        )

    return config

# Usage
#load_config('config.yaml')


