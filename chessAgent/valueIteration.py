from ui.board import Board
from ui.constants import ROWS, COLS
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
        self.nA = 2
        self.nS = len(self.findAgentPieces())
        self.V = [0] * self.nS
        self.P = self.calculateProbabilityMatrix()

    def valueIteration(self, V, P, nA, nS):
        gamma = 0.9
        new_V, policy = [0] * nS, [0] * nS

        for s in range(nS):
            new_v = [0] * nA
            for a in range(nA):
                if P[s][a] is None:
                    new_v[a] = -999  # Put -999 when P[s][a] is None
                    continue
                
                for transition in P[s][a]:
                    prob, next_s, reward, terminal = transition
                    new_v[a] += prob * (reward + gamma * V[next_s])
            new_V[s] = max(new_v)
            policy[s] = np.argmax(new_V)
        return new_V, policy

    def findAgentPieces(self):
        nP = []
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.get_piece(i, j):
                    nP.append(self.board.get_piece(i, j))
        return nP

    def determineProbability(self, moves):
        max_capture_count = 0
        for move, captured_pieces in moves.items():
            capture_count = len(captured_pieces)
            max_capture_count = max(max_capture_count, capture_count)

        best_moves = [0] * len(moves)
        for i, move in enumerate(moves):
            if len(moves[move]) == max_capture_count:
                best_moves[i] = 1

        return best_moves




    def calculateProbabilityMatrix(self):
        nP = self.findAgentPieces()
        p = [[None for _ in range(COLS)] for _ in range(ROWS)]

        for piece in nP:
            moves = self.board.get_valid_moves(piece)
            probabilities = self.determineProbability(moves)
            next_states = []

            for move, prob in zip(moves, probabilities):
                next_state = move
                reward = 1  # Assuming a constant reward for simplicity
                terminal = False  # Assuming no terminal states for simplicity
                next_states.append((next_state, prob, reward, terminal))

            # Populate P with the next states for each action (0 and 1 for example)
            p[piece.row][piece.col] = next_states

        return p

    # def calculateProbabilityMatrix(self):
    #     nP = self.findAgentPieces()
    #     p = [[None for _ in range(COLS)] for _ in range(ROWS)]

    #     for piece in nP:
    #         moves = self.board.get_valid_moves(piece)
    #         probabilities = self.determineProbability(moves)
    #         reward = 1
    #         next_states = []
    #         for move, prob in zip(moves, probabilities):
    #             next_state = move
    #             terminal = False
    #             next_states.append((next_state, prob, terminal))
    #         p[piece.row][piece.col] = State(probability=None, reward=reward, next_states=next_states, terminal=False)

    #     return p


    # def calculateProbabilityMatrix(self):
    #     nP = self.findAgentPieces() #retreiving our list of "states"
    #     p = [[None for _ in range (COLS) for _ in range (ROWS)]]
        
    #     # probability = self.determineProbability(nP[0])
    #     moves = self.board.get_valid_moves(nP[0]) #getting valid moves for our piece
    #     probabilities = self.determineProbability(moves)
    #     reward = 1
    #     next_s = ()
    #     terminal = False
    #     for i in range(ROWS):
    #         for j in range(COLS):
    #             if self.board.get_piece(i, j): #if there is a piece
    #                 nP.append(self.board.get_piece(i,j))
                    
    #                 p[i][j] = State(probability, reward, next_s(i + 1, j + 1), terminal)
    
    #     return p


        

    
    