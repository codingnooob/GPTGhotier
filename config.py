import os
from dotenv import load_dotenv
import yaml

def load_config(file_path):
    # Load environment variables from .env file
    load_dotenv()

    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Replace the token with the environment variable
    config['token'] = str(os.getenv('LICHESS_API_KEY'))

    return config

# Usage
config = load_config('config.yml')
