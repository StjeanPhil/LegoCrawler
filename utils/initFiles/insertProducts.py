#insert produyct from csv to db
import sqlite3
import csv

def insert_products_from_csv():
    # Connect to the database
    conn = sqlite3.connect('LegoLogs.db')
    cursor = conn.cursor()

    # Read CSV data
    with open('goodSets.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        i=0
        # Insert products
        
        for row in csv_reader:
            
            set_num = row[0]
            name = row[1]
            year = int(row[2])
            theme_id = int(row[3])
            num_parts = int(row[4])
            img_url = row[5]
            print(i)
            i+=1
            cursor.execute('''INSERT INTO products (set_num, name, year, theme_id, num_parts, img_url) VALUES (?, ?, ?, ?, ?, ?)''', (set_num, name, year, theme_id, num_parts, img_url))

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_products_from_csv()
    print("Products inserted successfully.")