from ui.board import Board #imported board object from ui
from ui.constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE #import constants from ui 
from ui.piece import Piece #import piece from ui
import numpy as np

'''
loop through the board
use value iteration for each red piece
'''

'''
the state holds probability, reward, the next state, and if the next state holds a terminal state
'''
class State:
    def __init__(self, probability, reward, nextState, terminal):
        self.probability = probability
        self.reward = reward
        self.nextState = nextState
        self.terminal = terminal

class Agent:

    def __init__(self):
        self.board = Board()
        self.nA = 2 # number of actions
        self.nS = len(self.findAgentPieces()) # number of states
        self.V = [0] * self.nS # initial state values
        self.P = self.calculateProbabilityMatrix()
        
    ''' 
    params- 
    V- initial state values
    P- Proability matrix
    nA- Number of actions
    nS- Number of states

    '''
    def valueIteration(V, P, nA, nS):
        gamma = 0.9
        new_V, policy = [0]*nS #initialize an array for nS size (new updated values)
        
        for s in range(nS): #fill policy and new_v arrays
            new_v = [0]*nA #initialize an array for all actions
            for a in range(nA): #fill action to take array
                #Let's consider only deterministic policy; P[][] is where all the (state,action)->(next_state,reward) probability, rewards are stored
                for prob, next_s, reward, terminal in P[s][a]: #
                    new_v[a] += prob * (reward + gamma * V[next_s]) 
            new_V[s] = max(new_v) 
            policy[s] = np.argmax(new_V) 
        return new_V, policy
        
    

    '''
    this will loop through the board and find the agent's pieces and store them in a list.
    this list will represent our number of states
    '''
    def findAgentPieces(self):
        nP = [] #this is our list of states
        for i in range(ROWS):
            for j in range(COLS):
                print(f"i is {i} and {j}")
                if self.board.get_piece(i, j): #if there is a piece
                    nP.append(self.board.get_piece(i,j))
        return nP
    

    
    
    '''
    This function will determine the probability of the action to take
    it will take in 2 actions
    0 - if we decide not to take the action
    1- if we decide to take the action
    '''
    def determineProbability(moves):
        max_capture_count = 0
        
        
        for move, captured_pieces in moves.items():
            capture_count = len(captured_pieces)
            max_capture_count = max(max_capture_count, capture_count)
        
        # Create a list to store the best move indicator (1 for best, 0 for not best)
        best_moves = [0] * len(moves)
        
        # Set the indicator for the moves with maximum captured pieces to 1
        for i, (move, captured_pieces) in enumerate(moves.items()):
            if len(captured_pieces) == max_capture_count:
                best_moves[i] = 1
        
        return best_moves

    '''
    This matrix will hold objects for each state and their actions. 
    Each slot holds a probability, reward, the next state, and if the next state holds a terminal state
    probality = .5
    reward = 1
    nextState = ?
    terminal = bool
    '''
    def calculateProbabilityMatrix(self):
        nP = self.findAgentPieces()  # retrieving our list of "states"
        p = [[None for _ in range(COLS)] for _ in range(ROWS)]  # Initialize the probability matrix

        for piece in nP:
            moves = self.board.get_valid_moves(piece)  # getting valid moves for our piece
            probabilities = self.determineProbability(moves)
            reward = 1  # Assuming a constant reward for simplicity
            next_states = []  # List to store possible next states
            for move, prob in probabilities.items():
                next_state = move  # The next state is the move itself in this case
                terminal = False  # Terminal state is False since the game is ongoing
                next_states.append((next_state, prob, terminal))  # Append next state, probability, and terminal flag

            # Set the state for the current piece in the probability matrix
            p[piece.row][piece.col] = State(probability=None, reward=reward, next_state=next_states, terminal=False)

        return p


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


        

    
    