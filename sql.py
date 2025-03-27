import sqlite3
import bcrypt

# create connection
connection = sqlite3.connect("rhythmrolls.db")

# create cursor to execute methods
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# create tables
cursor.execute("""
               CREATE TABLE IF NOT EXISTS accounts(
               username TEXT PRIMARY KEY,
               password TEXT NOT NULL
               );
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS levels(
               level INTEGER PRIMARY KEY,
               difficulty TEXT NOT NULL,
               track TEXT NOT NULL,
               height INTEGER NOT NULL
               );
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS leaderboard(
               username TEXT NOT NULL,
               level INTEGER NOT NULL,
               score INTEGER NOT NULL,
               PRIMARY KEY (username, level),
               FOREIGN KEY (username) REFERENCES accounts (username) ON DELETE CASCADE,
               FOREIGN KEY (level) REFERENCES levels (level) ON DELETE CASCADE
               );
               """)


# add level

def add_level(connection, level, difficulty, track, height):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM levels WHERE level = ?", (level,))
    check = cursor.fetchone()

    if check == None:
        cursor.execute("INSERT INTO levels (level, difficulty, track, height) VALUES (?, ?, ?, ?)", (level, difficulty, track, height))
        connection.commit()
        return True
    
    else:
        return False
    
# add levels
add_level(connection, 1, 'easy', 'music/moonlit.mp3', 200)
add_level(connection, 2, 'easy', 'music/heartoftheocean.mp3', 125)
add_level(connection, 3, 'hard', 'music/moonlit.mp3', 200)
add_level(connection, 4, 'easy', 'music/moonlit.mp3', 200)

# alter level records

def change_level(connection, level, difficulty, track, height):
    cursor = connection.cursor()

    cursor.execute("UPDATE levels SET difficulty = ?, track = ?, height = ? WHERE level = ?", (difficulty, track, height, level))
    connection.commit()

change_level(connection, 4, 'hard', 'music/enchantingforest.mp3', 200)

# get level info

def get_level(connection, level):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM levels WHERE level = ?", (level,))
    info = cursor.fetchone()

    return info

# create account

def check_user(connection, user):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM accounts WHERE username = ?", (user,))
    check = cursor.fetchone()

    if check == None:
        return True
    
    else:
        return False


def create_account(connection, user, password):
    cursor = connection.cursor()

    cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (user, password))
    connection.commit()

# add score

def add_score(connection, user, level, score):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM leaderboard WHERE level = ? AND username = ?", (level, user))
    check = cursor.fetchone()

    if not check:
        cursor.execute("INSERT INTO leaderboard (username, level, score) VALUES (?, ?, ?)", (user, level, score))
    else:
        cursor.execute("UPDATE leaderboard SET score = ? WHERE level = ? AND username = ?", (score, level, user))

    connection.commit() 

# check password

def check_password(connection, user, pass_input):
    cursor = connection.cursor()
    pass_input = pass_input.encode()

    cursor.execute("SELECT password FROM accounts WHERE username = ?", (user,))
    hash = cursor.fetchone()

    return bcrypt.checkpw(pass_input, hash[0])

# get top values

def top_five(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 5")

    top_scores = cursor.fetchall()

    return top_scores

def top_five_from_level(connection, level):
    cursor = connection.cursor()

    cursor.execute("SELECT username, score FROM leaderboard WHERE level = ? ORDER BY score DESC LIMIT 5", (level,))

    top_scores = cursor.fetchall()

    return top_scores

def top_five_from_user(connection, user):
    cursor = connection.cursor()

    cursor.execute("SELECT username, score FROM leaderboard WHERE username = ? ORDER BY score DESC LIMIT 5", (user,))

    top_scores = cursor.fetchall()

    return top_scores

# get track info

def track_info(connection, level):
    cursor = connection.cursor()

    cursor.execute("SELECT difficulty, track, bpm FROM leaderboard WHERE level = ? ORDER BY score DESC LIMIT 5", (level,))


# add accounts and scores

# create_account(connection, 'user1', '.1234567')
# create_account(connection, 'user2', '.1234567')
# create_account(connection, 'user3', '.1234567')
# create_account(connection, 'user4', '.1234567')
# create_account(connection, 'user5', '.1234567')
# create_account(connection, 'user6', '.1234567')

# add_score(connection, 'user1', 1, 9000) #1
# add_score(connection, 'user2', 1, 43653) #2
# add_score(connection, 'user3', 1, 91298) #3
# add_score(connection, 'user2', 2, 13783) #4
# add_score(connection, 'user3', 2, 23493) #5
# add_score(connection, 'user4', 2, 100000) #6
# add_score(connection, 'user3', 3, 62343) #7
# add_score(connection, 'user4', 3, 23978) #8
# add_score(connection, 'user5', 3, 0) #9
# add_score(connection, 'user4', 4, 87897) #10
# add_score(connection, 'user5', 4, 76125) #11
# add_score(connection, 'user6', 4, 31289) #12