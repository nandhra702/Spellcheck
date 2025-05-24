import subprocess
from tkinter import *

def get_suggestions(mode, word):
    try:
        result = subprocess.run(
            ["./executable", mode, word],
            capture_output=True,
            text=True
        )
        return result.stdout.strip().split('\n') if result.stdout else []
    except Exception as e:
        return []

def get_current_word():
    text = textbox.get("1.0", END).strip()
    words = text.split()
    return words[-1] if words else ""

def update_autocomplete_suggestions(word):
    if not word:
        listbox.delete(0, END)
        return
    suggestions = get_suggestions("autocomplete", word)
    listbox.delete(0, END)
    for suggestion in suggestions:
        listbox.insert(END, suggestion)

def on_key_release(event):
    word = get_current_word()
    update_autocomplete_suggestions(word)

def on_space(event):
    # Check the last word
    word = get_current_word()
    if not word:
        return
    suggestions = get_suggestions("spellcheck", word)
    if word not in suggestions:
        underline_last_word(word)

def underline_last_word(word):
    textbox.tag_remove("misspelled", "1.0", END)
    text = textbox.get("1.0", END).strip()
    index = text.rfind(word)
    if index != -1:
        start = f"1.{index}"
        end = f"1.{index + len(word)}"
        textbox.tag_add("misspelled", start, end)
        textbox.tag_config("misspelled", underline=True, foreground="red")

# UI setup
root = Tk()
root.title("Centered trial 1")
root.geometry("400x300")

# Heading
heading = Label(
    root,
    text="My First try at a notepad with autocomplete suggestions",
    font=("Helvetica", 19),
    fg="black",
    bg="white"
)
heading.pack(padx=20, pady=(30, 10))

# Textbox
textbox = Text(
    root,
    width=80,
    height=10,
    fg="black",
    bg="lightblue"
)
textbox.pack(padx=30, pady=(10, 5))
textbox.bind("<KeyRelease>", on_key_release)
textbox.bind("<space>", on_space)

# Listbox for autocomplete suggestions
listbox = Listbox(root, height=4)
listbox.pack(padx=30, pady=(0, 10))

root.mainloop()
