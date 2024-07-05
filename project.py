import tkinter as tk
import mysql.connector

class StockManagementSystemGUI:
    def _init_(self, root):
        self.root = root
        self.root.title("Stock Management System")

        # Create labels and entry fields
        self.name_label = tk.Label(root, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        self.quantity_label = tk.Label(root, text="Quantity:")
        self.quantity_label.grid(row=1, column=0)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=1, column=1)

        self.price_label = tk.Label(root, text="Price:")
        self.price_label.grid(row=2, column=0)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row=2, column=1)

        # Create buttons
        self.add_button = tk.Button(root, text="Add", command=self.add_product)
        self.add_button.grid(row=3, column=0)

        self.delete_button = tk.Button(root, text="Delete", command=self.delete_product)
        self.delete_button.grid(row=3, column=1)

        self.update_button = tk.Button(root, text="Update", command=self.update_product)
        self.update_button.grid(row=3, column=2)

        self.search_button = tk.Button(root, text="Search", command=self.search_product)
        self.search_button.grid(row=3, column=3)

        # Create output text area
        self.output_text = tk.Text(root, height=10, width=40)
        self.output_text.grid(row=4, columnspan=4)

        # Connect to MySQL database
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="yourusername",
                password="yourpassword",
                database="stock_inventory"
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def add_product(self):
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())

        sql = "INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)"
        values = (name, quantity, price)
        try:
            self.cursor.execute(sql, values)
            self.db.commit()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Product added successfully.")
        except mysql.connector.Error as err:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {err}")

    def delete_product(self):
        name = self.name_entry.get()

        sql = "DELETE FROM products WHERE name = %s"
        values = (name,)
        try:
            self.cursor.execute(sql, values)
            self.db.commit()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Product deleted successfully.")
        except mysql.connector.Error as err:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {err}")

    def update_product(self):
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())

        sql = "UPDATE products SET quantity = %s, price = %s WHERE name = %s"
        values = (quantity, price, name)
        try:
            self.cursor.execute(sql, values)
            self.db.commit()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Product updated successfully.")
        except mysql.connector.Error as err:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {err}")

    def search_product(self):
        name = self.name_entry.get()

        sql = "SELECT * FROM products WHERE name = %s"
        values = (name,)
        self.cursor.execute(sql, values)
        result = self.cursor.fetchall()

        if result:
            output = f"Name: {result[0][0]}\nQuantity: {result[0][1]}\nPrice: {result[0][2]}"
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output)
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Product not found.")

if _name_ == "_main_":
    # Create the root window
    root = tk.Tk()

    # Initialize the GUI application
    app = StockManagementSystemGUI(root)

    # Start the GUI event loop
    root.mainloop()
