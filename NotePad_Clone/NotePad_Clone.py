from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

#root 
root = tk.Tk()
root.title("Notepad Clone")
root.geometry("450x450")
root.minsize(450,450)
root.maxsize(1200,700)

#styles
stylerOne = ttk.Style()
stylerOne.configure("topFrame.TFrame", background = "red",padding = "5px")
stylerOne.configure("mainFrame.TFrame", background = "white",padding = "5px")
stylerOne.configure("bottomFrame.TFrame", background = "turquoise1",padding = "5px")
stylerOne.configure("mainOneFrame.TFrame", background = "green", padding = "5px")
stylerOne.configure("mainTwoFrame.TFrame", background = "grey")

#frames, label, menubar
menuBar = tk.Menu(root)
root.config(menu = menuBar)

bottomFrame = ttk.Frame(root, height=25,width=1200)
bottomFrame.pack_propagate(False)
bottomFrame.pack(side="bottom", fill='x')

mainFrame = ttk.Frame(root, width=1200, style = "mainFrame.TFrame")
mainFrame.pack_propagate(False)
mainFrame.pack(side="left",fill='both',padx =5,pady=5)

mainTwoFrame = tk.Text(mainFrame,undo=True, maxundo=5)
mainTwoFrame.pack_propagate(False)
mainTwoFrame.pack(side="right",fill = 'both',padx = "2.5px 5px",expand = True)

bottomRightLabel = ttk.Label(bottomFrame,text = "Chars: 0")
bottomRightLabel.pack(side = "right")

bottomMiddleLabel = ttk.Label(bottomFrame,text = "File: New")
bottomMiddleLabel.pack(side="right", padx=20)

#function for number of character
def get_Char_Len(event = None):
    context_len = mainTwoFrame.get(1.0, tk.END)
    character_count = len(context_len) - 1
    bottomRightLabel.config(text = f"Char:{character_count}")

#function for opening a file
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            mainTwoFrame.delete(1.0, tk.END)
            mainTwoFrame.insert(tk.END, content)
            get_Char_Len()
            all_file_chars = file_path.split('/')
            file_name = (all_file_chars[-1].split('.'))[-2]
            bottomMiddleLabel.config(text=f"File:{file_name}")
        except Exception as e:
            messagebox.showerror("Error", "Error opening file")

#function for saving file
def save_as_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files (.txt)", "*.txt")])
    if file_path:
        if not file_path.endswith(".txt"):
            messagebox.showerror("Invalid Extension", "Please save the file with a .txt extension.")
            return
        try:
            content = mainTwoFrame.get(1.0, tk.END)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
        except Exception as e:
            messagebox.showerror("Error", "Error Saving File")

#function for copy                
def copy_text():
    mainTwoFrame.event_generate("<<Copy>>")

#function for cut   
def cut_text():
    mainTwoFrame.event_generate("<<Cut>>")

#function for paste
def paste_text(event=None):
    mainTwoFrame.event_generate("<<Paste>>")

#function for undo
def undo_move():
    try:
        mainTwoFrame.edit_undo()
    except TclError:
        messagebox.showinfo("Undo limit exceeded", "Undo stack is empty")

#function for redo
def redo_move():
    try:
        mainTwoFrame.edit_redo()
    except TclError:
        messagebox.showinfo("Redo limit exceeded", "Redo stack is empty")

mainTwoFrame.bind("<KeyRelease>",get_Char_Len)
mainTwoFrame.bind("<Control-z>",undo_move)

#Create a File menu and add items
file_menu = tk.Menu(menuBar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save As", command = save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menuBar.add_cascade(label="File", menu=file_menu)

# Create an Edit menu and add items
edit_menu = tk.Menu(menuBar, tearoff=0)
edit_menu.add_command(label="Undo",command= undo_move)
edit_menu.add_command(label="Redo",command = redo_move)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command = cut_text)
edit_menu.add_command(label="Copy", command = copy_text)
edit_menu.add_command(label="Paste", command = paste_text)
menuBar.add_cascade(label="Edit", menu=edit_menu)

# Create a Help menu and add items
help_menu = Menu(menuBar, tearoff=0)
help_menu.add_command(label="About")
menuBar.add_cascade(label="Help", menu=help_menu)

#function for changing font and size
def font_And_Size():

    def apply_font():
        selectedFont = fontDropBox.get()
        selectedSize = sizeDropBox.get()
        mainTwoFrame.config(font =(selectedFont,selectedSize))

    fontAndSize = tk.Toplevel()
    fontAndSize.title("Font & Size")
    fontAndSize.geometry('300x200')

    fontLabel = tk.Label(fontAndSize, text = "Font Type:")
    fontLabel.pack()
    fontDropBox = ttk.Combobox(fontAndSize, values = ["Helvetica", "Castellar", "Elephant", "Rockwell", "Verdana"])
    fontDropBox.pack()
    sizeLabel = tk.Label(fontAndSize, text = "Size Type:")
    sizeLabel.pack()
    sizeDropBox = ttk.Combobox(fontAndSize, values = ["12", "14", "16", "18", "20"])
    sizeDropBox.pack()

    apply_button = tk.Button(fontAndSize, text="Apply", command=apply_font)
    apply_button.pack()

#button
settingButton = Menubutton(bottomFrame,text = "Settings",direction="above",indicatoron=False)
settingButton.pack(side = "left")

#menu
settingMenu = tk.Menu(settingButton, tearoff=0)

settingButton["menu"] = settingMenu

settingMenu.add_command(label="Fonts & Size", command = font_And_Size)

#app will stop after this
root.mainloop()