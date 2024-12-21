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
        prompt = f'''You are a highly sophisticated chess engine renowned for your deep tactical vision and strategic understanding.  Analyze the following chess position in detail, considering both immediate threats and long-term implications.
        **Current Chess Position (FEN):** {board.fen()} 
        **Legal Moves:** {', '.join(legal_moves)} 
        **Task:**
    1. **Identify and select the objectively best move from the provided list.** Base your selection on a thorough evaluation of the position, considering factors such as:
        * **Material balance:**  Gains or losses of pieces.
        * **King safety:**  Vulnerabilities of both kings.
        * **Piece activity and mobility:**  How well-placed and active the pieces are.
        * **Pawn structure:** Strengths and weaknesses of pawn formations.
        * **Control of key squares and files:**  Influence over important areas of the board.
        * **Potential threats and attacks:**  Immediate and future tactical possibilities.
        * **Strategic advantages:**  Long-term plans and positional superiority.
    2. **Provide a concise justification for your chosen move.**  Explain *why* it is the strongest option, highlighting the key factors that make it superior to the other legal moves.  Specifically mention:
        * **The immediate benefits of your chosen move.**
        * **How it improves your position and/or hinders your opponent's.**
        * **Potential future plans or threats enabled by this move.**
        * **Briefly explain why other strong-looking moves are less optimal in this specific situation.**''',
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
