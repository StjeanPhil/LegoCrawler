import sqlite3
import json

def insert_watchlist_from_json():
    # Read JSON data
    with open('./data/watchlist.json') as json_file:
        data = json.load(json_file)

    # Connect to the database
    conn = sqlite3.connect('LegoLogs.db')
    cursor = conn.cursor()
    i=0
    # Insert shops
    for item in data:
        watchlist_id = i
        
        set_num = item["name"]
        target_price = float(item["price"])/100
        i+=1

        cursor.execute('''INSERT INTO watchlist (watchlist_id, set_num, target_price) VALUES (?, ?, ?)''', (watchlist_id,set_num,target_price))

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_watchlist_from_json()
    print("Shops inserted successfully.")