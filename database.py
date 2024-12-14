import sqlite3

### DATABASE CONNECTION ###

def get_db_connection():
    """Helper function to get a database connection."""
    return sqlite3.connect('Books.db')

### DATABASE SETUP ###

def create_books_table():
    """Create the Books table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        total_sales INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def create_order_table():
    """Create the Orders table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(book_id) REFERENCES Books(id)
    )''')
    conn.commit()
    conn.close()

def create_sales_report_table():
    """Create the Sales_Report table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sales_Report (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_date DATE NOT NULL UNIQUE,
        total_sales REAL NOT NULL,
        total_orders INTEGER NOT NULL
    )''')
    conn.commit()
    conn.close()

def create_admin_table():
    """Create the Admin table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Admin (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Initialize the database and tables
def initialize_database():
    create_books_table()
    create_order_table()
    create_sales_report_table()
    create_admin_table()

### BOOKS TABLE FUNCTIONS ###

def fetch_books():
    """Fetch all books from the Books table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    conn.close()
    return books

def insert_book(book_id, title, author, genre, quantity, price):
    """Insert a new book into the Books table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Books (id, title, author, genre, quantity, price)
                      VALUES (?, ?, ?, ?, ?, ?)''', (book_id, title, author, genre, quantity, price))
    conn.commit()
    conn.close()

def delete_book(book_id):
    """Delete a book by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def update_book_quantity(book_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Books SET quantity = ? WHERE id = ?', (quantity, book_id))
    conn.commit()
    conn.close()

def update_book_price(book_id, price):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Books SET price = ? WHERE id = ?', (price, book_id))
    conn.commit()
    conn.close()


def id_exists(book_id):
    """Check if a book ID exists in the Books table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Books WHERE id = ?', (book_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

def get_book_stock(book_id):
    """Fetch the stock quantity for a given book ID from the Books table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT quantity FROM Books WHERE id = ?', (book_id,))
    stock = cursor.fetchone()
    conn.close()
    return stock[0] if stock else 0

def update_book_stock(book_id, quantity):
    """Update the stock quantity of a book after an order is placed."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE Books
                      SET quantity = quantity - ?
                      WHERE id = ?''', (quantity, book_id))
    conn.commit()
    conn.close()

### ORDERS TABLE FUNCTIONS ###

def add_orders(book_id, quantity, total_price):
    """Add an order to the Orders table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Orders (book_id, quantity, total_price)
                      VALUES (?, ?, ?)''', (book_id, quantity, total_price))
    conn.commit()
    conn.close()

def fetch_orders():
    """Fetch orders from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, book_id, quantity, total_price, order_date FROM Orders")
    orders = cursor.fetchall()
    conn.close()
    return orders

    
def update_order_status(order_id, status):
    """Update the status of an order."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Orders SET status = ? WHERE id = ?
    ''', (status, order_id))
    conn.commit()
    conn.close()

def delete_order(order_id):
    """Delete an order by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

### SALES REPORT FUNCTIONS ###

def generate_sales_report():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT title, SUM(total_price) FROM Books
                      INNER JOIN Orders ON Books.id = Orders.book_id
                      GROUP BY Books.id''')
    report = cursor.fetchall()
    conn.close()
    return report


def fetch_sales_report():
    """Fetch the sales report for all books."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT books.title, SUM(orders.quantity * books.price) AS total_sales
                      FROM orders
                      JOIN books ON orders.book_id = books.id
                      GROUP BY books.id""")
    sales_report = cursor.fetchall()
    conn.close()
    return sales_report

### ADMIN TABLE FUNCTIONS ###

def insert_admin(username, password):
    """Insert a new admin into the Admin table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Admin (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def register_admin(username: str, password: str):
    """Add a new admin user to the credentials file."""
    try:
        with open("credentials.txt", "a") as file:
            file.write(f"{username},{password}\n")
            print("Admin registered successfully.")
    except Exception as e:
        print(f"Error writing to credentials file: {e}")

def authenticate_admin(username, password):
    """Check if the admin username and password are valid."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Admin WHERE username = ? AND password = ?', (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None
