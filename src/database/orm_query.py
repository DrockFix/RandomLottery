def get_all_winners(user_id: str):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM winners WHERE user_id = ?', (user_id,))
    winners_rows = cursor.fetchall()
    winners = []
    for row in winners_rows:
        winners_dict = dict(id=row[0], winner=row[2], winner_url=row[3], post=row[4], likes=row[5], create_at=row[6])
        winners.append(winners_dict)
    conn.commit()
    conn.close()
    return winners


def db_user_add(user_id: str):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users(user_id) VALUES(?)', (user_id,))
    conn.commit()
    conn.close()


def db_winner_add(user_id: int, winner: str, winner_url: str, post: str, likes: int):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO winners(user_id, winner, winner_url, post, likes) VALUES(?,?,?,?,?)',
                   (user_id, winner, winner_url, post, likes))
    conn.commit()
    conn.close()