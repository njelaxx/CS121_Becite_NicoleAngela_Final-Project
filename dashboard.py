import customtkinter as ctk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database

font1 = ('Sen', 25, 'bold')
font2 = ('Sen', 18, 'bold')
font3 = ('Sen', 13, 'bold')
menu_frame = None # Global variable to track the menu frame
# ----------------------------- Application Setup -----------------------------
# Initialize the application
def launch_dashboard():
    # Initialize the main application window
    app = ctk.CTk()
    app.geometry("1575x1200")
    app.resizable(True, True)
    app.config(bg="#0A0B0C")

    # ----------------------------- Title Section -----------------------------
    # Title Label
    addingform_label = ctk.CTkLabel(app, font=font1, text="Shelf Life: Digital Bookstore Assistant", text_color='#FFF', bg_color="#0A0B0C")
    addingform_label.place(x=80, y=10)

    # ----------------------------- Left Panel: Book Management -----------------------------
    # Left Panel Frame for Book Management
    frame = ctk.CTkFrame(app, fg_color='#1B1B21', corner_radius=10, width=450, height=600, border_width=2, border_color='#FFF')
    frame.place(x=20, y=60)

    # Input Fields for Book Management
    id_label = ctk.CTkLabel(frame, font=font2, text="Book ID:", text_color="#FFF", bg_color="#1B1B21")
    id_label.place(x=20, y=20)
    id_entry = ctk.CTkEntry(frame, font=font3, fg_color="#FFF", width=350)
    id_entry.place(x=20, y=60)

    title_label = ctk.CTkLabel(frame, font=font2, text="Title:", text_color="#FFF", bg_color="#1B1B21")
    title_label.place(x=20, y=100)
    title_entry = ctk.CTkEntry(frame, font=font3, fg_color="#FFF", width=350)
    title_entry.place(x=20, y=140)

    author_label = ctk.CTkLabel(frame, font=font2, text="Author:", text_color="#FFF", bg_color="#1B1B21")
    author_label.place(x=20, y=180)
    author_entry = ctk.CTkEntry(frame, font=font3, fg_color="#FFF", width=350)
    author_entry.place(x=20, y=220)

    genre_label = ctk.CTkLabel(frame, font=font2, text="Genre:", text_color="#FFF", bg_color="#1B1B21")
    genre_label.place(x=20, y=260)
    genre_entry = ctk.CTkEntry(frame, font=font3, fg_color="#FFF", width=350)
    genre_entry.place(x=20, y=300)

    quantity_label = ctk.CTkLabel(frame, font=font2, text="Quantity:", text_color="#FFF", bg_color="#1B1B21")
    quantity_label.place(x=20, y=340)
    quantity_entry = ctk.CTkEntry(frame, font=font3, fg_color="#FFF", width=350)
    quantity_entry.place(x=20, y=380)

    price_label = ctk.CTkLabel(frame, font=font2, text="Price:", text_color="#FFF", bg_color="#1B1B21")
    price_label.place(x=20, y=420)
    price_entry = ctk.CTkEntry(frame, font=font3, fg_color="#FFF", width=350)
    price_entry.place(x=20, y=460)

    # Action Buttons (Add, Update, Delete, Clear)
    def add_book():
        try:
            # Retrieve input values
            book_id = int(id_entry.get().strip())  # Convert to integer
            title = title_entry.get().strip()  # Ensure no extra spaces
            author = author_entry.get().strip()
            genre = genre_entry.get().strip()
            quantity = int(quantity_entry.get().strip())  # Convert to integer
            price = float(price_entry.get().strip())  # Convert to float

            # Validate inputs
            if not title or not author or not genre:
                raise ValueError("Title, Author, and Genre cannot be empty.")
            if quantity < 0 or price < 0:
                raise ValueError("Quantity and Price must be positive values.")

            # Insert into database
            database.insert_book(book_id, title, author, genre, quantity, price)

            # Show success message and refresh book table
            messagebox.showinfo("Success", "Book added successfully!")
            load_books()

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")

    def update_book():
        try:
            selected_item = tree.selection()
            if not selected_item:
                raise ValueError("Please select a book from the table to update.")
            
            # Retrieve selected book details
            book_id = int(tree.item(selected_item[0], 'values')[0])  # Get the ID from the first column
            quantity = int(quantity_entry.get().strip())
            price = float(price_entry.get().strip())

            # Ensure quantity and price are valid
            if quantity < 0 or price < 0:
                raise ValueError("Quantity and Price must be positive values.")

            # Update the book in the database
            if quantity > 0:
                database.update_book_quantity(book_id, quantity)
            if price > 0:
                database.update_book_price(book_id, price)

            messagebox.showinfo("Success", "Book updated successfully!")
            load_books()  # Refresh the book list

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))  # Handle invalid input
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update book: {str(e)}")
            
# Confirm delete book function to ask for confirmation and delete the book
    def confirm_delete_book():
        selected_item = tree.selection()  # Get the selected book from the Treeview
        if selected_item:
            book_id = tree.item(selected_item[0], 'values')[0]  # Assuming ID is the first column
            response = messagebox.askquestion("Delete Book", f"Are you sure you want to delete book ID {book_id}?", parent=app)
            if response == 'yes':
                try:
                # Directly delete the book from the database
                    database.delete_book(book_id)
                    messagebox.showinfo("Success", f"Book ID {book_id} deleted successfully!", parent=app)
                    load_books()  # Refresh the book list after deletion
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=app)
        else:
            messagebox.showwarning("Selection Error", "Please select a book to delete.", parent=app)


    # Function to handle the delete process
    def delete_selected_book():
        selected_item = tree.selection()  # Get the selected book from the Treeview
        if selected_item:
            confirm_delete_book()  # Call confirm_delete_book() without passing book_id
        else:
            messagebox.showwarning("Selection Error", "Please select a book to delete.")


    def clear_form():
        id_entry.delete(0, 'end')
        title_entry.delete(0, 'end')
        author_entry.delete(0, 'end')
        genre_entry.delete(0,'end')
        quantity_entry.delete(0, 'end') 
        price_entry.delete(0, 'end')

    # Buttons for Add, Update, Delete, and Clear
    add_button = ctk.CTkButton(frame, text="Add", font=font3, fg_color="#4CAF50", command=add_book)
    add_button.place(x=20, y=500)

    update_button = ctk.CTkButton(frame, text="Update", font=font3, fg_color="#FFA500", command=update_book)
    update_button.place(x=220, y=500)

    delete_button = ctk.CTkButton(frame, text="Delete", font=font3, fg_color="#F44336", command=delete_selected_book)
    delete_button.place(x=20, y=550)

    clear_button = ctk.CTkButton(frame, text="New", font=font3, fg_color="#2196F3", command=clear_form)
    clear_button.place(x=220, y=550)

    # ----------------------------- Right Panel: Book Table and Orders -----------------------------
    # Right Panel Frame for Table
    table_frame = ctk.CTkFrame(app, fg_color="#1B1B21", corner_radius=10, width=950, height=600, border_width=2, border_color="#FFF")
    table_frame.place(x=500, y=60)

    # Table for displaying Books
    columns = ("ID", "Title", "Author", "Genre", "Quantity", "Price")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Genre", text="Genre")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")

    tree.column("ID", width=100)
    tree.column("Title", width=300)
    tree.column("Author", width=200)
    tree.column("Genre", width=150)
    tree.column("Quantity", width=100)
    tree.column("Price", width=100)

    tree.pack(fill="both", expand=True)
 


# Function to toggle the menu
    def on_select_book(event):
        # Get the selected row from the Treeview
        selected_item = tree.selection()
        if selected_item:
            # Retrieve the book details from the selected row
            book_id = tree.item(selected_item[0], 'values')[0]
            title = tree.item(selected_item[0], 'values')[1]
            quantity = tree.item(selected_item[0], 'values')[4]
            price = tree.item(selected_item[0], 'values')[5]

            # Fill the entry fields with the selected data
            id_entry.delete(0, 'end')
            id_entry.insert(0, book_id)
            title_entry.delete(0, 'end')
            title_entry.insert(0, title)
            quantity_entry.delete(0, 'end')
            quantity_entry.insert(0, quantity)
            price_entry.delete(0, 'end')
            price_entry.insert(0, price)

    tree.bind("<<TreeviewSelect>>", on_select_book)  
       # ----------------------------- Menu Button Section -----------------------------
    def open_menu():
        global menu_frame

    # If the menu is already open, destroy it
        if menu_frame is not None and menu_frame.winfo_exists():
            menu_frame.destroy()
            menu_frame = None  # Reset the menu_frame variable
        else:
        # Create a menu frame
            menu_frame = ctk.CTkFrame(app, fg_color="#1B1B21", corner_radius=10, width=200, height=150)
            menu_frame.place(x=1550, y=60)

        # Add buttons for the menu options
            sales_button = ctk.CTkButton(menu_frame, text="Sales Report", font=font3, fg_color="#03A9F4", command=show_sales_graph)
            sales_button.pack(pady=10)

            order_dashboard_button = ctk.CTkButton(menu_frame, text="Order Dashboard", font=font3, fg_color="#03A9F4", command=lambda: open_order_dashboard(app))
            order_dashboard_button.pack(pady=10)

            logout_button = ctk.CTkButton(menu_frame, text="Logout", font=font3, fg_color="#F44336", command=confirm_logout)
            logout_button.pack(pady=10)


    # ----------------------------- Orders Section -----------------------------
    # Make Order Function with Stock Check
    def make_order():
        try:
            selected_item = tree.selection()  # Get the selected book from the Treeview

            # Check if an item is selected
            if not selected_item:
                raise Exception("Please select a book to order.")

            # Get the values of the selected book
            values = tree.item(selected_item[0], 'values')
            book_id = values[0]  # The book_id is the first column
            quantity = order_quantity_entry.get()

            # Validate the quantity input
            if not quantity.isdigit() or int(quantity) <= 0:
                raise Exception("Please enter a valid quantity.")

            quantity = int(quantity)

            # Check if the book has enough stock
            stock = database.get_book_stock(book_id)
            if stock < quantity:
                raise Exception(f"Insufficient stock. Only {stock} units available.")

            # Insert the order into the Orders table
            total_price = float(values[5]) * quantity  # price * quantity
            database.add_orders(book_id, quantity, total_price)

            # Update the book stock after the order is placed
            database.update_book_stock(book_id, quantity)

            messagebox.showinfo("Success", f"Order placed for {quantity} units of {values[1]}!")

            # Reload the books to update the quantity and sales info
            load_books()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Order Input Field and Button
    order_label = ctk.CTkLabel(app, text="Order Quantity:", font=font3, text_color="#FFF", bg_color="#0A0B0C")
    order_label.place(x=500, y=400)

    order_quantity_entry = ctk.CTkEntry(app, width=200, font=font3, fg_color="#FFF")
    order_quantity_entry.place(x=620, y=400)

    order_button = ctk.CTkButton(app, text="Make Order", font=font3, fg_color="#03A9F4", command=make_order)
    order_button.place(x=850, y=400)

    # Order Dashboard Button
    def open_order_dashboard(app):
    # Destroy the main window when opening the order dashboard
        app.destroy()

    # Create the Order Dashboard (Toplevel window)
        order_dashboard = ctk.CTkToplevel()
        order_dashboard.title("Order Dashboard")
        order_dashboard.geometry("800x600")
        order_dashboard.resizable(True, True)
        order_dashboard.config(bg="#0A0B0C")

    # --- Add Order Dashboard Widgets ---
        columns = ("Order ID", "Book ID", "Quantity", "Total Price", "Order Date")
        order_tree = ttk.Treeview(order_dashboard, columns=columns, show="headings", height=15)
        order_tree.heading("Order ID", text="Order ID")
        order_tree.heading("Book ID", text="Book ID")
        order_tree.heading("Quantity", text="Quantity")
        order_tree.heading("Total Price", text="Total Price")
        order_tree.heading("Order Date", text="Order Date")
        order_tree.pack(fill="both", expand=True, padx=20, pady=20)

    # Populate the orders table
        orders = database.fetch_orders()
        for order in orders:
            order_tree.insert('', 'end', values=order)

    # --- Close Button to Return to Main Window ---
        close_button = ctk.CTkButton(order_dashboard, text="Close", font=font3, fg_color="#F44336", command=lambda: close_order_dashboard(order_dashboard))
        close_button.place(x=350, y=500)


        def close_order_dashboard(order_dashboard):
    # Destroy the order dashboard and reopen the main window
            order_dashboard.destroy()
            launch_dashboard()  # Reopen the main window

        
        def load_orders():
            orders = database.fetch_orders()
            for row in order_tree.get_children():
                order_tree.delete(row)
            for order in orders:
                order_tree.insert('', 'end', values=order)

# Function to handle the void process
        def void_selected_order():
            selected_item = order_tree.selection()  # Get the selected order from the Treeview
            if selected_item:
                confirm_void_order()  # Call confirm_void_order() without passing order_id
            else:
                messagebox.showwarning("Selection Error", "Please select an order to void.")

# Confirm void order function to ask for confirmation and void the order
        def confirm_void_order():
            selected_item = order_tree.selection()  # Get the selected order from the Treeview
            if selected_item:
                order_id = order_tree.item(selected_item[0], 'values')[0]  # Assuming Order ID is the first column
                response = messagebox.askquestion("Void Order", f"Are you sure you want to void order ID {order_id}?", parent=order_dashboard)
                if response == 'yes':
                    try:
                # Directly void the order from the database
                        database.delete_order(order_id)  # Assuming a function like `delete_order()` exists in your `database.py`
                        messagebox.showinfo("Success", f"Order ID {order_id} voided successfully!", parent=order_dashboard)
                        load_orders()  # Refresh the orders list after voiding the order
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to void order ID {order_id}: {str(e)}", parent=order_dashboard)
            else:
                messagebox.showwarning("Selection Error", "Please select an order to void.", parent=order_dashboard)

# Void Order button
        void_button = ctk.CTkButton(order_dashboard, text="Void Order", fg_color="#F44336", command=void_selected_order)
        void_button.pack(side="left", padx=10, pady=10)
    
    def confirm_logout():
        response = messagebox.askquestion("Logout", "Are you sure you want to log out?")
        if response == 'yes':
            logout()  # Perform logout

    def logout():
        messagebox.showinfo("Logout", "Logging out...")  # Implement actual logout logic here
        app.quit()

    # Menu button (in upper-right corner of the right panel)
    menu_button = ctk.CTkButton(app, text="Menu", font=font3, fg_color="#03A9F4", command=open_menu)
    menu_button.place(x=1550, y=30)

    # ----------------------------- Sales Graph Section -----------------------------
    # Show Sales Graph Function
    def show_sales_graph():
        sales_data = database.fetch_sales_report()

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        titles = [data[0] for data in sales_data]
        sales = [data[1] for data in sales_data]

        ax.bar(titles, sales, color="green")
        ax.set_title("Sales Report")
        ax.set_ylabel("Total Sales")
        ax.set_xlabel("Books")

        # Embed the graph in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=app)
        canvas.get_tk_widget().place(x=500, y=510)
        canvas.draw()

    # ----------------------------- Load Books Function -----------------------------
    def load_books():
        # Clear the existing data in the table
        for row in tree.get_children():
            tree.delete(row)

        # Fetch books from the database
        books = database.fetch_books()

        # Insert books into the Treeview
        for book in books:
            # Ensure column order matches the Treeview headers: ID, Title, Author, Genre, Quantity, Price
            tree.insert('', 'end', values=(book[0], book[1], book[2], book[3], book[4], book[5]))

    # ----------------------------- Main Application Loop -----------------------------
    # Initialize the app with loaded books
    load_books()
    app.mainloop()
