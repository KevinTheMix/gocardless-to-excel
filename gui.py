import tkinter as tk

def on_click():
    label.config(text="Button clicked!")

# Create main window
root = tk.Tk()
root.title("My First GUI")
root.geometry("300x150")

# Add a label
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=10)

# Add a button
button = tk.Button(root, text="Click Me", command=on_click)
button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
