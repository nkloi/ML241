import random
#import chess.engine
#import chess
pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "p": 100}
pieceThreaten ={'p': 30, 'R': 170, 'N': 140, 'B': 140, 'Q': 200, 'K': 220}
pieceProtect ={'p': 120, 'R': 210, 'N': 180, 'B': 180, 'Q': 240, 'K': 300}
#for opening
kingScores = [[-30, -40, -40, -50, -50, -40, -40, -30],
              [-30, -40, -40, -50, -50, -40, -40, -30],
              [-80, -70, -60, -80, -80, -60, -70, -80],
              [-40, -60, -50, -60, -60, -50, -60, -40],
              [-20, -30, -40, -50, -50, -40, -30, -20],
              [-10, -20, -20, -30, -30, -20, -20, -10],
              [20,  20,   0,   0,   0,   0,  20,  20],
              [20,  30,  10,   0,   0,  10,  30,  20]]
knightScores = [[-50, -40, -30, -20, -20, -30, -40, -50],
              [-40, -15,   0,   0,   0,   0, -15, -40],
              [-30,   0,  10,  15,  15,  10,   0, -30],
              [-20,   5,  15,  20,  20,  15,   5, -20],
              [-20,   0,  15,  20,  20,  15,   0, -20],
              [-30,   5,  10,  15,  15,  10,   5, -30],
              [-40, -15,   0,   5,   5,   0, -15, -40],
              [-50, -40, -30, -20, -20, -30, -40, -50]]
bishopScores =   [[ -20, -10, -10, -10, -10, -10, -10, -20],
                  [-10,   0,   0,   0,   0,   0,   0, -10],
                  [-10,   0,   5,  10,  10,   5,   0, -10],
                  [-10,   5,   5,  10,  10,   5,   5, -10],
                  [-10,   0,  10,  10,  10,  10,   0, -10],
                  [-10,  10,  10,  10,  10,  10,  10, -10],
                  [-10,   5,   0,   0,   0,   0,   5, -10],
                  [-20, -10, -10, -10, -10, -10, -10, -20]]
rookScores = [[ 0,   0,   0,   0,   0,   0,   0,   0],
                [5,  10,  10,  10,  10,  10,  10,   5],
               [-5,   0,   0,   0,   0,   0,   0,  -5],
               [-5,   0,   0,   0,   0,   0,   0,  -5],
               [-5,   0,   0,   0,   0,   0,   0,  -5],
               [-5,   0,   0,   0,   0,   0,   0,  -5],
               [-5,   0,   0,   0,   0,   0,   0,  -5],
               [ 0,   0,   0,   5,   5,   0,   0,   0]]
queenScores = [[-20, -10, -10,  -5,  -5, -10, -10, -20],
              [-10,   0,   0,   0,   0,   0,   0, -10],
              [-10,   0,   5,   5,   5,   5,   0, -10],
              [ -5,   0,   5,   5,   5,   5,   0,  -5],
              [  0,   0,   5,   5,   5,   5,   0,  -5],
              [-10,   5,   5,   5,   5,   5,   0, -10],
              [-10,   0,   5,   0,   0,   0,   0, -10],
              [-20, -10, -10,  -5,  -5, -10, -10, -20]]
pawnScores = [[  0,   0,   0,   0,   0,   0,   0,   0],
              [  0,   0,   0,   0,   0,   0,   0,   0],
              [ -5,   0,   5,  20,  20,   5,   0,  -5],
              [-10,   0,  10,  30,  30,  10,   0, -10],
              [-10,   0,   5,  20,  20,   5,   0, -10],
              [  0,   0,   0,   0,   0,   0,   0,   0],
              [  0,   0,   0, -20, -20,   0,   0,   0],
              [  0,   0,   0,   0,   0,   0,   0,   0]]
#mid and endgame
kingEndgameScores =  [[-50, -40, -30, -20, -20, -30, -40, -50],
                      [-30, -20, -10,   0,   0, -10, -20, -30],
                      [-30, -10,  20,  30,  30,  20, -10, -30],
                      [-30, -10,  30,  40,  40,  30, -10, -30],
                      [-30, -10,  30,  40,  40,  30, -10, -30],
                      [-30, -10,  20,  30,  30,  20, -10, -30],
                      [-30, -30,   0,   0,   0,   0, -30, -30],
                      [-50, -30, -30, -30, -30, -30, -30, -50]]
knightEndgameScores = [[-50, -40, -30, -30, -30, -30, -40, -50],
                      [-40, -20,   0,   0,   0,   0, -20, -40],
                      [-30,   0,  10,  15,  15,  10,   0, -30],
                      [-30,   5,  15,  20,  20,  15,   5, -30],
                      [-30,   0,  15,  20,  20,  15,   0, -30],
                      [-30,   5,  10,  15,  15,  10,   5, -30],
                      [-40, -20,   0,   5,   5,   0, -20, -40],
                      [-50, -40, -30, -30, -30, -30, -40, -50]]
queenEndgameScores = [[-20, -10, -10,  -5,  -5, -10, -10, -20],
                      [-10,   0,   0,   0,   0,   0,   0, -10],
                      [-10,   0,   5,   5,   5,   5,   0, -10],
                      [ -5,   0,   5,   5,   5,   5,   0,  -5],
                      [  0,   0,   5,   5,   5,   5,   0,  -5],
                      [-10,   5,   5,   5,   5,   5,   0, -10],
                      [-10,   0,   5,   0,   0,   0,   0, -10],
                      [-20, -10, -10,  -5,  -5, -10, -10, -20]]
rookEndgameScores = [[0,   0,   0,   0,   0,   0,   0,   0],
                   [5,  10,  10,  10,  10,  10,  10,   5],
                   [-5,   0,   0,   0,   0,   0,   0,  -5],
                   [-5,   0,   0,   0,   0,   0,   0,  -5],
                   [-5,   0,   0,   0,   0,   0,   0,  -5],
                   [-5,   0,   0,   0,   0,   0,   0,  -5],
                   [-5,   0,   0,   0,   0,   0,   0,  -5],
                   [ 0,   0,   0,   5,   5,   0,   0,   0]]
bishopEndgameScores = [[-20, -10, -10, -10, -10, -10, -10, -20],
                      [-10,   0,   0,   0,   0,   0,   0, -10],
                      [-10,   0,   5,  10,  10,   5,   0, -10],
                      [-10,   5,   5,  10,  10,   5,   5, -10],
                      [-10,   0,  10,  10,  10,  10,   0, -10],
                      [-10,  10,  10,  10,  10,  10,  10, -10],
                      [-10,   5,   0,   0,   0,   0,   5, -10],
                      [-20, -10, -10, -10, -10, -10, -10, -20]]
pawnEndgameScores = [[0,   0,   0,   0,   0,   0,   0,   0],
                       [50,  50,  30,  20,  20,  30,  50,  50],
                       [30,  30,  20,  10,  10,  20,  30,  30],
                        [0,   0,   0,   0,   0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0],
                        [0,   0,   0,   0,   0,   0,   0,   0]]
piecePositionScores = {"N": knightScores, "Ne": knightEndgameScores,
                       "Q": queenScores,  "Qe": queenEndgameScores,
                       "B": bishopScores, "Be": bishopEndgameScores,
                       "R": rookScores,   "Re": rookEndgameScores,
                       "p": pawnScores,   "pe": pawnEndgameScores,
                       "K": kingScores,   "Ke": kingEndgameScores}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 2
count = 0
potentialScore = 0

def findRandomMove(validMoves):
    return random.choice(validMoves)

def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    bestMove = None
    minMaxScore = CHECKMATE

    random.shuffle(validMoves)
    for move in validMoves:
        gs.makeMove(move)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            score = STALEMATE
        elif gs.checkMate:
            score = -CHECKMATE
        else:
            score = -CHECKMATE
            for opponentMove in opponentsMoves:
                gs.makeMove(opponentMove)
                if gs.checkMate:
                    tempScore = CHECKMATE
                elif gs.staleMate:
                    tempScore = STALEMATE
                else:
                    tempScore = -turnMultiplier * scoreMaterial(gs.board)
                score = max(score, tempScore)
                gs.undoMove()
        gs.undoMove()

        if score < minMaxScore:
            minMaxScore = score
            bestMove = move
    return bestMove
def findBestMove(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None
    #findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBetaWithNullMove(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    #findMoveNegaMaxAlphaBetaWithNullMoveQuiescenceSearch(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1) # Null Move Heuristic
    returnQueue.put(nextMove)
    print(count)
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global count
    count += 1
    if depth == 0:
        return scoreMaterial(gs.board)

    scores = []
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = findMoveMinMax(gs, nextMoves, depth - 1, not whiteToMove)
        scores.append(score)
        gs.undoMove()

    if whiteToMove:
        maxScore = max(scores)
        if depth == DEPTH:
            global nextMove
            nextMove = validMoves[scores.index(maxScore)]
        return maxScore
    else:
        minScore = min(scores)
        if depth == DEPTH:
            nextMove = validMoves[scores.index(minScore)]
        return minScore





def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global count
    count += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()

        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                global nextMove
                nextMove = move
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
    print(count)

def findMoveNegaMaxAlphaBetaWithNullMove(gs, validMoves, depth, alpha, beta, turnMultiplier):
    #global count
    #count += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Null Move Heuristic
    if depth > 1 and not gs.checkMate and not gs.staleMate:
        gs.makeNullMove()
        score = -findMoveNegaMaxAlphaBetaWithNullMove(gs, validMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoNullMove()
        if score >= beta:
            return score

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBetaWithNullMove(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()

        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                global nextMove
                nextMove = move
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def findMoveNegaMaxAlphaBetaWithNullMoveQuiescenceSearch(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global count
    count += 1
    if depth == 0:
        return quiescenceSearch(gs, alpha, beta, turnMultiplier)

    if depth > 1 and not gs.checkMate and not gs.staleMate:
        gs.makeNullMove()
        score = -findMoveNegaMaxAlphaBetaWithNullMove(gs, validMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoNullMove()
        if score >= beta:
            return score

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBetaWithNullMoveQuiescenceSearch(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()

        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                global nextMove
                nextMove = move
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
def quiescenceSearch(gs, alpha, beta, turnMultiplier, depth=2):
    standPat = turnMultiplier * scoreBoard(gs)

    if standPat >= beta:
        return beta

    if alpha < standPat:
        alpha = standPat

    if depth <= 0:
        return alpha
    captures = gs.getAllCaptures()
    captures.sort(key=lambda move: getPieceValue(gs.board[move.endRow][move.endCol][1]), reverse=True)

    for move in captures:

        captureValue = getPieceValue(gs.board[move.endRow][move.endCol][1])
        if standPat + captureValue + 300 < alpha:
            continue

        gs.makeMove(move)
        score = -quiescenceSearch(gs, -beta, -alpha, -turnMultiplier, depth - 1)
        gs.undoMove()


        if score > alpha:
            alpha = score

        if alpha >= beta:
            break

    return alpha

def getPieceValue(piece):

    pieceScore = { "K": 10000, "Q": 900, "R": 500, "B": 330, "N": 320, "p": 100}

    return pieceScore.get(piece, 0)

def scoreBoard(gs):
    score = 0
    potentialScore = PotentialScore(gs)

    if gs.checkMate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    if gs.staleMate:
        return -CHECKMATE if PotentialScore(gs) > 0 else STALEMATE

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piece = square[1]
                pieceScoreValue = pieceScore.get(piece, 0)

                if gs.endGame or (gs.middleGame and piece != 'K'):
                    key = piece + 'e'
                else:
                    key = 'K' if piece == 'K' and gs.middleGame else piece

                piecePositionScore = piecePositionScores.get(key, [[0] * 8] * 8)[row][col]
                piecePositionScoreB = piecePositionScores.get(key, [[0] * 8] * 8)[7 - row][7 - col]

                score += (pieceScoreValue + piecePositionScore if square[0] == 'w' else -pieceScoreValue - piecePositionScoreB)

    return score + potentialScore


def PotentialScore(gs):
    return ThreatAndProtectPotential(gs) + Structure(gs)

# Bonus point for Bishop pair and penalty point for Double-Pawn
def Structure(gs):
    BonusPoint = 0
    whitePair = blackPair = 0
    centralSquares = {(3, 3), (3, 4), (4, 3), (4, 4), (5, 3), (5, 4), (2, 4), (2, 3)}
    CentralControl = {'p': 10, 'R': 0, 'N': 0, 'B': 0, 'Q': 0, 'K': 0}
    pieceMobility = {"K": 0, "Q": 0, "R": 0, "B": 0, "N": 0, "p": 0}

    allMoves = gs.getAllPossibleMoves()
    moveDict = {gs.board[move.startRow][move.startCol]: [] for move in allMoves}
    for move in allMoves:
        moveDict[gs.board[move.startRow][move.startCol]].append(move)

    for col in range(8):
        whitePawns = blackPawns = whiteRookMoves = blackRookMoves = 0
        colHasWhitePawn = colHasBlackPawn = False

        for row in range(8):
            piece = gs.board[row][col]
            if piece == '--':
                continue

            isWhite = piece[0] == 'w'
            pieceType = piece[1]

            # Bonus for pawns and knights in central squares
            if (piece == 'wp' or piece == 'wN') and (row, col) in centralSquares:
                BonusPoint += 20
                whitePawns += 1
            elif (piece == 'bp' or piece == 'bN') and (row, col) in centralSquares:
                BonusPoint -= 20
                blackPawns += 1

            # Count bishop pairs
            if piece == 'wB':
                whitePair += 1
            elif piece == 'bB':
                blackPair += 1

            # Calculate mobility and central control
            if piece in moveDict:
                numMoves = len(moveDict[piece])
                mobilityBonus = numMoves * pieceMobility.get(pieceType, 0)
                BonusPoint += mobilityBonus if isWhite else -mobilityBonus

                for move in moveDict[piece]:
                    if (move.endRow, move.endCol) in centralSquares:
                        BonusPoint += CentralControl.get(pieceType, 0) if isWhite else -CentralControl.get(pieceType, 0)

            # Count rook moves
            if piece == 'wR':
                whiteRookMoves += len(moveDict.get(piece, []))
            elif piece == 'bR':
                blackRookMoves += len(moveDict.get(piece, []))

            # Passed pawns flagging
            if piece == 'wp':
                colHasWhitePawn = True
            elif piece == 'bp':
                colHasBlackPawn = True

        # Bonuses for rook mobility
        if whiteRookMoves > 3:
            BonusPoint += 5 if whiteRookMoves <= 7 else 20
        if blackRookMoves > 3:
            BonusPoint -= 5 if blackRookMoves <= 7 else 20

        # Penalty for multiple pawns in the same column
        if whitePawns > 1:
            BonusPoint -= 10
        if blackPawns > 1:
            BonusPoint += 10

        # Passed pawn check for white pawns
        if colHasWhitePawn and not any(gs.board[r][col] == 'bp' for r in range(8)):
            if (col == 0 or not any(gs.board[r][col - 1] == 'bp' for r in range(8))) and \
               (col == 7 or not any(gs.board[r][col + 1] == 'bp' for r in range(8))):
                BonusPoint += 15  # Passed white pawn bonus

        # Passed pawn check for black pawns
        if colHasBlackPawn and not any(gs.board[r][col] == 'wp' for r in range(8)):
            if (col == 0 or not any(gs.board[r][col - 1] == 'wp' for r in range(8))) and \
               (col == 7 or not any(gs.board[r][col + 1] == 'wp' for r in range(8))):
                BonusPoint -= 15  # Passed black pawn penalty

    # Bonus for bishop pairs
    if whitePair > 1:
        BonusPoint += 50
    if blackPair > 1:
        BonusPoint -= 50

    return BonusPoint





def ThreatAndProtectPotential(gs):
    BonusPoints = 0
    allMoves = gs.getAllPossibleMoves()

    for move in allMoves:
        endRow, endCol = move.endRow, move.endCol
        targetSquare = gs.board[endRow][endCol]

        if targetSquare != "--":
            pieceType = targetSquare[1]
            threatValue = pieceThreaten.get(pieceType, 0)
            protectValue = pieceProtect.get(pieceType, 0)

            if gs.whiteToMove:
                if targetSquare[0] == 'b':
                    BonusPoints += threatValue
                elif targetSquare[0] == 'w':
                    BonusPoints += protectValue
            else:
                if targetSquare[0] == 'w':
                    BonusPoints -= threatValue
                elif targetSquare[0] == 'b':
                    BonusPoints -= protectValue

    return BonusPoints
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore.get(square[1], 0)
            elif square[0] == 'b':
                score -= pieceScore.get(square[1], 0)
    return score
