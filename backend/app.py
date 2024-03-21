from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)  

board = ['n', 'n' , 'n', 'n', 'n', 'n', 'n', 'n', 'n']
# Gracze
# x to pierwszy gracz
players = {'player1': None, 'player2': None}
current_player = None
winner = None
lock = True
gameRunning = False


@app.route('/register', methods=['POST'])
def register():
    global players
    global current_player
    global gameRunning, lock

    if players['player1'] == request.json.get('nick') or players['player2'] == request.json.get('nick'):
        return jsonify({'status': 'taken'})
    if not players['player1']:
        players['player1'] = request.json.get('nick')
        gameRunning = True
        return jsonify({'status': 'registered'})  
    elif not players['player2']:
        players['player2'] = request.json.get('nick')
        current_player = players['player1']
        lock = False
        return jsonify({'status': 'registered'})  
    else:
        return jsonify({'status': 'full'})  

@app.route('/get_players', methods=['GET'])
def get_players():
    return jsonify({'players': players})

@app.route('/send_move', methods=['POST'])
def send_move():
    global board, current_player, players, lock, gameRunning
    move = request.json.get('move')
    player = request.json.get('yourNick')
    
    if player == current_player and board[move] == 'n' and not lock:
        if player == players['player1']:
            board[move] = 'x'
            current_player = players['player2']
            checkWin()
            return jsonify({'status': 'success'})  
        elif player == players['player2']:
            board[move] = 'o'
            current_player = players['player1']
            checkWin()
            return jsonify({'status': 'success'})  
    else:
        return jsonify({'status': 'error', 'message': 'Invalid move'}) 
    
@app.route('/get_end', methods=['GET'])
def get_end():
    return jsonify({'gameRunning': gameRunning})

@app.route('/end_game', methods=['POST'])
def end_game():
    endRunningGame()
    return jsonify({'status': 'registered'})  

def endRunningGame():
    global board, current_player, players, lock, gameRunning, winner
    board = ['n', 'n' , 'n', 'n', 'n', 'n', 'n', 'n', 'n']
    players = {'player1': None, 'player2': None}
    current_player = None
    winner = None
    lock = True
    gameRunning = False



@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify({'board': board})

@app.route('/get_winner', methods=['GET'])
def get_winner():
    winnerNick = None
    if winner == None:
        return jsonify({'winner': 'None'})
    if winner == 'x':
        winnerNick = players['player1']
    elif winner =='o':
        winnerNick = players['player2']
    elif winner =='pat':
        winnerNick = 'pat'
    return jsonify({'winner': winnerNick})

def checkWin():
    global winner, lock
    # poziomo
    if board[0] == board[1] == board[2] and board[2] != "n":
        winner = board[0]
        lock = True
    elif board[3] == board[4] == board[5] and board[5] != "n":
        winner = board[3]
        lock = True
    elif board[6] == board[7] == board[8] and board[8] != "n":
        winner = board[6]
        lock = True

    # pionowo
    elif board[0] == board[3] == board[6] and board[6] != "n":
        winner = board[0]
        lock = True
    elif board[1] == board[4] == board[7] and board[7] != "n":
        winner = board[1]
        lock = True
    elif board[2] == board[5] == board[8] and board[8] != "n":
        winner = board[2]
        lock = True

    # skosy
    elif board[0] == board[4] == board[8] and board[8] != "n":
        winner = board[0]
        lock = True
    elif board[2] == board[4] == board[6] and board[6] != "n":
        winner = board[2]
        lock = True
    elif "n" not in board:
        winner = 'pat'
        lock = True


if __name__ == '__main__':
    app.run(debug=True)