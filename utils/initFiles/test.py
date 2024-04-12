#delete all watchlist items

import sqlite3

def delete_all_watchlist():
    conn = sqlite3.connect('LegoLogs.db')
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM watchlist''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    delete_all_watchlist()