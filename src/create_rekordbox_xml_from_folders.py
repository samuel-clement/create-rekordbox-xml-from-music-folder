import xml.etree.ElementTree as ET
import os
import hashlib
from mutagen import File
from mutagen.mp3 import HeaderNotFoundError
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

def create_rekordbox_xml(root_path, output_path, progress_var):
    """Generates Rekordbox XML from the provided root path and updates progress_var."""
    dj_playlists = ET.Element("DJ_PLAYLISTS", Version="1.0.0")
    ET.SubElement(dj_playlists, "PRODUCT", Name="rekordbox", Version="7.0.4", Company="AlphaTheta")
    collection = ET.SubElement(dj_playlists, "COLLECTION", Entries="0")
    playlists = ET.SubElement(dj_playlists, "PLAYLISTS")
    root_playlist_node = ET.SubElement(playlists, "NODE", Type="0", Name="ROOT", Count="0")

    track_id = 1
    file_names = {}
    total_tracks = 0
    playlist_count = 0

    def add_track_to_collection(track_path):
        nonlocal track_id, total_tracks
        track_name = os.path.basename(track_path)
        if track_name not in file_names:
            artist, album = "Unknown Artist", "Unknown Album"
            try:
                audio_file = File(track_path)
                if audio_file and audio_file.tags:
                    artist = audio_file.tags.get('TPE1', ["Unknown Artist"])[0]
                    album = audio_file.tags.get('TALB', ["Unknown Album"])[0]
            except (HeaderNotFoundError, Exception):
                return None  # Skip unreadable files
            track_element = ET.SubElement(
                collection, "TRACK",
                TrackID=str(track_id),
                Name=track_name,
                Artist=artist,
                Album=album,
                Location=f"file://localhost/{track_path.replace(os.sep, '/')}"
            )
            file_names[track_name] = track_id
            track_id += 1
            total_tracks += 1
        return file_names[track_name]

    def add_playlist(folder_path):
        nonlocal playlist_count
        playlist_name = os.path.basename(folder_path)
        playlist_node = ET.SubElement(root_playlist_node, "NODE", Name=playlist_name, Type="1", KeyType="0", Entries="0")
        entries_count = 0
        for filename in os.listdir(folder_path):
            if filename.endswith(('.mp3', '.wav', '.flac', '.aac')):
                track_path = os.path.join(folder_path, filename)
                track_id_ref = add_track_to_collection(track_path)
                if track_id_ref:
                    ET.SubElement(playlist_node, "TRACK", Key=str(track_id_ref))
                    entries_count += 1
        playlist_node.set("Entries", str(entries_count))
        playlist_count += 1
        # Update progress
        progress_var.set(f"Creating playlist {playlist_count}...")

    for folder_name in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder_name)
        if os.path.isdir(folder_path):
            add_playlist(folder_path)

    collection.set("Entries", str(len(file_names)))
    root_playlist_node.set("Count", str(playlist_count))
    tree = ET.ElementTree(dj_playlists)
    tree.write(output_path, encoding="UTF-8", xml_declaration=True)

    progress_var.set("XML creation complete!")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

def select_output_file():
    output_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
    if output_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)

def run_script():
    folder_path = folder_entry.get()
    output_path = output_entry.get()
    if not folder_path or not output_path:
        messagebox.showwarning("Missing Information", "Please select both the folder path and output file path.")
        return
    progress_var.set("Starting XML generation...")
    generate_button.config(state=tk.DISABLED)

    # Run XML creation in a separate thread to keep the UI responsive
    threading.Thread(target=create_rekordbox_xml, args=(folder_path, output_path, progress_var)).start()

# Set up the main GUI window
app = tk.Tk()
app.title("Rekordbox Playlist XML Generator")

progress_var = tk.StringVar()

tk.Label(app, text="Select Playlist Folder Path:").pack(pady=5)
folder_entry = tk.Entry(app, width=50)
folder_entry.pack(padx=10)
tk.Button(app, text="Browse", command=select_folder).pack(pady=5)

tk.Label(app, text="Select Output XML File Path:").pack(pady=5)
output_entry = tk.Entry(app, width=50)
output_entry.pack(padx=10)
tk.Button(app, text="Browse", command=select_output_file).pack(pady=5)

generate_button = tk.Button(app, text="Generate XML", command=run_script)
generate_button.pack(pady=20)

progress_label = tk.Label(app, textvariable=progress_var, fg="blue")
progress_label.pack()

app.mainloop()
