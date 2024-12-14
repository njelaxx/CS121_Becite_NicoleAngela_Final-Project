import json
from PIL import Image, ImageTk 
import tkinter as tk
from tkinter import messagebox, Canvas, PhotoImage, Entry, Button, Label
from pathlib import Path
from dashboard import launch_dashboard  # Import the launch_dashboard function from the dashboard.py file

# Set the assets path
ASSETS_PATH = Path("C:/Users/DELL/Desktop/Tkinter-Designer-master/build/assets/frame0")

def relative_to_assets(path: str) -> str:
    """Resolve asset paths."""
    full_path = ASSETS_PATH / Path(path)
    if not full_path.exists():
        print(f"Error: File not found - {full_path}")
    return str(full_path)

def update_image(canvas, image_key, file_path, width):
    """Update an image on the canvas with a specified width, maintaining aspect ratio."""
    try:
        # Open and resize the image
        original_image = Image.open(file_path)
        aspect_ratio = original_image.height / original_image.width
        resized_image = original_image.resize((width, int(width * aspect_ratio)), Image.ANTIALIAS)
        image_refs[image_key] = ImageTk.PhotoImage(resized_image)
        # Update the canvas image
        canvas.itemconfig(image_key, image=image_refs[image_key])
    except Exception as e:
        print(f"Error resizing image {file_path}: {e}")

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Create a rounded rectangle on a Tkinter canvas."""
    points = [
        (x1 + radius, y1), (x2 - radius, y1),
        (x2, y1), (x2, y1 + radius),
        (x2, y2 - radius), (x2, y2),
        (x2 - radius, y2), (x1 + radius, y2),
        (x1, y2), (x1, y2 - radius),
        (x1, y1 + radius), (x1, y1)
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)
# Function to add a new admin to the JSON file
def add_admin(username, password):
    try:
        with open('admins.json', 'r') as f:
            admins = json.load(f)
    except FileNotFoundError:
        admins = []  # If the file doesn't exist, create a new list

    # Add the new admin to the list
    admins.append({"username": username, "password": password})

    # Save the updated list back to the JSON file
    with open('admins.json', 'w') as f:
        json.dump(admins, f)
    messagebox.showinfo("Success", "Admin added successfully!")

# Function to validate admin login
def validate_admin(username, password):
    try:
        with open('admins.json', 'r') as f:
            admins = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Admin data not found!")
        return False  # If file doesn't exist, return False

    # Check if the username and password match any entry in the list
    for admin in admins:
        if admin["username"] == username and admin["password"] == password:
            return True
    return False

def authenticate_admin(username: str, password: str) -> bool:
    """Authenticate admin by checking credentials from admins.json."""
    return validate_admin(username, password)

def attempt_login(username_entry, password_entry, root):
    """Handle login attempts."""
    username = username_entry.get()  # Get entered username
    password = password_entry.get()  # Get entered password

    if authenticate_admin(username, password):  # Authenticate using the updated function
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()  # Close login window
        launch_dashboard()  # Open main dashboard window after login
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def create_ui(window):
    """Create the GUI for the login page."""
    window.geometry("1575x1200")
    window.configure(bg="#0B0C10")
    window.title("Login Page")

    canvas = Canvas(
        window,
        bg="#0B0C10",
        height=1024,
        width=1440,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )
    canvas.place(x=0, y=0)

    global image_refs
    image_refs = {}

    # Load and place images
    try:
        image_refs["image_1"] = canvas.create_image(730.0, 75.0, anchor="n")  # Placeholder for dynamic resizing
        file_path = relative_to_assets("image_1.png")
        update_image(canvas, "image_1", file_path, window.winfo_width() // 2)
    except Exception as e:
        print("Error loading image_1.png:", e)


    try:
        image_refs["image_2"] = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas.create_image(68.0, 65.0, image=image_refs["image_2"])
    except Exception as e:
        print("Error loading image_2.png:", e)

    # Add text elements
    canvas.create_text(
        113.0,
        35.0,
        anchor="nw",
        text="Shelf Life",
        fill="#FFFFFF",
        font=("Sen ExtraBold", 48),
    )
    canvas.create_text(
        830.0,
        312.0,
        anchor="nw",
        text="WELCOME ADMIN",
        fill="#FFFFFF",
        font=("Sen ExtraBold", 48),
    )

    # Add username and password labels
    canvas.create_text(
        950.0,
        440.0,
        anchor="nw",
        text="Username",
        fill="#FFFFFF",
        font=("Sen Bold", 24),
    )
    canvas.create_text(
        950.0,
        522.0,
        anchor="nw",
        text="Password",
        fill="#FFFFFF",
        font=("Sen Bold", 24),
    )

    # Add background for username and password fields
    create_rounded_rectangle(canvas, 945, 480, 1265, 515, radius=10, fill="#FFFFFF", outline="")
    create_rounded_rectangle(canvas, 945, 560, 1265, 595, radius=10, fill="#FFFFFF", outline="")

    # Username entry
    username_entry = Entry(
        window,
        bg="#FFFFFF",
        font=("Sen", 14),
        highlightthickness=0,
        relief="flat",
    )
    username_entry.place(x=950, y=485, width=310, height=30)

    # Password entry
    password_entry = Entry(
        window,
        bg="#FFFFFF",
        font=("Sen", 14),
        show="*",
        highlightthickness=0,
        relief="flat",
    )
    password_entry.place(x=950, y=565, width=310, height=30)

    # Login button
    login_button = Button(
        window,
        text="Login",
        bg="#FFFFFF",
        font=("Sen Bold", 18),
        relief="flat",
        command=lambda: attempt_login(username_entry, password_entry, window),
    )
    login_button.place(x=1020, y=620, width=100, height=40)

    # "Forgot Password?" label
    forgot_password_label = Label(
        window,
        text="Forgot Password?",
        bg="#0B0C10",
        fg="#FFFFFF",
        font=("Sen Medium", 14),
        cursor="hand2",
    )
    forgot_password_label.place(x=1000, y=675)

    # Background image
    try:
        image_refs["image_4"] = PhotoImage(file=relative_to_assets("image_4.png"))
        canvas.create_image(403.0, 576.0, image=image_refs["image_4"])
    except Exception as e:
        print("Error loading image_4.png:", e)

    def on_resize(event):
        update_image(canvas, "image_1", file_path, event.width // 2)
    window.bind("<Configure>", on_resize)

if __name__ == "__main__":
    root = tk.Tk()
    create_ui(root)
    root.mainloop()
