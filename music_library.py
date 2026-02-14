import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "music_library.json"

library = []

# ---------------- FILE HANDLING ---------------- #

def load_library():
    global library
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            library = json.load(file)
            refresh_library()

def save_library():
    with open(FILE_NAME, "w") as file:
        json.dump(library, file, indent=4)

# ---------------- CORE FUNCTIONS ---------------- #

def add_song():
    title = title_entry.get()
    artist = artist_entry.get()
    album = album_entry.get()
    genre = genre_entry.get()

    if not title or not artist or not album or not genre:
        messagebox.showerror("Error", "All fields are required!")
        return

    song = {
        "title": title,
        "artist": artist,
        "album": album,
        "genre": genre
    }

    library.append(song)
    save_library()
    refresh_library()
    clear_fields()

    messagebox.showinfo("Success", "Song added successfully!")

def delete_song():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a song to delete!")
        return

    item = tree.item(selected[0])
    values = item["values"]

    for song in library:
        if (song["title"], song["artist"], song["album"], song["genre"]) == tuple(values):
            library.remove(song)
            break

    save_library()
    refresh_library()
    messagebox.showinfo("Deleted", "Song deleted successfully!")

def search_song():
    query = search_entry.get().lower()
    tree.delete(*tree.get_children())

    for song in library:
        if (query in song["title"].lower() or
            query in song["artist"].lower() or
            query in song["album"].lower() or
            query in song["genre"].lower()):
            
            tree.insert("", "end", values=(
                song["title"],
                song["artist"],
                song["album"],
                song["genre"]
            ))

def clear_fields():
    title_entry.delete(0, tk.END)
    artist_entry.delete(0, tk.END)
    album_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)

def refresh_library():
    tree.delete(*tree.get_children())
    for song in library:
        tree.insert("", "end", values=(
            song["title"],
            song["artist"],
            song["album"],
            song["genre"]
        ))

# ---------------- GUI SETUP ---------------- #

root = tk.Tk()
root.title("Music Library Organizer - Advanced")
root.geometry("750x500")
root.configure(bg="#f4f4f4")

title_label = tk.Label(root, text="🎵 Music Library Organizer", font=("Arial", 18, "bold"), bg="#f4f4f4")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#f4f4f4")
frame.pack(pady=10)

tk.Label(frame, text="Title:", bg="#f4f4f4").grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(frame)
title_entry.grid(row=0, column=1)

tk.Label(frame, text="Artist:", bg="#f4f4f4").grid(row=1, column=0, padx=5, pady=5)
artist_entry = tk.Entry(frame)
artist_entry.grid(row=1, column=1)

tk.Label(frame, text="Album:", bg="#f4f4f4").grid(row=2, column=0, padx=5, pady=5)
album_entry = tk.Entry(frame)
album_entry.grid(row=2, column=1)

tk.Label(frame, text="Genre:", bg="#f4f4f4").grid(row=3, column=0, padx=5, pady=5)
genre_entry = tk.Entry(frame)
genre_entry.grid(row=3, column=1)

button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Song", width=15, command=add_song, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Delete Song", width=15, command=delete_song, bg="#f44336", fg="white").grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Clear Fields", width=15, command=clear_fields).grid(row=0, column=2, padx=5)

# Search Section
search_frame = tk.Frame(root, bg="#f4f4f4")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search:", bg="#f4f4f4").grid(row=0, column=0, padx=5)
search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=5)

tk.Button(search_frame, text="Search", command=search_song).grid(row=0, column=2, padx=5)
tk.Button(search_frame, text="Show All", command=refresh_library).grid(row=0, column=3, padx=5)

# Table
tree = ttk.Treeview(root, columns=("Title", "Artist", "Album", "Genre"), show="headings")
tree.heading("Title", text="Title")
tree.heading("Artist", text="Artist")
tree.heading("Album", text="Album")
tree.heading("Genre", text="Genre")

tree.pack(fill="both", expand=True, padx=20, pady=20)

# Load existing data
load_library()

root.mainloop()
