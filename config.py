import os
from dotenv import load_dotenv
import yaml

def load_config(file_path):
    # Load environment variables from .env file
    load_dotenv()

    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)  # Use safe_load instead of safe_load_all

    # Ensure config is a dictionary before assigning
    if isinstance(config, dict):
        # Replace the token with the environment variable
        config['token'] = os.getenv('LICHESS_API_KEY')

    return config

# Usage
config = load_config('config.yml')


