import sqlite3
import json


def update_inventory(parsed_data):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        product_name TEXT PRIMARY KEY,
        quantity INTEGER,
        price REAL
    )
    """)

    for item in parsed_data["Items"]:
        cursor.execute("SELECT quantity FROM inventory WHERE product_name = ?", (item["name"],))
        result = cursor.fetchone()

        if result:
            new_quantity = result[0] + item["quantity"]
            cursor.execute("UPDATE inventory SET quantity = ? WHERE product_name = ?", (new_quantity, item["name"]))
        else:
            cursor.execute("INSERT INTO inventory (product_name, quantity, price) VALUES (?, ?, ?)",
                           (item["name"], item["quantity"], item["price"]))

    conn.commit()
    conn.close()
    print("Inventory updated successfully!")


conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM inventory")
print(cursor.fetchall())
