import pygame
from math import inf as infinity
from random import choice
import time

#CONSTANTS
WIDTH = 400
HEIGHT = 500
FONT = 'freesansbold.ttf'

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

#COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)


COORD = {
	1:( 50, 100),
	2:(150, 100),
	3:(250, 100),
	4:( 50, 200),
	5:(150, 200),
	6:(250, 200),
	7:( 50, 300),
	8:(150, 300),
	9:(250, 300),
}

"""
				DRAW FUNCTIONS
"""
def draw_rect(screen, bgC, fgC, x, y, w, h):
	pygame.draw.rect(screen, fgC,(x, y, w, h))
	pygame.draw.rect(screen, bgC,(x+1, y+1, w-2, h-2))
	
def text(screen, size, text, bg, fg, cx, cy):
	font = pygame.font.Font(FONT, size) 
	text = font.render(text, True, fg, bg) 
	textRect = text.get_rect()  
	textRect.center = (cx, cy)
	screen.blit(text, textRect)
	
def draw_board(screen, human):
	if human is 'X':
		comp = 'O'
	else:
		comp = 'X'
	for i in range(1, 10):
		draw_rect(screen, BLACK, WHITE, COORD[i][0], COORD[i][1], 100, 100)
		x = (i-1)//3
		y = (i-1)%3
		if board[x][y] is HUMAN:
			text(screen, 60, human, BLACK, WHITE, COORD[i][0]+50, COORD[i][1]+50)
		elif board[x][y] is COMP:
			text(screen, 60, comp, BLACK, WHITE, COORD[i][0]+50, COORD[i][1]+50)

"""
				BOARD FUNCTIONS
"""
def get_empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells
	
def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
    return score
	
def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]  
    else:
        best = [-1, -1, +infinity]  
		
    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score] 			

    for cell in get_empty_cells(state):		
        x, y = cell[0], cell[1]			
        state[x][y] = player		
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value
    return best

"""
			GAME LOOP
"""

def game_loop(screen, human, human_turn, w, d, l):
	running = True
	keep_playing = True
	while running:
		#PROCESS EVENTS
		x, y = pygame.mouse.get_pos()
		xC, yC = 0, 0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				keep_playing = False
			if event.type == pygame.MOUSEBUTTONUP:
				xC, yC = pygame.mouse.get_pos()
		#UPDATE
		if len(get_empty_cells(board)) == 0:
			message = 'Draw!'
			d += 1
			time.sleep(1.5)
			running = False
		if wins(board, HUMAN):
			message = 'You win!'
			w += 1
			time.sleep(1.5)
			running = False
		if wins(board, COMP):
			message = 'Computer win!'
			l += 1
			time.sleep(1.5)
			running = False
		
		
		if human_turn:
			if xC > 50 and yC > 100 and xC < 350 and yC < 400:
				x = (yC-100)//100
				y = (xC-50)//100
				if board[x][y] == 0:
					board[x][y] = HUMAN
					human_turn = False
		else:
			depth = len(get_empty_cells(board))
			
			if depth == 0 or game_over(board):
				running = False
				
			if depth == 9:
				x = choice([0, 1, 2])
				y = choice([0, 1, 2])
				board[x][y] = COMP
				human_turn = True
			elif depth == 8 and board[1][1] == HUMAN:
				x = choice([0, 2])
				y = choice([0, 2])
				board[x][y] = COMP
				human_turn = True
			else:
				copy = board[:]
				move = minimax(copy, depth, COMP)
				x, y = move[0], move[1]
				board[x][y] = COMP
				human_turn = True
		#DRAW
		screen.fill(BLACK)
		draw_board(screen, human)
		if human_turn and x > 50 and y > 100 and x < 350 and y < 400:
			xi = (x-50)//100
			yi = (y-100)//100
			if board[yi][xi] == 0:
				text(screen, 60, human, BLACK, GREY, 100+xi*100, 100*yi+150)
		pygame.display.flip()

	if keep_playing:	
		for i in range(0, 9):
			x = i//3
			y = i%3
			board[x][y] = 0
		menu_loop(screen, w, d, l, message)
		
"""
			MENU LOOP
"""

def menu_loop(screen, w, d, l, message=None):
	running = True
	while running:
		#PROCESS EVENTS
		x, y = pygame.mouse.get_pos()
		xC, yC = 0, 0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONUP:
				xC, yC = pygame.mouse.get_pos()
		#UPDATE
		bgColorX = BLACK
		bgColorO = BLACK	
		if x > 50 and x < 150 and y > 200 and y < 300:
			bgColorX = GREY
			
		if x > 250 and x < 350 and y > 200 and y < 300:
			bgColorO = GREY
			
		if xC > 50 and xC < 150 and yC > 200 and yC < 300:
			game_loop(screen, 'X', True, w, d, l)
			running = False
		if xC > 250 and xC < 350 and yC > 200 and yC < 300:
			game_loop(screen, 'O', False, w, d, l)
			running = False
		
		#DRAW
		screen.fill(BLACK)
		draw_rect(screen, bgColorX, WHITE, 50, 200, 100, 100)
		draw_rect(screen, bgColorO, WHITE, 250, 200, 100, 100)
		draw_rect(screen, GREY, BLACK, 0, 450, 400, 50)
		if message:
			text(screen, 30, message, BLACK, WHITE, 200, 380)
		text(screen, 30, 'X', bgColorX, WHITE, 100, 250)
		text(screen, 30, 'O', bgColorO, WHITE, 300, 250)
		text(screen, 12, '1st', bgColorX, WHITE, 135, 290)
		text(screen, 12, '2nd', bgColorO, WHITE, 335, 290)
		text(screen, 24, 'Tic Tac Toe Game', BLACK, WHITE, 200, 100)
		text(screen, 20, 'Select one:', BLACK, WHITE, 200, 160)
		text(screen, 15, 'Wins: ' + str(w), GREY, WHITE, 50, 475)
		text(screen, 15, 'Draws: ' + str(d), GREY, WHITE, 200, 475)
		text(screen, 15, 'Loses: ' + str(l), GREY, WHITE, 350, 475)
		
		pygame.display.flip()

def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Tic Tac Toe')
	
	menu_loop(screen, 0, 0, 0)

	pygame.quit()

if __name__ == '__main__':
    main()



