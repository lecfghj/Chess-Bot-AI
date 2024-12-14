import chess
from queue import PriorityQueue

class ChessBotBFS:
    def __init__(self, max_depth, evaluator):
        # Maximum depth to explore moves
        self.max_depth = 2
        # Evaluation function to score board positions
        self.evaluator = evaluator
        self.nodes_explored = 0

    def get_best_move(self, board):

        best_move = None
        best_score = float('-inf')  # Initialize with a very low score

        max_depth = self.max_depth

        if (board.turn == chess.WHITE):
            current_player = chess.WHITE
        elif (board.turn == chess.BLACK):
            current_player = chess.BLACK

        # Iterate over all legal moves
        for move in board.legal_moves:
            # Get immediate score of the move
            current_score = self.evaluator.evaluate(board) 

            # Get the long-term score for this move by using greedy_best_move_score
            long_term_score = self.get_long_term_score(board, move, max_depth, current_player) 

            # Sum short-term score and long-term score
            combined_score = current_score + long_term_score

            # Check if this move has the highest combined score
            if combined_score > best_score:
                best_score = combined_score
                best_move = move

        return best_move

    def get_long_term_score(self, board, move, max_depth, current_player):
        is_maximizing_player = board.turn == current_player
       # Initialize local best scores for maximizing player/opponent
        if(is_maximizing_player):
            best_score = float('inf')
        else:
            best_score = float('-inf')

        def recursive_deepening(board, depth, best_score):
            
            is_maximizing_player = board.turn == current_player
            # Check if depth is 0 and return the evaluation
            if depth == 0:
                return self.evaluator.evaluate(board)

            # Explore all legal moves
            for next_move in board.legal_moves:
                board.push(next_move)
                self.nodes_explored += 1

                # Recursive call to evaluate the next depth
                score = recursive_deepening(board, depth - 1, best_score)

                # Update best score based on whether maximizing or minimizing
                if is_maximizing_player:
                    best_score = max(best_score, score)
                else:
                    best_score = min(best_score, score)

                board.pop()  # Undo the move

            return best_score

        # Apply the initial move
        board.push(move)
        self.nodes_explored += 1

        # Evaluate the board state recursively 
        best_score = recursive_deepening(board, max_depth - 1, best_score)

        # Undo the initial move
        board.pop()
        return best_score
