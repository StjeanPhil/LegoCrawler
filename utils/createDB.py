import sqlite3

def create_LegoLogsDB():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('LegoLogs.db')
    cursor = conn.cursor()

    # Create shops table
    cursor.execute('''CREATE TABLE IF NOT EXISTS shops (
                        shop_id INTEGER PRIMARY KEY,
                        name TEXT,
                        website TEXT,
                        notes TEXT
                    )''')

    # Create products table COULD BE EXPANDED TO INCLUDE MORE PRODUCT INFO
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        set_num TEXT PRIMARY KEY,
                        name TEXT,
                        year INTEGER,
                        theme_id INTEGER,
                        num_parts INTEGER,
                        img_url TEXT
                    )''')

    # Create watchlist table
    cursor.execute('''CREATE TABLE IF NOT EXISTS watchlist (
                        watchlist_id INTEGER PRIMARY KEY,
                        set_num INTEGER,
                        target_price REAL,
                        FOREIGN KEY (set_num) REFERENCES products(set_num)
                    )''')

    # Create hitlist table
    cursor.execute('''CREATE TABLE IF NOT EXISTS hitlist (
                        hit_id INTEGER PRIMARY KEY,
                        watchlist_id INTEGER,
                        log_id INTEGER,
                        FOREIGN KEY (watchlist_id) REFERENCES watchlist(watchlist_id),
                        FOREIGN KEY (log_id) REFERENCES logs(log_id)
                    )''')

    # Create logs table 
    # INSTOCK,PICKUP AND SHIPS ARE BOOLEAN VALUES
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        log_id INTEGER PRIMARY KEY,
                        datetime TEXT,
                        shop_id INTEGER,
                        set_num INTEGER,
                        price REAL,
                        inStock INTEGER,
                        pickup INTEGER,
                        ships INTEGER,
                        link TEXT,
                        FOREIGN KEY (shop_id) REFERENCES shops(shop_id),
                        FOREIGN KEY (set_num) REFERENCES products(set_num)
                    )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("LegoLogs Database created successfully.")

if __name__ == "__main__":
    create_LegoLogsDB() 


