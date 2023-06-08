from datetime import datetime
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
                                name text PRIMARY KEY 
                            ); """

sql_create_game_table = """CREATE TABLE IF NOT EXISTS games (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                score integer,
                                player_id text NOT NULL,
                                timer integer NOT NULL,
                                create_date timestamp NOT NULL,
                                FOREIGN KEY (player_id) REFERENCES players (name)
                            );"""

sql_create_game_player_table = """ CREATE TABLE IF NOT EXISTS games_players (
                                    player_id text NOT NULL,
                                    game_id integer NOT NULL,
                                    correctWord text NOT NULL,
                                    FOREIGN KEY (player_id) REFERENCES players (name),
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

    # Open a connection to the database
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Query the database to see if the player already exists
        cur.execute("SELECT * FROM players WHERE name=?", (username,))
        player = cur.fetchone()

        # If the player does not exist, add them to the database
        if player is None:
            cur.execute("INSERT INTO players (name) VALUES (?)", (username,))
            conn.commit()

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("INSERT INTO games (score, player_id, timer, create_date) VALUES (?, ?, ?, ?)",
                    (0, username, timer, current_datetime))
        conn.commit()
        cur.execute("SELECT last_insert_rowid()")
        game_id = cur.fetchone()[0]

        gamecontroller.new_game(size, timer, username, game_id)
        return redirect("/game")

    finally:
        conn.close()


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
    game = gamecontroller.game
     
    if result == True:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE games SET score = ? WHERE id = ?", (game.score, game.id))
            cur.execute("INSERT INTO games_players (player_id, game_id, correctWord) VALUES (?, ?, ?)",
                        (game.player.name, game.id, word))
            message = "Valid word!"
            conn.commit()

        finally:
            cur.close()
            conn.close()
    else:
        message = "Invalid word!"

    remaining_time = gamecontroller.get_remaining_time()
    return render_template("game.html", game=game, remaining_time=remaining_time, message=message)


#end of the game
@app.route("/end_game")
def end_game():

    try:
        score = gamecontroller.end_game()
        return render_template("end_game.html", score=score)

    finally:
        conn.close()


#add statistics to the game
def fetch_stats(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name AS player_name, g.id AS game_id, g.score, g.timer, g.create_date, gp.correctWord
        FROM games_players gp
        JOIN games g ON gp.game_id = g.id
        JOIN players p ON gp.player_id = p.name
    """)
    results = cur.fetchall()
    cur.close()
    print(results);
    return results


@app.route('/statistics')
def statistics():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.name AS player_name, g.id AS game_id, g.score, g.timer, g.create_date, gp.correctWord
            FROM games g
            JOIN players p ON g.player_id = p.name
            LEFT JOIN games_players gp ON gp.game_id = g.id
        """)
        results = cur.fetchall()
        cur.close()
        print(results)
        return render_template('stats.html', stats=results)

    finally:
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)