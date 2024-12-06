"""
1. Storing the information about the current state of the chess game.
2. Determining the valid moves at the currrent state
3. Keeping a move-log
"""
import copy
import pygame as p
class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],  # Rook, kNight, Bishop, Queen, King, pawn
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],  # empty space with no piece
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]  # [w: white] - [b: black]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.middleGame = False
        self.endGame = False
        self.whiteChecked = False
        self.blackChecked = False
        self.nullMoveMade = False
        self.draw = False
        self.isPawnPromotion = False
        self.enPassantPossible = ()
        self.enPassantPossibleLog = [self.enPassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        self.history = []

    def saveState(self):
        boardState = [row[:] for row in self.board]
        self.history.append(boardState)


    def checkDraw(self):
        whitePieces = [square[1] for row in self.board for square in row if square.startswith('w') and square[1] != 'K']
        blackPieces = [square[1] for row in self.board for square in row if square.startswith('b') and square[1] != 'K']


        insufficientMaterial = (whitePieces in [['N', 'N'], ['N'], ['B'], []]) and \
                               (blackPieces in [['N', 'N'], ['N'], ['B'], []])

        self.draw = insufficientMaterial

    def updateGamePhase(self):
        totalPieces = sum([row.count('wR') + row.count('bR') +
                           row.count('wN') + row.count('bN') +
                           row.count('wB') + row.count('bB') +
                           row.count('wQ') + row.count('bQ') +
                           row.count('wp') + row.count('bp') + row.count('bK') + row.count('wK')
                           for row in self.board])
        if len(self.moveLog) > 14:
            self.middleGame = True
            self.endGame = False
        if len(self.moveLog) > 70 or totalPieces < 16:
            self.middleGame = False
            self.endGame = True
        else:
            self.middleGame = False
            self.endGame = False
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)


        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            global promotePiece
            promotePiece = 'Q'
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotePiece



        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'


        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enPassantPossible = ()


        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        self.enPassantPossibleLog.append(self.enPassantPossible)

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    def makeNullMove(self):
        self.whiteToMove = not self.whiteToMove

    def undoNullMove(self):
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        self.draw = False;
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)

            self.enPassantPossibleLog.pop()
            self.enPassantPossible = self.enPassantPossibleLog[-1]
            #if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                #self.enPassantPossible = ()

            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

            self.checkMate = False;
            self.staleMate = False;

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

        # Rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self .currentCastlingRight.bks = False

    def getAllCaptures(self):
        captures = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.board[row][col]
                if piece != "--" and piece[0] == ("w" if self.whiteToMove else "b"):
                    pieceMoves = self.getValidMoves()
                    for move in pieceMoves:
                        if self.board[move.endRow][move.endCol] != "--":
                            captures.append(move)
        return captures

    def getValidMoves(self):
        self.updateGamePhase()
        tempEnpassantPossible = self.enPassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)

        moves = self.getAllPossibleMoves()


        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])


            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            self.whiteChecked = True if self.squareUnderAttack(self.whiteKingLocation[0],
                                                               self.whiteKingLocation[1]) else False
            self.blackChecked = True if self.squareUnderAttack(self.blackKingLocation[0],
                                                               self.blackKingLocation[1]) else False
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
            self.blackChecked = True if self.squareUnderAttack(self.blackKingLocation[0],
                                                               self.blackKingLocation[1]) else False
            self.whiteChecked = True if self.squareUnderAttack(self.whiteKingLocation[0],
                                                               self.whiteKingLocation[1]) else False
        self.enPassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation
            if self.board[r - 1][c] == "--":
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            # inside between king and pawn, outside range between pawn and border
                            insideRange = range(kingCol + 1, c - 1)
                            outsideRange = range(c + 1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c - 2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != '--':  # some piece blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == 'b' and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r,c), (r-1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            # inside between king and pawn, outside range between pawn and border
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c + 2, 8)
                        else:
                            insideRange = range(kingCol - 1, c + 1, -1)
                            outsideRange = range(c - 1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != '--':  # some piece blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == 'b' and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r,c), (r-1, c+1), self.board, isEnpassantMove=True))

        else:
            kingRow, kingCol = self.blackKingLocation
            if self.board[r + 1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r,c), (r+2, c), self.board))

            if c - 1 >= 0:
                if self.board[r + 1][c-1][0] == "w":
                    moves.append(Move((r,c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            #inside between king and pawn, outside range between pawn and border
                            insideRange = range(kingCol + 1, c-1)
                            outsideRange = range(c+1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c-2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != '--': #some piece blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == 'w' and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r,c), (r+1, c-1), self.board, isEnpassantMove=True))
            if c + 1 <= 7:
                if self.board[r + 1][c+1][0] == "w":
                    moves.append(Move((r,c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            # inside between king and pawn, outside range between pawn and border
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c + 2, 8)
                        else:
                            insideRange = range(kingCol - 1, c + 1, -1)
                            outsideRange = range(c - 1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != '--':  # some piece blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == 'w' and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r,c), (r+1,c+1), self.board, isEnpassantMove=True))
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)


    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c), (r, c+2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r,c), (r, c-2), self.board, isCastleMove=True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():


    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.isCastleMove = isCastleMove
        self.isCapture = self.pieceCaptured != '--'
        self.reach50 = 0
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #gs = GameState()



    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):

        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



    def __str__(self):

        #castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)
        #pawn

        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        # pawn promotions

        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare
