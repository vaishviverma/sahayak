import sqlite3

# Connect to SQLite database (this will create the database file if it doesn't exist)
connection = sqlite3.connect('database.db')

# Create a cursor object to execute SQL queries
cursor = connection.cursor()


# Create the Suppliers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_name TEXT,
        contact_email TEXT,
        contact_phone TEXT,
        address TEXT
    )
''')

# Create the Products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        supplier_id INTEGER,
        unit_price REAL NOT NULL,
        retail_price REAL NOT NULL,
        unit TEXT NOT NULL,
        expiration_date DATE,
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
    )
''')

# Create the InventoryTransactions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS InventoryTransactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        transaction_type TEXT NOT NULL CHECK(transaction_type IN ('purchase', 'sale', 'return')),
        quantity INTEGER NOT NULL,
        transaction_date TEXT NOT NULL,
        cost_price REAL,
        sale_price REAL,
        supplier_id INTEGER,
        FOREIGN KEY (product_id) REFERENCES Products(product_id),
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
    )
''')

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Tables created successfully!")





def insert_supplier(name, contact_name, contact_email, contact_phone, address):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Suppliers (name, contact_name, contact_email, contact_phone, address)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, contact_name, contact_email, contact_phone, address))
    connection.commit()
    connection.close()


def insert_product(name, description, supplier_id, unit_price, retail_price, unit, expiration_date=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Products (name, description, supplier_id, unit_price, retail_price, unit, expiration_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ( name, description, supplier_id, unit_price, retail_price, unit, expiration_date))
    connection.commit()
    connection.close()


def insert_inventory_transaction(product_id, transaction_type, quantity, transaction_date, cost_price=None, sale_price=None, supplier_id=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO InventoryTransactions (product_id, transaction_type, quantity, transaction_date, cost_price, sale_price, supplier_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (product_id, transaction_type, quantity, transaction_date, cost_price, sale_price, supplier_id))
    connection.commit()
    connection.close()

def update_product_stock(name, new_stock_quantity):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT unit FROM Products WHERE name = ?', (name,))
    result = cursor.fetchone()

    if result:

        old_stock_quantity = result[0]
        stock_quantity = int(old_stock_quantity) + int(new_stock_quantity)

        # Update the product's stock quantity by adding the new stock
        cursor.execute('''UPDATE Products SET unit = ? WHERE name = ?''',
                       (stock_quantity, name))
        print(f"Stock updated successfully! New stock for product {name}: {stock_quantity}")
    else:
        print(f"Product {name} not found!")

    # Commit the changes and close the connection
    connection.commit()
    connection.close()
