from flask import Flask, render_template, redirect, url_for
from game_state import Game

app = Flask(__name__)
app.secret_key = 'secret'

player_names = ['Alice', 'Bob', 'Charlie', 'Diana']
game = Game(player_names)

@app.route('/')
def board():
    winner = game.check_winner()
    if winner:
        return f"<h1>{winner} wins the game!</h1><a href='/reset'>Play again?</a>"

    return render_template('board.html', game=game)

@app.route('/roll')
def roll():
    player = game.current_player()
    roll_value = game.roll_dice()
    game.move_player(player, roll_value)

    # Option to climb if at corner
    if player.position % 8 == 0 and player.has_completed_one_lap and not player.on_mountain:
        game.climb_mountain(player)

    game.apply_king_tax()
    game.handle_duels()
    game.check_eliminations()
    game.next_turn()

    return redirect(url_for('board'))

@app.route('/reset')
def reset():
    global game
    game = Game(player_names)
    return redirect(url_for('board'))

if __name__ == '__main__':
    app.run(debug=True)