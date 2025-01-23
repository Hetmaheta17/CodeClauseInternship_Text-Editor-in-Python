import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk


class InteractiveTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Text Editor")
        self.root.geometry("800x600")

        # Initialize variables
        self.file_path = None

        # Apply theme
        self.style = ttk.Style()
        self.style.theme_use("radiance")  # Choose a theme

        # Create UI components
        self.create_menu()
        self.create_toolbar()
        self.create_text_area()
        self.create_status_bar()

    def create_menu(self):
        # Menu bar
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

    def create_toolbar(self):
        # Toolbar frame
        self.toolbar = ttk.Frame(self.root, padding=2)
        self.toolbar.pack(side="top", fill="x")

        # Toolbar buttons
        ttk.Button(self.toolbar, text="New", command=self.new_file).pack(side="left", padx=2)
        ttk.Button(self.toolbar, text="Open", command=self.open_file).pack(side="left", padx=2)
        ttk.Button(self.toolbar, text="Save", command=self.save_file).pack(side="left", padx=2)
        ttk.Button(self.toolbar, text="Word Count", command=self.show_word_count).pack(side="left", padx=2)

    def create_text_area(self):
        # Text area
        self.text_area = tk.Text(self.root, wrap="word", undo=True, font=("Arial", 12))
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.text_area, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

    def create_status_bar(self):
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

        # Update cursor position
        self.text_area.bind("<KeyRelease>", self.update_status_bar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.status_bar.config(text="New File")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
            self.file_path = file_path
            self.status_bar.config(text=f"Opened: {file_path}")

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END).strip())
            self.status_bar.config(text=f"Saved: {self.file_path}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END).strip())
            self.file_path = file_path
            self.status_bar.config(text=f"Saved: {file_path}")

    def show_word_count(self):
        text = self.text_area.get(1.0, tk.END).strip()
        word_count = len(text.split())
        messagebox.showinfo("Word Count", f"Total Words: {word_count}")

    def update_status_bar(self, event=None):
        row, col = self.text_area.index(tk.INSERT).split(".")
        self.status_bar.config(text=f"Line {row}, Column {col}")

    def show_about(self):
        messagebox.showinfo("About", "Interactive Text Editor\nDeveloped with Python and Tkinter.")


if __name__ == "__main__":
    root = ThemedTk()  # Use ThemedTk for enhanced UI
    editor = InteractiveTextEditor(root)
    root.mainloop()
