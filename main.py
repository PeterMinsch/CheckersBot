import pygame
from ui.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from ui.game import Game
from ui.board import Board
from chessAgent.valueIteration import Agent

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def custom_hash(state, policy):
        
        
        # Ensure that the hash value is within the range of valid indices for the policy list
        state_index = state % len(policy)
        return state_index

import pygame
from ui.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from ui.game import Game
from ui.board import Board
from chessAgent.valueIteration import Agent

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def custom_hash(state, policy):
        
        
        # Ensure that the hash value is within the range of valid indices for the policy list
        state_index = state % len(policy)
        return state_index

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    chessAgent = Agent()
    
    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            print(game.winner())
            run = False
            continue  # Skip the rest of the loop if the game has ended

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game.turn == RED:  # User's turn (Red)
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                
        if game.turn == WHITE:  # Agent's turn (White)
            pieces_with_moves = [piece for piece in chessAgent.findAgentPieces() if chessAgent.board.get_valid_moves(piece)]
            chessAgent.nS = len(pieces_with_moves)
            chessAgent.nA = len(chessAgent.ACTION_SPACE)
            new_V, policy = chessAgent.valueIteration()
            
            for piece in pieces_with_moves:
                state_index = pieces_with_moves.index(piece)
                state_index = custom_hash(state_index, policy)
                if isinstance(state_index, int):
                    if 0 <= state_index < len(policy):
                        action_index = policy[state_index]
                        print(f"Action index for state {state_index}: {action_index}")
                        if isinstance(action_index, int) and 0 <= action_index < len(chessAgent.ACTION_SPACE):
                            action = chessAgent.ACTION_SPACE[action_index]
                            if action in game.board.get_valid_moves(piece):
                                game.move(*action)
                            else:
                                print("Invalid action selected by the agent:", action)
                        else:
                            print("Invalid action index:", action_index)
                    else:
                        print("State index out of range:", state_index)
                else:
                    print("Invalid state index:", state_index)

        game.update()
    
    pygame.quit()

    
main()
