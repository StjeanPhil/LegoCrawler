import sqlite3
import json

def insert_shops_from_json():
    # Read JSON data
    with open('./data/stores.json') as json_file:
        shops_data = json.load(json_file)

    # Connect to the database
    conn = sqlite3.connect('LegoLogs.db')
    cursor = conn.cursor()

    # Insert shops
    for shop in shops_data:
        shop_id = shop["shop_id"]
        shop_name = shop["shop_name"]
        website = shop["website"]
        notes = shop["notes"]

        cursor.execute('''INSERT INTO shops (shop_id, name, website, notes) VALUES (?, ?, ?, ?)''', (shop_id, shop_name, website, notes))

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_shops_from_json()
    print("Shops inserted successfully.")