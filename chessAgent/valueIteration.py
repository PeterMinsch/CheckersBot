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

    def __init__(self, board):
        self.board = board
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
        new_V = [0]*nS #initialize an array for nS size (new updated values)
        policy = [0]*nS #initialize an array for nS size (best action for each state)
        for s in range(nS): #fill policy and new_v arrays
            new_v = [0]*nA #initialize an array for all actions
            for a in range(nA): #fill action to take array
                #Let's consider only deterministic policy; P[][] is where all the (state,action)->(next_state,reward) probability, rewards are stored
                for prob, next_s, reward, terminal in P[s][a]: #
                    new_v[a] += prob * (reward + gamma * V[next_s]) #(1) fill in the blank: calculate the updated state value for action a at state s
            new_V[s] = max(new_v) #(2) fill in the blank: update the state value for state s to be the maximum state-action value
            policy[s] = np.argmax(new_V) #(3) fill in the blank: update the policy for state s to be the action that has the maximum state-action value
        return new_V, policy
        # pass
    

    '''
    this will loop through the board and find the agent's pieces and store them in a list.
    this list will represent our number of states
    '''
    
    def findAgentPieces(self):
        nP = [] #this is our list of states
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.getPiece(i, j): #if there is a piece
                    nP.append(self.board.getPiece(i,j))
        return nP
    
    '''
    This matrix will hold objects for each state and their actions. 
    Each slot holds a probability, reward, the next state, and if the next state holds a terminal state
    probality = .5
    reward = 1
    nextState = ?
    terminal = bool
    '''
    def calculateProbabilityMatrix(self):
        nP = self.findAgentPieces(self) #retreiving our list of "states"
        p = [[None for _ in range (COLS) for _ in range (ROWS)]]
        probability = .5
        reward = 1
        next_s = ()
        terminal = False
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.getPiece(i, j): #if there is a piece
                    nP.append(self.board.getPiece(i,j))
                    for k in nP:
                        if nP[k].color != WHITE: #no more white pieces on the board
                            terminal = True #set terminal to true
                    p[i][j] = State(probability, reward, next_s(i + 1, j + 1), terminal)

        return p


        

    
    