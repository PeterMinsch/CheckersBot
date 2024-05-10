from ui.constants import ROWS, COLS, RED, WHITE
from ui.board import Board
from ui.piece import Piece
import numpy as np

class State:
    def __init__(self, probability, reward, next_states, terminal):
        self.probability = probability
        self.reward = reward
        self.next_states = next_states
        self.terminal = terminal

class Agent:
    def __init__(self):
        self.board = Board()
        self.agent_pieces = self.findAgentPieces()  # Store the list of agent pieces
        self.nS = len(self.agent_pieces)  # Number of agent pieces
        self.ACTION_SPACE = self.createActionSpace()
        self.nA = len(self.ACTION_SPACE)
        self.V = np.zeros(self.nS)
        self.P = self.calculateProbabilityMatrix()

    def valueIteration(self, gamma=0.9, max_iterations=100):
        for _ in range(max_iterations):
            delta = 0
            for s in range(self.nS):
                v = self.V[s]
                new_v = np.zeros(self.nA)
                for a in range(self.nA):
                    transitions = self.P[s]
                    for prob, next_s_index, reward, terminal in transitions:
                        new_v[a] += prob * (reward + gamma * self.V[next_s_index])
                self.V[s] = max(new_v)
                delta = max(delta, abs(v - self.V[s]))
            if delta < 1e-6:
                break

        return self.V, self.P

    def calculateProbabilityMatrix(self):
        P = [[] for _ in range(self.nS)]  # Initialize P with correct size
        for agent_piece_index, piece in enumerate(self.agent_pieces):
            transitions = []
            moves = self.board.get_valid_moves(piece)
            total_prob = len(moves)
            for move, _ in moves.items():
                if isinstance(move, tuple) and len(move) > 0:
                    next_pos = move[0]  # Get the first position in the tuple
                    if isinstance(next_pos, tuple) and len(next_pos) == 2:
                        next_row, next_col = next_pos
                        next_s_index = next_row * COLS + next_col
                        reward = 1
                        terminal = False
                        prob = 1 / total_prob
                        transitions.append((prob, next_s_index, reward, terminal))
                    else:
                        print("Invalid position in move:", next_pos)
                elif isinstance(move, list) and len(move) > 0:
                    for next_pos in move:
                        if isinstance(next_pos, tuple) and len(next_pos) == 2:
                            next_row, next_col = next_pos
                            next_s_index = next_row * COLS + next_col
                            reward = 1
                            terminal = False
                            prob = 1 / total_prob
                            transitions.append((prob, next_s_index, reward, terminal))
                        else:
                            print("Invalid position in move:", next_pos)
                elif not move:
                    print("Empty move detected:", move)
            if transitions:
                P[agent_piece_index] = transitions
        return P

    def findAgentPieces(self):
        agent_pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece is not None and piece != 0 and piece.color == WHITE:
                    if self.board.get_valid_moves(piece):
                        agent_pieces.append(piece)  # Append the piece to the list
        return agent_pieces

    def createActionSpace(self):
        action_space = {}
        for i in range(self.nS):
            action_space[i] = i  # Action index corresponds to state index
        return action_space
