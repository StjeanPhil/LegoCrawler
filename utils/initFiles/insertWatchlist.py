import sqlite3
import json
from decimal import Decimal

def insert_shops_from_json():
    with open('./data/watchlist.json') as json_file:
        data = json.load(json_file)

    conn = sqlite3.connect('LegoLogs.db')
    cursor = conn.cursor()
    #delete the current table
    cursor.execute('''DELETE from watchlist''')
    i=0
    for item in data:
        watchlist_id = 1
        set_num = item["set_num"]
        target_price = Decimal(item["target_price"])/100

        cursor.execute('''INSERT INTO watchlist (watchlist_id, set_num, target_price) VALUES (?, ?, ?)''', (watchlist_id, set_num, target_price))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_shops_from_json()