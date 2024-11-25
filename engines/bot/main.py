# engines/bot/main.py

import openai
import os
import chess
import random

def get_api_key():
    # Try to read the API key from the file
    try:
        with open('OPENAI_API_KEY', 'r') as file:
            api_key = file.read().strip()
            if api_key:
                return api_key
    except FileNotFoundError:
        pass

    # Try to get the API key from the environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key

    # Raise an error if the API key is not found
    raise ValueError("OpenAI API key not found. Please provide it in the OPENAI_API_KEY file or as an environment variable.")

# Set your OpenAI API key
openai.api_key = get_api_key()
client = openai.OpenAI(api_key=get_api_key())

def get_move(board):
    """
    Sends the FEN position and legal moves to ChatGPT and returns the best move.
    
    :param board: chess.Board, the current board position
    :return: str, the best move as determined by ChatGPT
    """
    # Ensure the board is a chess.Board instance
    if not isinstance(board, chess.Board):
        raise ValueError("The board must be an instance of chess.Board.")
    
    # Calculate legal moves from the board
    legal_moves = [move.uci() for move in board.legal_moves]

    # Create a prompt for ChatGPT
    prompt = f"Given the FEN position: {board.fen()} and the legal moves: {', '.join(legal_moves)}, what is the best move? Return the move and nothing else."

    # Call the OpenAI API using the new method
    response = client.chat.completions.create(
        model="gpt-4o",  # Use the appropriate model
        messages=[{"role": "system", "content": "You are a chess bot."},
                  {"role": "user", "content": prompt}],
        max_tokens=50  # Adjust the token limit as needed
    )
    
    # Extract the best move from the response
    best_move = response.choices[0].message.content.strip()
    
    # Debugging output
    print(f"API Response: {best_move}")

    # Validate the move
    if best_move not in legal_moves:
        print(f"Invalid move returned by API: {best_move}. Playing a random legal move instead.")
        best_move = random.choice(legal_moves)
    
    return best_move

'''
if __name__ == "__main__":
    # Example FEN and legal moves
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    legal_moves = ["e2e4", "d2d4", "g1f3", "c2c4"]

    best_move = get_move(fen, legal_moves)
    print(f"The best move is: {best_move}")
'''
