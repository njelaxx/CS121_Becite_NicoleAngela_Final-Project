
# Shelf Life: Digital Bookstore Assistant

## I. Project Overview

This project is a comprehensive Shelf Life: Digital Bookstore Assistant developed using Python and Tkinter. The system provides functionalities for managing books, placing orders, and generating sales reports. Additionally, it includes an admin authentication system to ensure secure access to the management dashboard.

The primary goal of this project is to automate and streamline the process of book inventory management, order placement, and sales reporting, helping businesses improve efficiency and accuracy.

## II. Explanation of Python Concepts, Libraries, and Frameworks Applied

1. **Tkinter**: 
   - Tkinter is used for building the graphical user interface (GUI). It provides various widgets such as buttons, entry fields, labels, and canvases to design an interactive interface.

2. **SQLite**:
   - SQLite is used for database management. The project uses SQLite to store and retrieve information about books, orders, and sales reports.
   - Tables are created for storing data related to books, orders, sales reports, and admins. 

3. **Pillow**:
   - Pillow is used for handling and resizing images within the Tkinter application. Images are used for UI elements like backgrounds and icons.

4. **JSON**:
   - JSON is used to store admin credentials for authentication. The file `admins.json` is used to validate admin login attempts.

5. **Functions and Classes**:
   - The project organizes code into functions that handle different tasks such as adding books, updating stock, placing orders, generating sales reports, and handling admin logins.

## III. Details of the Chosen SDG (Sustainable Development Goal) and Its Integration into the Project

This project indirectly supports **SDG 12: Responsible Consumption and Production** by promoting efficient and responsible management of resources within a business. It helps businesses keep track of inventory (books) and sales, ensuring that stock is managed properly and reducing waste.

By streamlining the order and inventory processes, businesses can make more informed decisions about production and sales, avoiding overproduction or underproduction and reducing environmental impact.

## IV. Instructions for Running the Program

### Prerequisites:
1. **Python 3.x** installed on your machine.
2. **Libraries**: The following Python libraries need to be installed:
   - `Tkinter`: for building the GUI.
   - `SQLite`: for database management (included in Python's standard library).
   - `Pillow`: for handling images (install via `pip install pillow`).

### Setup:

1. Clone or download the repository to your local machine.
2. Navigate to the project directory.

### Running the Program:

1. Ensure the required Python libraries are installed.
2. Execute the following command in the terminal or command prompt to start the application:
   ```bash
   python main.py
   ```

### Notes on Images and Asset Paths

In this project, images are used within the graphical user interface (GUI) and can be modified according to your needs. To ensure that images are displayed correctly, the paths to the image files should be properly set up. The following points should be considered when working with images and assets:

1. **Image Files**:
   - The project uses image files for elements like the login page background and other UI components.
   - Ensure that the image files (e.g., `background.jpg`) are placed in a directory accessible to the program.
   - It is recommended to create an `assets` folder in the project directory to store all image files, ensuring proper organization.

2. **File Path**:
   - Paths to image files must be correct to avoid errors. In the provided code, images are loaded using relative paths. For example, the code might look like this:

   ```python
   img = PhotoImage(file="assets/login_background.png")
   ```

   If you place your image files in a subdirectory like `assets`, make sure the relative path reflects that directory structure. Example:

   ```python
   img = PhotoImage(file="assets/backgrounds/login_background.png")
   ```

3. **Supported Image Formats**:
   - The code is set to support standard image formats such as PNG, JPG, or JPEG. You can add more formats as needed, but ensure that the format is compatible with **Pillow**.
   
4. **Image Size**:
   - Images should be resized appropriately for the GUI. If an image is too large or too small, it might not appear correctly. You can resize images using **Pillow** to fit your desired dimensions. For example:

   ```python
   img = Image.open("assets/login_background.png")
   img = img.resize((400, 300))  # Resize the image to 400x300 pixels
   img = ImageTk.PhotoImage(img)  # Convert to a format Tkinter understands
   ```

5. **Missing Assets**:
   - If any image or asset file is missing or not found, Tkinter will raise an error. Make sure all necessary files are present before running the program.

6. **Alternative Asset Paths**:
   - If you are planning to run this code on different systems or environments (e.g., Windows, macOS, Linux), you may want to consider using absolute paths, especially when working with file storage. However, relative paths are preferred for portability in most cases.

### Example Folder Structure:
```
/ShelfLife
    /assets
        /backgrounds
            login_background.png
        /icons
            book_icon.png
    main.py
    books.db
    README.md
```

---


