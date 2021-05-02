"""functions for playing games"""

import chess
import chess.engine
import chess.svg
import chess.pgn
import chess.polyglot
import lib.postgres as psql
import io
import os

### this function is broken, used to work, not sure what is wrong
def playGame( whiteName,blackName,timePerMove,line ):
    os.chdir('/src/notebooks')
    if whiteName == 'leela':
        white = chess.engine.SimpleEngine.popen_uci("/lczero/lc0")
        black = chess.engine.SimpleEngine.popen_uci("/root/Stockfish/src/stockfish")
    else:
        black = chess.engine.SimpleEngine.popen_uci("/lczero/lc0")
        white = chess.engine.SimpleEngine.popen_uci("/root/Stockfish/src/stockfish")
    board = chess.Board()
    openingGame = chess.pgn.read_game(io.StringIO(line))
    game = chess.pgn.Game()

    for move in openingGame.mainline_moves():
        if ((board.fullmove_number == 1) & board.turn):
            node = game.add_variation(chess.Move.from_uci(str(move)))
        else:
            node = node.add_variation(chess.Move.from_uci(str(move)))
        board.push(chess.Move.from_uci(str(move)))
        
    while not board.is_game_over(claim_draw=True):
        if board.turn:
            result = white.play(board, chess.engine.Limit(time=timePerMove))
        else:
            result = black.play(board, chess.engine.Limit(time=timePerMove))

        node = node.add_variation(result.move)
        board.push(result.move)

    game.headers["Result"] = board.result()
    game.headers["White"] = whiteName
    game.headers["Black"] = blackName
    psql.insert_game(game,timePerMove)
    
    

def playMatch(player_white,player_black,games,dep):
    score = 0
    whiteBookMoves = 0
    blackBookMoves = 0
    stockfish = chess.engine.SimpleEngine.popen_uci("/root/Stockfish/src/stockfish")
    with chess.polyglot.open_reader("/src/notebooks/data/books/w" + player_white + ".bin") as whiteBook:
        with chess.polyglot.open_reader("/src/notebooks/data/books/b" + player_black + ".bin") as blackBook:
            for i in range(games):
                board = chess.Board()
                while not board.is_game_over(claim_draw=True):
                    if board.turn:
                        try:
                            entry = whiteBook.weighted_choice(board) # or reader.find(board)
                            move = entry.move
                            board.push(move)
                            whiteBookMoves += 1
                        except:
                            entry = stockfish.play(board, chess.engine.Limit(depth=dep))
                            move = entry.move
                            board.push(move)
                    else:
                        try:
                            entry = blackBook.weighted_choice(board) # or reader.find(board)
                            move = entry.move
                            board.push(move)
                            blackBookMoves += 1
                        except:
                            entry = stockfish.play(board, chess.engine.Limit(depth=dep))
                            move = entry.move
                            board.push(move)
                if "0-1" in board.result():
                    score -= 1
                elif "1-0" in board.result():
                    score += 1
                elif "1/2-1/2" in board.result():
                    score += 0
                else:
                    score += 0
    psql.insert_match(player_white,player_black,games,dep,score,whiteBookMoves,blackBookMoves)
    
    
    
    
    
                    