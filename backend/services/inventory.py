import sqlite3
import json
from database_manipulate import insert_product, update_product_stock

def update_inventory(parsed_data):

    for item in parsed_data["Items"]:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT unit FROM Products WHERE name = ?", (item["name"],))
        result = cursor.fetchone()

        if result:
            update_product_stock(item["name"], item["quantity"])
        else:
            insert_product(item["name"],"", "",item["price"],item["price"]+20,item["quantity"])
           
    conn.commit()
    conn.close()
    print("Inventory updated successfully!")


conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM Products")
print(cursor.fetchall())
