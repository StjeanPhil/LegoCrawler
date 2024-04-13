import sqlite3

def print_all_shops():
    conn = sqlite3.connect('LegoLogs.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM shops''')
    shops = cursor.fetchall()
    print("Shops: ")
    for shop in shops:
        print(shop)
    
    #print all products
    cursor.execute('''SELECT * FROM products''')
    products = cursor.fetchmany(5)
    print("Products: ")
    for product in products:
        print(product)

        #print all products
    cursor.execute('''SELECT * FROM watchlist''')
    products = cursor.fetchall()
    print("Watchlist: ")
    for product in products:
        print(product)
    cursor.execute('''SELECT * FROM logs''')
    products = cursor.fetchmany(5)
    print("Logs: ")
    for product in products:
        print(product)

    conn.close()

if __name__ == "__main__":
    print_all_shops()
