import psycopg2

DB_CONFIG = {
    "dbname": "snake_game",
    "user": "postgres",
    "password": "4567",
    "host": "localhost",
    "port": 5432
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def get_or_create_player(username):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    row = cur.fetchone()

    if row:
        player_id = row[0]
    else:
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return player_id


def save_game(player_id, score, level):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()
    cur.close()
    conn.close()


def get_top10():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def get_best(player_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(score) FROM game_sessions
        WHERE player_id=%s
    """, (player_id,))

    best = cur.fetchone()[0]
    cur.close()
    conn.close()

    return best or 0