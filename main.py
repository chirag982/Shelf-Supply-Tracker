import customtkinter
import tkinter
import sqlite3
import tkinter
from CTkScrollableDropdown import CTkScrollableDropdown

class Database:
    def __init__(self, db_name="shop_manager.db"):
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.create_tables()
    
    def create_tables(self):
        # Items Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)

        # Suppliers Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL
            )
        """)        

        self.conn.commit()



class Shop(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.db = Database()
        self.cart_list = []
        self.title("Shop Manager")
        self.geometry("950x600")
        self.minsize(900, 550)

        self.grid_columnconfigure(0, weight=5) # Sidebar column stays fixed
        self.grid_columnconfigure(1, weight=95) # Main area stretches horizontally
        self.grid_rowconfigure(0, weight=1)    # Rows stretch vertically

        self.build_side_bar()
        self.build_main_container()

        self.show_inventory_screen()

    def build_side_bar(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False) # Forces frame to strictly keep its custom width

        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(0, weight=0)
        self.sidebar_frame.grid_rowconfigure(1, weight=0)
        self.sidebar_frame.grid_rowconfigure(2, weight=0)
        self.sidebar_frame.grid_rowconfigure(3, weight=0)

        customtkinter.CTkLabel(
            self.sidebar_frame,
            text="NAVIGATION",
            text_color="white",
            font=customtkinter.CTkFont(size=14, weight="normal")
        ).grid(row=0, column=0, padx=10, pady=20, sticky="w")
        customtkinter.CTkButton(
            self.sidebar_frame,
            text="📦  Inventory Manager",
            command=self.show_inventory_screen,
            fg_color="gainsboro",
            text_color="black",
            font=customtkinter.CTkFont(size=18, weight="normal")
        ).grid(row=1, column=0, padx=10, pady=10, sticky="we")
        customtkinter.CTkButton(
            self.sidebar_frame,
            text="👤  Supplier Log",
            command=self.show_supplier_screen,
            fg_color="gainsboro",
            text_color="black",
            font=customtkinter.CTkFont(size=18, weight="normal")
        ).grid(row=2, column=0, padx=10, pady=10, sticky="we")
        customtkinter.CTkButton(
            self.sidebar_frame,
            text="🛒 Billing (Cash Register)",
            command=self.show_billing_screen,
            fg_color="gainsboro",
            text_color="black",
            font=customtkinter.CTkFont(size=18, weight="normal")
        ).grid(row=3, column=0, padx=10, pady=10, sticky="we")

    def build_main_container(self):
        self.main_area = customtkinter.CTkFrame(self, fg_color="white")
        self.main_area.grid(row=0, column=1, sticky="nsew")

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_inventory_screen(self):
        self.clear_main_area()

        self.main_area.grid_columnconfigure(0, weight=2)
        self.main_area.grid_columnconfigure(1, weight=8)
        self.main_area.grid_rowconfigure(0, weight=0)
        self.main_area.grid_rowconfigure(1, weight=1)

        self.render_inventory_header()
        self.render_inventory_form()
        self.render_inventory_table()
        
        self.load_inventory_items()

    def render_inventory_header(self):
        self.inventory_header_frame = customtkinter.CTkFrame(self.main_area, height=80, fg_color="transparent")
        self.inventory_header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 50), sticky="ew")
        self.inventory_header_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(
            self.inventory_header_frame,
            text_color="black",
            text="Inventory Manager",
            font=customtkinter.CTkFont(size=26, weight="bold"),
            anchor="w"
        ).grid(row=0, column=0, padx=(20,20), pady=(10,0), sticky="w")
        customtkinter.CTkLabel(
            self.inventory_header_frame,
            text_color="gray",
            text="Track and manage item prices, stock levels, and low stock alerts.",
            font=customtkinter.CTkFont(size=14, weight="normal"),
            anchor="w"
        ).grid(row=1, column=0, padx=(20,20), pady=(0,5), sticky="w")
        customtkinter.CTkFrame(
            self.inventory_header_frame,
            height=2,
            fg_color="grey"
        ).grid(row=2, column=0, padx=(20,20), sticky="we")

    def render_inventory_form(self):
        self.inventory_form_frame = customtkinter.CTkScrollableFrame(self.main_area, fg_color="gainsboro", corner_radius=10)
        self.inventory_form_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 150), sticky="nsew")
        self.inventory_form_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(
            self.inventory_form_frame,
            text="＋Add/Edit Item",
            text_color="black",
            font=customtkinter.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=(10, 10), pady=(20, 20), sticky="w")

        customtkinter.CTkFrame(
            self.inventory_form_frame,
            height=2,
            fg_color="black",
        ).grid(row=1, column=0, padx=(10, 10), sticky="we")

        customtkinter.CTkLabel(self.inventory_form_frame, text="Item Name:", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")
        self.inv_name_entry = customtkinter.CTkEntry(self.inventory_form_frame, placeholder_text="e.g. Bread", fg_color="white", text_color="black")
        self.inv_name_entry.grid(row=3, column=0, padx=10, pady=(0,10), sticky="we")
        
        customtkinter.CTkLabel(self.inventory_form_frame, text="Price (₹):", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=4, column=0, padx=10, pady=(0,0), sticky="w",)
        self.inv_price_entry = customtkinter.CTkEntry(self.inventory_form_frame, placeholder_text="0.00", fg_color="white", text_color="black")
        self.inv_price_entry.grid(row=5, column=0, padx=10, pady=(0,10), sticky="we")
        
        customtkinter.CTkLabel(self.inventory_form_frame, text="Stock:", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=6, column=0, padx=10, pady=(0,0), sticky="w")
        self.inv_stock_entry = customtkinter.CTkEntry(self.inventory_form_frame, placeholder_text="0", fg_color="white", text_color="black")
        self.inv_stock_entry.grid(row=7, column=0, padx=10, pady=(0,10), sticky="we")

        customtkinter.CTkButton(
            self.inventory_form_frame,
            text="📦  Save Item to Inventory",
            command=self.save_item_to_inventory,
            font=customtkinter.CTkFont(size=16, weight="normal")
        ).grid(row=8, column=0, padx=10, pady=10, sticky="we")

    def render_inventory_table(self):
        self.inventory_table_frame = customtkinter.CTkScrollableFrame(self.main_area, fg_color="gainsboro", corner_radius=10)
        self.inventory_table_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 150), sticky="nsew")

        for i in range(5):
            self.inventory_table_frame.grid_columnconfigure(i, weight=1)

        customtkinter.CTkLabel(
            self.inventory_table_frame,
            text="Stock Items Table",
            text_color="black",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            corner_radius=10
        ).grid(row=0, column=0, columnspan=5, padx=(20, 20), pady=(10, 10), sticky="w")

        customtkinter.CTkFrame(
            self.inventory_table_frame,
            height=2,
            fg_color="black",
        ).grid(row=1, column=0, columnspan=5, padx=(20, 20), sticky="we")

        # Table Header Labels
        headers = ["ID","ITEM NAME","PRICE","STOCK LEVEL","ACTION"]
        for col_idx, text in enumerate(headers):
            customtkinter.CTkLabel(
                self.inventory_table_frame,
                text=text,
                text_color="black",
                font=customtkinter.CTkFont(size=14, weight="normal")
            ).grid(row=2, column=col_idx, padx=(20,5), pady=(20,5))

    def clear_inventory_form_inputs(self):
        self.inv_name_entry.delete(0, tkinter.END)
        self.inv_price_entry.delete(0, tkinter.END)
        self.inv_stock_entry.delete(0, tkinter.END)

    def load_inventory_items(self):
        for widget in self.inventory_table_frame.winfo_children():
            if int(widget.grid_info().get("row", 0)) >= 3:
                widget.destroy()

        self.db.cursor.execute("SELECT id, name, price, stock FROM items")
        for i, row in enumerate(self.db.cursor.fetchall()):
            id, name, price, stock = row        
            customtkinter.CTkLabel(self.inventory_table_frame, text=f"{id}", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=3+i, column=0, padx=(20,5), pady=(0,5))
            customtkinter.CTkLabel(self.inventory_table_frame, text=f"{name}", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=3+i, column=1, padx=(5,5), pady=(0,5))
            customtkinter.CTkLabel(self.inventory_table_frame, text=f"{price:.2f}", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=3+i, column=2, padx=(5,5), pady=(0,5))
            if stock<=3:
                customtkinter.CTkLabel(self.inventory_table_frame, text=f"{stock}", text_color="red", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=3+i, column=3, padx=(5,5), pady=(0,5))
            else:
                customtkinter.CTkLabel(self.inventory_table_frame, text=f"{stock}", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=3+i, column=3, padx=(5,5), pady=(0,5))
            customtkinter.CTkButton(
                self.inventory_table_frame,
                text="🗑", 
                fg_color="transparent", 
                hover_color="red", 
                text_color="black", 
                command=lambda current_id=id, current_name=name:self.delete_item_from_inventory(current_id, current_name), 
                font=customtkinter.CTkFont(size=14, weight="normal")
            ).grid(row=3+i, column=4, padx=(5,20), pady=(0,5))    

    def delete_item_from_inventory(self, id, name):
        confirm = tkinter.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this item : '{name}'")
        if confirm:
            try:
                self.db.cursor.execute("DELETE FROM items WHERE id = ?", (id,))
                self.db.conn.commit()
                # Clear inputs & refresh
                self.load_inventory_items()
                tkinter.messagebox.showinfo("Success", "Successfully deleted the item!")
            except sqlite3.Error as error:
                tkinter.messagebox.showerror("Database Error", f"Failed to delete item: {error}")

    def save_item_to_inventory(self):
        name = self.inv_name_entry.get().strip()
        price = self.inv_price_entry.get().strip()
        stock = self.inv_stock_entry.get().strip()

        if not name or not price or not stock:
            tkinter.messagebox.showerror("Error", "All fields are required")
            return

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            tkinter.messagebox.showerror("Error", "Prices must be numeric and Stock must be integer.")
            return

        self.db.cursor.execute("SELECT id FROM items WHERE name = ?", (name,))
        existing = self.db.cursor.fetchone()
        
        if existing:
            self.db.cursor.execute("UPDATE items SET price = ?, stock = ? WHERE id = ?", (price, stock, existing[0]))
            msg = "Successfully updated the item!"
        else:
            self.db.cursor.execute("INSERT INTO items (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
            msg = "Successfully added the item!"
        
        self.db.conn.commit()
        self.clear_inventory_form_inputs()
        self.load_inventory_items()
        tkinter.messagebox.showinfo("Success", msg)


    def show_supplier_screen(self):
        self.clear_main_area()
        
        self.render_supplier_header()
        self.render_supplier_form()
        self.render_supplier_table()
        self.load_supplier_names()

    def render_supplier_header(self):
        self.supplier_header_frame = customtkinter.CTkFrame(self.main_area, height=80, fg_color="transparent")
        self.supplier_header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 50), sticky="ew")
        self.supplier_header_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(
            self.supplier_header_frame,
            text_color="black",
            text="Inventory Manager",
            font=customtkinter.CTkFont(size=26, weight="bold"),
            anchor="w"
        ).grid(row=0, column=0, padx=(20,20), pady=(10,0), sticky="w")
        customtkinter.CTkLabel(
            self.supplier_header_frame,
            text_color="gray",
            text="Track and manage item prices, stock levels, and low stock alerts.",
            font=customtkinter.CTkFont(size=14, weight="normal"),
            anchor="w"
        ).grid(row=1, column=0, padx=(20,20), pady=(0,5), sticky="w")
        customtkinter.CTkFrame(
            self.supplier_header_frame,
            height=2,
            fg_color="grey"
        ).grid(row=2, column=0, padx=(20,20), sticky="we")

    def render_supplier_form(self):
        self.supplier_form_frame = customtkinter.CTkScrollableFrame(self.main_area, fg_color="gainsboro", corner_radius=10)
        self.supplier_form_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 150), sticky="nsew")
        self.supplier_form_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(
            self.supplier_form_frame,
            text="＋Add/Edit Item",
            text_color="black",
            font=customtkinter.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=(10, 10), pady=(20, 20), sticky="w")

        customtkinter.CTkFrame(
            self.supplier_form_frame,
            height=2,
            fg_color="black",
        ).grid(row=1, column=0, padx=(10, 10), sticky="we")

        customtkinter.CTkLabel(self.supplier_form_frame, text="Supplier Name/Company:", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")
        self.supplier_name_entry = customtkinter.CTkEntry(self.supplier_form_frame, placeholder_text="e.g. Fresh Produce Ltd", fg_color="white", text_color="black")
        self.supplier_name_entry.grid(row=3, column=0, padx=10, pady=(0,10), sticky="we")
        
        customtkinter.CTkLabel(self.supplier_form_frame, text="Phone Number:", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=4, column=0, padx=10, pady=(0,0), sticky="w",)
        self.supplier_phone_entry = customtkinter.CTkEntry(self.supplier_form_frame, placeholder_text="e.g. +91-98182 21", fg_color="white", text_color="black")
        self.supplier_phone_entry.grid(row=5, column=0, padx=10, pady=(0,10), sticky="we")
        
        customtkinter.CTkLabel(self.supplier_form_frame, text="Address:", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=6, column=0, padx=10, pady=(0,0), sticky="w")
        self.supplier_address_entry = customtkinter.CTkEntry(self.supplier_form_frame, placeholder_text="e.g. Model town, pathankot", fg_color="white", text_color="black")
        self.supplier_address_entry.grid(row=7, column=0, padx=10, pady=(0,10), sticky="we")

        customtkinter.CTkButton(
            self.supplier_form_frame,
            text="+  Add Supplier Record",
            command=self.save_supplier,
            font=customtkinter.CTkFont(size=16, weight="normal")
        ).grid(row=8, column=0, padx=10, pady=10, sticky="we")


    def render_supplier_table(self):
        self.supplier_table_frame = customtkinter.CTkScrollableFrame(self.main_area, fg_color="gainsboro", corner_radius=10)
        self.supplier_table_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 50), sticky="nsew")

        for i in range(5):
            self.supplier_table_frame.grid_columnconfigure(i, weight=1)

        customtkinter.CTkLabel(
            self.supplier_table_frame,
            text="Stock Items Table",
            text_color="black",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            corner_radius=10
        ).grid(row=0, column=0, columnspan=5, padx=(20, 20), pady=(10, 10), sticky="w")

        customtkinter.CTkFrame(
            self.supplier_table_frame,
            height=2,
            fg_color="black",
        ).grid(row=1, column=0, columnspan=5, padx=(20, 20), sticky="we")        

        # Table Headers Labels
        headers = ["ID","SUPPLIER/BUSINESS","PHONE NUMBER","ADDRESS","ACTION"]
        for col_idx, text in enumerate(headers):
            customtkinter.CTkLabel(
                self.supplier_table_frame,
                text=text,
                text_color="black",
                font=customtkinter.CTkFont(size=14, weight="normal")
            ).grid(row=2, column=col_idx, padx=(20,5), pady=(20,5))

    def clear_supplier_form_inputs(self):
        self.supplier_address_entry.delete(0, tkinter.END)
        self.supplier_name_entry.delete(0, tkinter.END)
        self.supplier_phone_entry.delete(0, tkinter.END)

    def load_supplier_names(self):
        for widget in self.supplier_table_frame.winfo_children():
            if int(widget.grid_info().get("row", 0)) >= 3:
                widget.destroy()

        self.db.cursor.execute("SELECT id, name, phone, address FROM suppliers")
        for i, row in enumerate(self.db.cursor.fetchall()):
            item_id, name, phone, address = row        
            customtkinter.CTkLabel(self.supplier_table_frame, text=f"{item_id}", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=3+i, column=0, padx=(10,0), pady=(0,5))
            customtkinter.CTkLabel(self.supplier_table_frame, text=f"{name}", text_color="black", wraplength=150, font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=3+i, column=1, padx=(0,0), pady=(0,5))
            customtkinter.CTkLabel(self.supplier_table_frame, text=f"{phone}", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=3+i, column=2, padx=(0,0), pady=(0,5))
            customtkinter.CTkLabel(self.supplier_table_frame, text=f"{address}", text_color="black", wraplength=150, font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=3+i, column=3, padx=(0,0), pady=(0,5))
            customtkinter.CTkButton(
                self.supplier_table_frame,
                text="🗑",
                fg_color="transparent",
                hover_color="red",
                text_color="black",
                command=lambda current_id=item_id, current_name=name : self.delete_supplier(current_id, current_name),
                font=customtkinter.CTkFont(size=14, weight="normal")
            ).grid(row=3+i, column=4, padx=(0,10), pady=(0,5))

    def delete_supplier(self, id, name):
        confirm = tkinter.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this supplier : {name}")
        if confirm:
            try:
                self.db.cursor.execute("DELETE FROM suppliers WHERE id = ?", (id,))
                self.db.conn.commit()
                # Clear inputs & refresh
                self.load_supplier_names()
                tkinter.messagebox.showinfo("Success", "Successfully deleted the supplier!")
            except sqlite3.Error as error:
                tkinter.messagebox.showerror("Database Error", f"Failed to delete supplier: {error}")

    def save_supplier(self):
        name = self.supplier_name_entry.get().strip()
        phone = self.supplier_phone_entry.get().strip()
        address = self.supplier_address_entry.get().strip()

        if not name or not phone or not address:
            tkinter.messagebox.showerror("Error", "These fields are required")
            return

        self.db.cursor.execute("SELECT id FROM suppliers WHERE name = ?", (name,))
        existing = self.db.cursor.fetchone()
        
        if existing:
            self.db.cursor.execute("UPDATE suppliers SET name = ?, phone = ?, address = ? WHERE id = ?", (name, phone, address, existing[0]))
            msg = "Successfully updated the supplier detail!"
        else:
            self.db.cursor.execute("INSERT INTO suppliers (name, phone, address) VALUES (?, ?, ?)", (name, phone, address))
            msg = "Successfully added the supplier!"

        self.db.conn.commit()
        self.clear_supplier_form_inputs()
        self.load_supplier_names()
        tkinter.messagebox.showinfo("Success", msg)


    def show_billing_screen(self):
        self.clear_main_area()
        
        self.render_billing_header()
        self.render_billing_form()
        self.render_billing_table()
        self.load_billing_cart()    

    def render_billing_header(self):
        self.billing_header_frame = customtkinter.CTkFrame(self.main_area, height=80, fg_color="transparent")
        self.billing_header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 50), sticky="ew")
        self.billing_header_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(
            self.billing_header_frame,
            text_color="black",
            text="Billing Screen (Cash Register)",
            font=customtkinter.CTkFont(size=26, weight="bold"),
            anchor="w"
        ).grid(row=0, column=0, padx=(20,20), pady=(10,0), sticky="w")
        customtkinter.CTkLabel(
            self.billing_header_frame,
            text_color="gray",
            text="Process customer transactions, auto-calculate totals, and update stock.",
            font=customtkinter.CTkFont(size=14, weight="normal"),
            anchor="w"
        ).grid(row=1, column=0, padx=(20,20), pady=(0,5), sticky="w")
        
        customtkinter.CTkFrame(
            self.billing_header_frame,
            height=2,
            fg_color="grey"
        ).grid(row=2, column=0, padx=(20,20), sticky="we")

    def render_billing_form(self):

        if hasattr(self, 'billing_form_frame') and self.billing_form_frame.winfo_exists():
            self.billing_form_frame.destroy()

        self.billing_form_frame = customtkinter.CTkScrollableFrame(self.main_area, fg_color="gainsboro", corner_radius=10)
        self.billing_form_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 150), sticky="nsew")
        self.billing_form_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(
            self.billing_form_frame,
            text="🔎 Select Product",
            text_color="black",
            font=customtkinter.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=(10, 10), pady=(20, 20), sticky="w")

        customtkinter.CTkFrame(
            self.billing_form_frame,
            height=2,
            fg_color="black",
        ).grid(row=1, column=0, padx=(10, 10), sticky="we")

        self.db.cursor.execute("SELECT id, name, stock FROM items")
        raw_data = self.db.cursor.fetchall()
        formatted_item_list = []
        for row in raw_data:
            id, name, stock= row
            display_string = f"{name} - ({stock} available) : {id}"
            formatted_item_list.append(display_string)

        if formatted_item_list != [] :
            customtkinter.CTkLabel(self.billing_form_frame, text="Choose Item from Inventory:", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")
            self.inventory_select_entry = customtkinter.CTkComboBox(self.billing_form_frame, fg_color="white", text_color="black")
            self.inventory_select_entry.grid(row=3, column=0, padx=10, pady=(0,10), sticky="we")    
            CTkScrollableDropdown(self.inventory_select_entry, values=formatted_item_list, height=300, width =600, autocomplete=True)
            self.inventory_select_entry.set("")

            customtkinter.CTkLabel(self.billing_form_frame, text="Quantity:", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=4, column=0, padx=10, pady=(0,0), sticky="w",)
            self.item_quantity_entry = customtkinter.CTkEntry(self.billing_form_frame, placeholder_text="e.g. 10", fg_color="white", text_color="black")
            self.item_quantity_entry.grid(row=5, column=0, padx=10, pady=(0,10), sticky="we")
        
            customtkinter.CTkButton(
                self.billing_form_frame,
                text="🛍 Add to Billing Card",
                command=self.add_item_to_cart,
                font=customtkinter.CTkFont(size=16, weight="normal")
            ).grid(row=8, column=0, padx=10, pady=10, sticky="we")
        

    def render_billing_table(self):
        self.billing_table_frame = customtkinter.CTkScrollableFrame(self.main_area, fg_color="gainsboro", corner_radius=10)
        self.billing_table_frame.grid(row=1, column=1, padx=(0,20), pady=(0,150), columnspan=2, sticky="nsew")

        self.billing_table_frame.grid_columnconfigure(0, weight=1)
        self.billing_table_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(
            self.billing_table_frame,
            text="Current Cart Items",
            text_color="black",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            corner_radius=10
        ).grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="w")
        customtkinter.CTkButton(
            self.billing_table_frame,
            text="🗑 Clear Cart",
            command=self.clear_cart,
            text_color="red",
            fg_color="transparent",
            corner_radius=10,
            font=customtkinter.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=1, columnspan=2, padx=(0,10), pady=(10,10), sticky="e")
        customtkinter.CTkFrame(
            self.billing_table_frame,
            height=2,
            fg_color="black",
        ).grid(row=1, column=0, columnspan=2, padx=(10, 10), sticky="we")

        self.cart_frame = customtkinter.CTkScrollableFrame(self.billing_table_frame, fg_color="white", corner_radius=10, height=150)
        self.cart_frame.grid(row=2, column=0, padx=(10,10), pady=(20,10), columnspan=2, sticky="we")

        for i in range(5):
            self.cart_frame.grid_columnconfigure(i, weight=1)

        headers = ["ITEM","UNIT PRICE","QTY","SUBTOTAL","ACTION"]
        for col_idx, text in enumerate(headers):
            customtkinter.CTkLabel(
                self.cart_frame,
                text=text,
                text_color="black",
                font=customtkinter.CTkFont(size=14, weight="normal")
            ).grid(row=0, column=col_idx, padx=(5,5), pady=(5,5))

    def load_billing_cart(self):
        for widget in self.cart_frame.winfo_children():
            if int(widget.grid_info().get("row", 0)) >= 1:
                widget.destroy()

        for widget in self.billing_table_frame.winfo_children():
            row_num = int(widget.grid_info().get("row", 0))
            if row_num ==3 or row_num==4:
                widget.destroy()
        
        self.total_price = 0.00
        for i, item_dict in enumerate(self.cart_list):
            item_id = item_dict["id"]
            name = item_dict["name"]
            price = item_dict["price"]
            qty = item_dict["quantity"]
            subtotal = item_dict["subtotal"]
            customtkinter.CTkLabel(self.cart_frame, text=name, text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=1+i, column=0, padx=(5,5), pady=(0,5))
            customtkinter.CTkLabel(self.cart_frame, text=f"{price:.2f}", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=1+i, column=1, padx=(5,5), pady=(0,5))
            customtkinter.CTkLabel(self.cart_frame, text=str(qty), text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=1+i, column=2, padx=(5,5), pady=(0,5))
            customtkinter.CTkLabel(self.cart_frame, text=f"{subtotal:.2f}", text_color="black", font=customtkinter.CTkFont(size=14, weight="normal")).grid(row=1+i, column=3, padx=(5,5), pady=(0,5))
            customtkinter.CTkButton(
                self.cart_frame, 
                text="🗑", 
                fg_color="transparent", 
                hover_color="red", 
                command=lambda idx=i: self.remove_item_from_cart(idx),
                text_color="black", 
                font=customtkinter.CTkFont(size=14, weight="normal")
            ).grid(row=i+1, column=4, padx=(5,5), pady=(0,5))

            self.total_price = self.total_price + subtotal

        customtkinter.CTkLabel(
            self.billing_table_frame,
            text=f"GRAND TOTAL",
            text_color="black",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            corner_radius=10
        ).grid(row=3, column=0, columnspan=2, padx=(10, 10), pady=(5, 0), sticky="w")

        customtkinter.CTkLabel(
            self.billing_table_frame,
            text=f"₹{self.total_price:.2f}",
            text_color="green",
            font=customtkinter.CTkFont(size=34, weight="bold"),
            corner_radius=10
        ).grid(row=4, column=0, columnspan=2, padx=(10, 10), pady=(0, 5), sticky="w")            

        customtkinter.CTkButton(
            self.billing_table_frame,
            text="🧾 Generate Bill & Update Stock",
            command=self.generate_bill_update_stock,
            text_color="white", 
            fg_color="green",
            cursor="hand2",
            font=customtkinter.CTkFont(size=22, weight="bold"),
            corner_radius=10
        ).grid(row=3, column=1, rowspan=2, padx=(10, 10), pady=(5, 5), sticky="e")

    
    def add_item_to_cart(self):
        if not hasattr(self, 'inventory_select_entry') or not hasattr(self, 'item_quantity_entry'):
            tkinter.messagebox.showerror("Error", "No item selected")
            return
        
        selected_val = self.inventory_select_entry.get().strip()
        qty_str = self.item_quantity_entry.get().strip()
        
        if not selected_val or not qty_str:
            tkinter.messagebox.showerror("Error", "These fields are required")
            return
        
        try:
            quantity = int(qty_str)
            if quantity <= 0:
                tkinter.messagebox.showerror("Error", "Quantity must be greater than zero.")
                return
            item_id = int(selected_val.split(":")[-1].strip())
            
            self.db.cursor.execute("SELECT id, name, price, stock FROM items WHERE id = ?", (item_id,))
            data = self.db.cursor.fetchone()
            
            if not data:
                tkinter.messagebox.showerror("Error", "Item not found in database.")
                return

            if data[3] < quantity:
                tkinter.messagebox.showerror("Error", "The selected quantity is more than the existing stock.")
                return

            # Append structured dictionary to cart
            self.cart_list.append({
                "id": data[0],
                "name": data[1],
                "price": data[2],
                "quantity": quantity,
                "subtotal": data[2] * quantity
            })

            self.clear_billing_form_input()
            self.load_billing_cart()
            
        except ValueError:
            tkinter.messagebox.showerror("Error", "Some error occured!")

        self.load_billing_cart()

    def remove_item_from_cart(self, index):
        if 0 <= index < len(self.cart_list):
            self.cart_list.pop(index)
            self.load_billing_cart()

    def clear_cart(self):
        self.cart_list.clear()
        self.load_billing_cart()

    def clear_billing_form_input(self):
        if hasattr(self, 'inventory_select_entry'):
            self.inventory_select_entry.set("")
        if hasattr(self, 'item_quantity_entry'):
            self.item_quantity_entry.delete(0, tkinter.END)

    def generate_bill_update_stock(self):
        for i, item_dict in enumerate(self.cart_list):
            item_id = item_dict["id"]
            qty = int(item_dict["quantity"])

            self.db.cursor.execute("SELECT stock FROM items WHERE id = ?", (item_id,))
            price_value = self.db.cursor.fetchone()
            self.db.cursor.execute("UPDATE items SET stock=? WHERE id=?", (price_value[0]-qty, item_id,))
            self.db.conn.commit() 

        self.clear_billing_form_input()
        self.clear_cart()
        self.load_billing_cart()
        self.render_billing_form()
        
    
shop = Shop()
shop.mainloop()