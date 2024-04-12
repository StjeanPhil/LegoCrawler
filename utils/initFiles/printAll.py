import sqlite3

def print_all_shops():
    conn = sqlite3.connect('LegoLogs.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM shops''')
    shops = cursor.fetchall()

    for shop in shops:
        print(shop)
    
    #print all products
    cursor.execute('''SELECT * FROM products''')
    products = cursor.fetchmany(5)
    for product in products:
        print(product)

        #print all products
    cursor.execute('''SELECT * FROM watchlist''')
    products = cursor.fetchmany(5)
    for product in products:
        print(product)

    conn.close()

if __name__ == "__main__":
    print_all_shops()
