import sqlite3

def test():
    conn = sqlite3.connect('LegoLogs.db')
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #check if set_num already exists
    print(cursor.execute('''select * FROM watchlist ''').fetchmany(5))
    

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    test()