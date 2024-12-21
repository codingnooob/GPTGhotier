# engines/bot/main.py

import openai
import os
import chess
import random
import re

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
    # prompt = f"Given the FEN position: {board.fen()} and the legal moves: {', '.join(legal_moves)}, what is the best move? Return the move and nothing else."

    # Call the OpenAI API using the new method
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Use the appropriate model
        prompt = f"You are the most advanced chess engine, capable of analyzing positions with unparalleled depth and accuracy. Given the current chess position described by the FEN notation: {board.fen()}, please select the optimal move from the following legal moves: {', '.join(legal_moves)}. In your response, please provide the move in algebraic notation and include a detailed explanation of why this move is considered the best, taking into account both tactical possibilities and strategic considerations. Additionally, if possible, compare this move to the alternatives and explain why they are less favorable.",
        #messages=[{"role": "system", "content": "You are a chess bot."},
        #         {"role": "user", "content": prompt}],
        max_tokens=1000,  # Adjust the token limit as needed
        api_key=openai.api_key
    )
    
    # Extract the best move from the response
    response_text = response.choices[0].text.strip()
    print(f"API Response: {response_text}")
    
    # Try to find a chess move in the response (4 character sequences like e2e4)
    moves = re.findall(r'[a-h][1-8][a-h][1-8]', response_text)
    
    # Use first valid move found
    for move in moves:
        if move in legal_moves:
            return move
            
    # Fallback to random move if no valid move found
    print(f"No valid move found in response. Playing random move instead.")
    return random.choice(legal_moves)

'''
if __name__ == "__main__":
    # Example FEN and legal moves
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    legal_moves = ["e2e4", "d2d4", "g1f3", "c2c4"]

    best_move = get_move(fen, legal_moves)
    print(f"The best move is: {best_move}")
'''
