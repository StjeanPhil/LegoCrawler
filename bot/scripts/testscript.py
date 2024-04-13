import sqlite3

def test():
    conn = sqlite3.connect('LegoLogs.db')
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #check if set_num already exists
    #print(cursor.execute('''select * FROM watchlist ''').fetchmany(5))
    item={}
    item['shop_id']=3
    #print(cursor.execute('''SELECT name FROM shops WHERE shop_id=(?)''',str(item['shop_id'])).fetchone()[0])
    #delete all rows of watchlist
    #data=cursor.execute('''Select * FROM watchlist''')
    #print(data.fetchall())
    cursor.execute('''DELETE FROM watchlist''')
    
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    test()