pip install pygame
pip install requests
import pygame
import requests
import random


global KEY
KEY = "f17eeaa0-b0e8-11eb-85dc-792aa5713150eec5b335-39e6-4729-abe7-7432d70343a0"



EMPTY = "EMPTY"
OPPONENT = "OPPONENT"   
PLAYER = "PLAYER"       


top_left = "top_left"
top_middle = "top_middle"
top_right = "top_right"
middle_left = "middle_left"
middle_middle = "middle_middle"
middle_right = "middle_right"
bottom_left = "bottom_left"
bottom_middle = "bottom_middle"
bottom_right = "bottom_right"

deconvert = {}
deconvert[top_left] = 0
deconvert[top_middle] = 1
deconvert[top_right] = 2
deconvert[middle_left] = 3
deconvert[middle_middle] = 4
deconvert[middle_right] = 5
deconvert[bottom_left] = 6
deconvert[bottom_middle] = 7
deconvert[bottom_right] = 8


HUMAN = "HUMAN"
COMPUTER = "COMPUTER"

gamehistory = {
    HUMAN : [],
    COMPUTER : []
}

decisions = {
    HUMAN : [],
    COMPUTER : []
}


def classify(board):
    debug("Predicting the next best move for the computer")


    url = "https://machinelearningforkids.co.uk/api/scratch/"+ KEY + "/classify"

    response = requests.get(url, params={
        "data" : get_board_from_perspective(board, COMPUTER)
    })

    if response.ok:
        responseData = response.json()

        for prediction in responseData:

            if is_space_empty(board, prediction["class_name"]):
                return prediction

        for space in random.sample(deconvert.keys(), len(deconvert)):

            if is_space_empty(board, space):
                return { "class_name" : space }
    else:

        print(response.json())
        response.raise_for_status()


def add_to_train(board, who, name_of_space):
    print ("Adding the move in %s by %s to the training data" % (name_of_space, who))

    url = "https://machinelearningforkids.co.uk/api/scratch/"+ KEY + "/train"

    response = requests.post(url, json={

        "data" : get_board_from_perspective(board, who),
        
        "label" : name_of_space
    })

    if response.ok:
        
        pass
    else:
     
        print(response.json())
        response.raise_for_status()

def train_new_model():
    print ("Training a new machine learning model")

    url = "https://machinelearningforkids.co.uk/api/scratch/"+ KEY + "/models"
    response = requests.post(url)

    if response.ok:
    
        pass
    else:
        
        print(response.json())
        response.raise_for_status()


def learn_from_this(winner, boardhistory, winnerdecisions):
    print("%s won the game!" % (winner))
    print("Maybe the computer could learn from %s's experience?" % (winner))
    for idx in range(len(winnerdecisions)):
        print("\nAt the start of move %d the board looked like this:" % (idx + 1))
        print(boardhistory[idx])
        print("And %s decided to put their mark in %s" % (winner, winnerdecisions[idx]))


def get_space_location(name_of_space):
    
    if name_of_space in deconvert:
        return deconvert[name_of_space]
    
    return deconvert[globals()[name_of_space]]


def get_space_contents(board, name_of_space):
    return board[get_space_location(name_of_space)]


def is_space_empty(board, name_of_space):
    return get_space_contents(board, name_of_space) == EMPTY

def create_empty_board():
    debug("Creating the initial empty game board state")
    return [ EMPTY, EMPTY, EMPTY,
             EMPTY, EMPTY, EMPTY,
             EMPTY, EMPTY, EMPTY ]


def get_board_from_perspective(board, who):
    convertedboard = []
    for move in board:
        if move == EMPTY:
           
            convertedboard.append(EMPTY)
        else:
            convertedboard.append(PLAYER if move == who else OPPONENT)
    return convertedboard

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


game_board_coordinates = {}
game_board_coordinates[top_left] = {
    "bottom_left_corner": (120, 120),
    "top_right_corner": (180, 180),
    "top_left_corner": (180, 120),
    "bottom_right_corner": (120, 180),
    "centre": (150, 150)
}
game_board_coordinates[top_middle] = {
    "bottom_left_corner": (220, 120),
    "top_right_corner": (280, 180),
    "top_left_corner": (220, 180),
    "bottom_right_corner": (280, 120),
    "centre": (250, 150)
}
game_board_coordinates[top_right] = {
    "bottom_left_corner": (320, 120),
    "top_right_corner": (380, 180),
    "top_left_corner": (320, 180),
    "bottom_right_corner": (380, 120),
    "centre": (350, 150)
}
game_board_coordinates[middle_left] = {
    "bottom_left_corner": (120, 220),
    "top_right_corner": (180, 280),
    "top_left_corner": (120, 280),
    "bottom_right_corner": (180, 220),
    "centre": (150, 250)
}
game_board_coordinates[middle_middle] = {
    "bottom_left_corner": (220, 220),
    "top_right_corner": (280, 280),
    "top_left_corner": (220, 280),
    "bottom_right_corner": (280, 220),
    "centre": (250, 250)
}
game_board_coordinates[middle_right] = {
    "bottom_left_corner": (320, 220),
    "top_right_corner": (380, 280),
    "top_left_corner": (320, 280),
    "bottom_right_corner": (380, 220),
    "centre": (350, 250)
}
game_board_coordinates[bottom_left] = {
    "bottom_left_corner": (120, 320),
    "top_right_corner": (180, 380),
    "top_left_corner": (120, 380),
    "bottom_right_corner": (180, 320),
    "centre": (150, 350)
}
game_board_coordinates[bottom_middle] = {
    "bottom_left_corner": (220, 320),
    "top_right_corner": (280, 380),
    "top_left_corner": (220, 380),
    "bottom_right_corner": (280, 320),
    "centre": (250, 350)
}
game_board_coordinates[bottom_right] = {
    "bottom_left_corner": (320, 320),
    "top_right_corner": (380, 380),
    "top_left_corner": (320, 380),
    "bottom_right_corner": (380, 320),
    "centre": (350, 350)
}

def display_winner(screen, board, who):
    debug("Checking if %s has won" % (who))

    gameover = False


    linecolour = GREEN if who == HUMAN else RED


    if get_space_contents(board, "top_left") == who and get_space_contents(board, "top_middle") == who and get_space_contents(board, "top_right") == who:
        pygame.draw.line(screen, linecolour, (100, 150), (400, 150), 10)
        gameover = True
    if get_space_contents(board, "middle_left") == who and get_space_contents(board, "middle_middle") == who and get_space_contents(board, "middle_right") == who:
        pygame.draw.line(screen, linecolour, (100, 250), (400, 250), 10)
        gameover = True
    if get_space_contents(board, "bottom_left") == who and get_space_contents(board, "bottom_middle") == who and get_space_contents(board, "bottom_right") == who:
        pygame.draw.line(screen, linecolour, (100, 350), (400, 350), 10)
        gameover = True

  
    if get_space_contents(board, "top_left") == who and get_space_contents(board, "middle_left") == who and get_space_contents(board, "bottom_left") == who:
        pygame.draw.line(screen, linecolour, (150, 100), (150, 400), 10)
        gameover = True
    if get_space_contents(board, "top_middle") == who and get_space_contents(board, "middle_middle") == who and get_space_contents(board, "bottom_middle") == who:
        pygame.draw.line(screen, linecolour, (250, 100), (250, 400), 10)
        gameover = True
    if get_space_contents(board, "top_right") == who and get_space_contents(board, "middle_right") == who and get_space_contents(board, "bottom_right") == who:
        pygame.draw.line(screen, linecolour, (350, 100), (350, 400), 10)
        gameover = True

    if get_space_contents(board, "top_left") == who and get_space_contents(board, "middle_middle") == who and get_space_contents(board, "bottom_right") == who:
        pygame.draw.line(screen, linecolour, (100, 100), (400, 400), 15)
        gameover = True
    if get_space_contents(board, "bottom_left") == who and get_space_contents(board, "middle_middle") == who and get_space_contents(board, "top_right") == who:
        pygame.draw.line(screen, linecolour, (400, 100), (100, 400), 15)
        gameover = True

    if gameover:

        pygame.display.update()

    return gameover

def redraw_screen(screen, colour, board):
    debug("Changing the background colour")

    screen.fill(colour)

    draw_game_board(screen)

    for spacename in deconvert.keys():
        space_code = deconvert[spacename]

        if board[space_code] == HUMAN:
            draw_move(screen, spacename, "cross")
        elif board[space_code] == COMPUTER:
            draw_move(screen, spacename, "nought")


    pygame.display.update()




def draw_game_board(screen):
    pygame.draw.rect(screen, WHITE, (195, 100, 10, 300))
    pygame.draw.rect(screen, WHITE, (295, 100, 10, 300))
    pygame.draw.rect(screen, WHITE, (100, 195, 300, 10))
    pygame.draw.rect(screen, WHITE, (100, 295, 300, 10))




def prepare_game_window():
    debug("Setting up the game user interface")
    
    pygame.init()
    
    screen = pygame.display.set_mode((300, 300))
    
    pygame.display.set_caption("Machine Learning Noughts and Crosses")
    return screen


def generate_random_colour():
    debug("Generating a random colour code")
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return [r, g, b]



def draw_move(screen, name_of_space, move):
    debug("Drawing a move on the game board : %s in %s" % (move, name_of_space))

    if move == "nought":
        location = game_board_coordinates[name_of_space]["centre"]
        pygame.draw.circle(screen, WHITE, location, 35 , 8)
    elif move == "cross":
        pygame.draw.line(screen, WHITE,
                         game_board_coordinates[name_of_space]["bottom_left_corner"],
                         game_board_coordinates[name_of_space]["top_right_corner"],
                         10)
        pygame.draw.line(screen, WHITE,
                         game_board_coordinates[name_of_space]["top_left_corner"],
                         game_board_coordinates[name_of_space]["bottom_right_corner"],
                         10)
    pygame.display.update()


def get_click_location(mx, my):
    debug("Getting location of click in %d,%d" % (mx, my))
    if 100 < mx < 400 and 100 < my < 400:
        if my < 200:
            if mx < 200:
                return top_left
            elif mx < 300:
                return top_middle
            else:
                return top_right
        elif my < 300:
            if mx < 200:
                return middle_left
            elif mx < 300:
                return middle_middle
            else:
                return middle_right
        else:
            if mx < 200:
                return bottom_left
            elif mx < 300:
                return bottom_middle
            else:
                return bottom_right
    return "none"


def game_move(screen, board, name_of_space, identity):
    debug("Processing a move for %s who chose %s" % (identity, name_of_space))


    symbol = "cross" if identity == HUMAN else "nought"

   
    draw_move(screen, name_of_space, symbol)

    gamehistory[identity].append(board.copy())
    decisions[identity].append(name_of_space)

    movelocation = get_space_location(name_of_space)
    board[movelocation] = identity

    gameover = display_winner(screen, board, identity)
    if gameover:

        learn_from_this(identity, gamehistory[identity], decisions[identity])

    if len(decisions[HUMAN]) + len(decisions[COMPUTER]) >= 9:
        gameover = True

    return gameover

def let_computer_play(screen, board):
    computer_move = classify(board)
    print(computer_move)
    return game_move(screen, board, computer_move["class_name"], COMPUTER)


def debug(msg):

    pass



debug("Configuration")
debug("Using identities %s %s %s" % (EMPTY, PLAYER, OPPONENT))
debug(deconvert)

debug("Initial startup and setup")
screen = prepare_game_window()
board = create_empty_board()
redraw_screen(screen, generate_random_colour(), board)

debug("Initialising game state variables")
running = True
gameover = False

debug("Deciding who will play first")
computer_goes_first = random.choice([False, True])
if computer_goes_first:
    let_computer_play(screen, board)


while running:

    event = pygame.event.wait()

    if event.type == pygame.QUIT:
        running = False

    if event.type == pygame.MOUSEBUTTONDOWN and gameover == False:

        mx, my = pygame.mouse.get_pos()
        location_name = get_click_location(mx, my)

        if location_name == "none":

            redraw_screen(screen, generate_random_colour(), board)

        elif is_space_empty(board, location_name):

            gameover = game_move(screen, board, location_name, HUMAN)


            if gameover == False:
             
                gameover = let_computer_play(screen, board)

        pygame.event.clear()

pygame.quit()

