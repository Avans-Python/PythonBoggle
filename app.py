import sqlite3
from sqlite3 import Error
from controllers.Gamecontroller import GameController



from flask import Flask, redirect, render_template, request

app = Flask(__name__)
gamecontroller = GameController()

def get_db_connection():
      return create_connection(r"database.db")


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

    
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


database = r"database.db"

sql_create_player_table = """ CREATE TABLE IF NOT EXISTS players (
                                id integer PRIMARY KEY,
                                name text NOT NULL
                            ); """

sql_create_game_table = """CREATE TABLE IF NOT EXISTS games (
                                id integer PRIMARY KEY,
                                score integer,
                                player_id integer NOT NULL,
                                timer integer NOT NULL,
                                create_date timestamp NOT NULL,
                                FOREIGN KEY (player_id) REFERENCES players (id)
                            );"""

sql_create_game_player_table = """ CREATE TABLE IF NOT EXISTS games_players (
                                    player_id integer NOT NULL,
                                    game_id integer NOT NULL,
                                    correctWord text NOT NULL,
                                    FOREIGN KEY (player_id) REFERENCES players (id),
                                    FOREIGN KEY (game_id) REFERENCES games (id)
                                ); """

# create a database connection
conn = create_connection(database)

# create tables
if conn is not None:
    # create player table
    create_table(conn, sql_create_player_table)

    # create game table
    create_table(conn, sql_create_game_table)

    # create game_player table
    create_table(conn, sql_create_game_player_table)
else:
    print("Error! cannot create the database connection.")


@app.route("/")
def index():
    return render_template("index.html")

#start the game
@app.route('/start_game', methods=['POST'])
def start_game():
    username = request.form['username']
    size = request.form['size']
    timer = True if request.form.get('timer') == "on" else False
    gamecontroller.new_game(size, timer, username) 
    return redirect("/game")


@app.route('/game')
def show_game():
    game = gamecontroller.game
    if game:
        remaining_time = gamecontroller.get_remaining_time()
        return render_template("game.html",game=game , remaining_time=remaining_time)
    else:
        return redirect("/")
    
@app.route("/check_word", methods=["POST"])
def check_word():
    word = request.form.get("word")
    result = gamecontroller.check_word(word)

    if result == "valid":
        message = "Valid word!"
    else:
        message = "Invalid word!"

    game = gamecontroller.game
    remaining_time = gamecontroller.get_remaining_time()

    return render_template("game.html", game=game, remaining_time=remaining_time, message=message)

@app.route("/end_game")
def end_game():
    score = gamecontroller.end_game()
    return render_template("end_game.html", score=score)

if __name__ == "__main__":
    app.run(debug=True)