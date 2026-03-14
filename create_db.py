import sqlite3
import pandas as pd

def setup_database():
    # 1. Connect to SQLite (this automatically creates the file if it doesn't exist)
    conn = sqlite3.connect('groceries.db')
    cursor = conn.cursor()

    # 2. Create the table schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            supermarket TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT
        )
    ''')

    # 3. Create our mock data (Realistic UK items and prices)
    mock_data = [
        # Aldi Prices (Generally cheapest)
        ('Semi-Skimmed Milk 2 Pints', 'Aldi', 1.20, 'Dairy'),
        ('Wholemeal Bread 800g', 'Aldi', 0.75, 'Bakery'),
        ('Free Range Eggs 6 pack', 'Aldi', 1.55, 'Dairy'),
        ('Chicken Breast Fillets 500g', 'Aldi', 3.49, 'Meat'),
        
        # Tesco Prices (Mid-range)
        ('Semi-Skimmed Milk 2 Pints', 'Tesco', 1.30, 'Dairy'),
        ('Wholemeal Bread 800g', 'Tesco', 0.85, 'Bakery'),
        ('Free Range Eggs 6 pack', 'Tesco', 1.80, 'Dairy'),
        ('Chicken Breast Fillets 500g', 'Tesco', 3.75, 'Meat'),

        # Sainsbury's Prices (Slightly higher)
        ('Semi-Skimmed Milk 2 Pints', 'Sainsburys', 1.35, 'Dairy'),
        ('Wholemeal Bread 800g', 'Sainsburys', 0.90, 'Bakery'),
        ('Free Range Eggs 6 pack', 'Sainsburys', 1.95, 'Dairy'),
        ('Chicken Breast Fillets 500g', 'Sainsburys', 4.00, 'Meat')
    ]

    # 4. Clear existing data to prevent duplicates if you run this script twice
    cursor.execute('DELETE FROM products')

    # 5. Insert the data into the database
    cursor.executemany('''
        INSERT INTO products (item_name, supermarket, price, category)
        VALUES (?, ?, ?, ?)
    ''', mock_data)

    # Commit changes and close the connection
    conn.commit()
    
    # 6. Verify it worked by printing the results using pandas
    print("Database created successfully! Here is a sample of the data:")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    print(df.head(12).to_string(index=False))
    
    conn.close()

if __name__ == '__main__':
    setup_database()