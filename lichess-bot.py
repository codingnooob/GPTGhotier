"""Starting point for lichess-bot."""
from config import load_config
from lib.lichess_bot import start_program

if __name__ == "__main__":
    load_config('config.yml')
    start_program()
