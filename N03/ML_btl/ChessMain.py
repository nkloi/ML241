"""
1. Handling user input and displaying the current Gamestate
"""
import pygame as p
import Engine, ChessAI
from multiprocessing import Process, Queue
import os
MAX_FPS = 10 #animations later on
BOARD_WIDTH = BOARD_HEIGHT = 480
MOVE_LOG_PANEL_WIDTH = 3*BOARD_WIDTH/8
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8 #chess board are 8 x 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
IMAGES = {}
p.mixer.init()
NotifySoundPlayed = False
CastleSoundPlayed = False
CaptureSoundPlayed = False
PromoteSoundPlayed = False
whiteCheckSoundPlayed = False
blackCheckSoundPlayed = False
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
promote_sound = p.mixer.Sound(os.path.join(BASE_DIR, 'sounds', 'promote.mp3'))
castle_sound = p.mixer.Sound(os.path.join(BASE_DIR, 'sounds', 'castle.mp3'))
check_sound = p.mixer.Sound(os.path.join(BASE_DIR, 'sounds', 'move-check.mp3'))
capture_sound = p.mixer.Sound(os.path.join(BASE_DIR, 'sounds', 'capture.mp3'))
move_sound = p.mixer.Sound(os.path.join(BASE_DIR, 'sounds', 'move-self.mp3'))
notify_sound = p.mixer.Sound(os.path.join(BASE_DIR, 'sounds', 'notify.mp3'))

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(os.path.join(BASE_DIR, "images", piece + ".png")), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    p.mixer.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT + SQ_SIZE/2))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Helvetica", 15, False, False)
    gs = Engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag for when a move is made
    animate = False #flag for the animation
    loadImages()
    running = True
    sqSelected = () #no square is selected, track of the last click of user
    playerClicks = [] #track of player clicks
    gameOver = False
    playerOne = True #white, True: human, False: AI
    playerTwo = True #Same like above
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False
    while running:
        #gs.checkDraw()
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() # get (x,y) of mouse
                    col = location[0] // SQ_SIZE # mapping to piece
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8: #clicked the same square twice
                        sqSelected = ()
                        playerClicks = [] #clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #append for 1st + 2nd clicks
                    if len(playerClicks) == 2 and humanTurn: #after 2nd click
                        move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                gs.saveState()
                                animate = True
                                sqSelected = () #reset
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key ==p.K_z: # 'z' is undo
                    gs.undoMove()
                    if gs.history:
                        gs.history.pop()
                    gs.draw = False
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True


                if e.key == p.K_i: # 'i' is reset the game
                    gs = Engine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    gs.draw = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

                if e.key == p.K_1:
                    playerOne = True
                    playerTwo = False
                if e.key == p.K_2:
                    playerOne = False
                    playerTwo = True
                if e.key == p.K_3:
                    playerOne = True
                    playerTwo = True
                if e.key == p.K_4:
                    playerOne = False
                    playerTwo = False




        #AI move finder
        if not gameOver and not humanTurn and not moveUndone:

            if not AIThinking:
                AIThinking = True
                print('thinking...')
                returnQueue = Queue() #used to pass data between threads
                moveFinderProcess = Process(target=ChessAI.findBestMove, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start()

            if not moveFinderProcess.is_alive():
                print("done thinking")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = ChessAI.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade = True
                animate = True
                AIThinking = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkMate or gs.staleMate or gs.draw:
            gameOver = True
            #if not gs.draw:
                #drawEndGameText(screen, ' STALEMATE ' if gs.staleMate else ' BLACK WON ' if gs.whiteToMove else ' WHITE WON ')
            #if gs.draw:
            if not gs.draw:
                drawEndGameText(screen,' STALEMATE ' if gs.staleMate else ' BLACK WON ' if gs.whiteToMove else ' WHITE WON ')
            if gs.draw:
                drawEndGameText(screen, ' DRAW ')
            if not NotifySoundPlayed:
                notify_sound.play()
                NotifySoundPlayed = True
        else:
            NotifySoundPlayed = False

        clock.tick(MAX_FPS)
        p.display.flip()
def highlightSquares(screen, gs, validMoves, sqSelected):
    global whiteCheckSoundPlayed, blackCheckSoundPlayed, CastleSoundPlayed, PromoteSoundPlayed

    if gs.whiteChecked:
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("red"))
        screen.blit(s, (gs.whiteKingLocation[1] * SQ_SIZE, gs.whiteKingLocation[0] * SQ_SIZE))
        if not whiteCheckSoundPlayed:
            check_sound.play()
            whiteCheckSoundPlayed= True
    if gs.blackChecked:
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("red"))
        screen.blit(s, (gs.blackKingLocation[1] * SQ_SIZE, gs.blackKingLocation[0] * SQ_SIZE))
        if not blackCheckSoundPlayed:
            check_sound.play()
            blackCheckSoundPlayed = True
    if not gs.whiteChecked:
        whiteCheckSoundPlayed = False
    if not gs.blackChecked:
        blackCheckSoundPlayed = False
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("green")) #cyan
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color("yellow")) #green
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen) #draw square pieces
    drawLabels(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw chess pieces
    drawMoveLog(screen, gs, moveLogFont)
def drawBoard(screen):
    global colors
    colors = [p.Color("light yellow"), p.Color("light blue")]
    for r in range(DIMENSION):
        for c in range (DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
def drawLabels(screen):
    font = p.font.SysFont("Arial", 18, False, False)
    for i in range(DIMENSION):
        letter = chr(ord('a') + i )
        color = p.Color('black') if (i % 2) == 0 else p.Color('black')
        text = font.render(letter, True, color)
        x_position = i * SQ_SIZE + SQ_SIZE // 2 - text.get_width() // 2
        y_position = BOARD_HEIGHT + SQ_SIZE/10
        screen.blit(text, (x_position, y_position))

    for i in range(DIMENSION):
        number = str(8 - i)
        color = p.Color('black') if (i % 2) == 0 else p.Color('black')
        text = font.render(number, True, color)
        x_position = BOARD_WIDTH + SQ_SIZE/6
        y_position = i * SQ_SIZE + SQ_SIZE // 2 - text.get_height() // 2
        screen.blit(text, (x_position, y_position))
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
def animateMove(move, screen, board, clock):
    global colors, CaptureSoundPlayed
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC))*framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                endPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, endPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
            if not CaptureSoundPlayed:
                capture_sound.play()
                CaptureSoundPlayed = True
        else:
            CaptureSoundPlayed = False

        if move.pieceMoved != '--':
            screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    move_sound.play()
def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 36, True, False)
    textObject = font.render(text, 0, p.Color('light blue'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2, BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('blue'))
    screen.blit(textObject, textLocation.move(2,2))
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH + SQ_SIZE/2, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT + SQ_SIZE)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = "#" + str(i//2 + 1) + ".  " + str(moveLog[i]) + "    "
        if i+1 < len(moveLog): #check if black made a move
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)

    movesPerRow = 1
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j] + "    "
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

if __name__ == '__main__':
    main()




