import tkinter as tk
from tkinter import filedialog
import os
import subprocess

# Global variable for language
current_language = "en"

# Language dictionary
translations = {
    "de": {
        "title": "S.T.A.L.K.E.R. 2 Pak GUI - by Schraenki",
        "unpack_section": "Unpack-Bereich",
        "selected_files": "Ausgewählte Dateien:",
        "add_file": "Pak hinzufügen",
        "clear_list": "Liste leeren",
        "unpack_button": "Archiv(e) entpacken",
        "pack_section": "Pack-Bereich",
        "folder_label": "Ordner für Packing:",
        "choose_folder": "Ordner wählen",
        "mod_name": "Mod-Name:",
        "use_folder_name": "Ordnername nutzen",
        "pack_button": "Pak erstellen",
        "hint": "Hinweis: Keine Leerzeichen in Dateinamen oder Ordnernamen verwenden.",
        "status_file_added": "Datei erfolgreich hinzugefügt.",
        "status_file_exists": "Fehler: Diese Datei ist bereits in der Liste.",
        "status_list_cleared": "Liste geleert.",
        "status_no_files": "Keine .pak-Dateien in der Liste.",
        "status_unpack_success": "Erfolgreich entpackt: {}",
        "status_unpack_error": "Fehler beim Entpacken von {}: {}",
        "status_invalid_file": "Ungültige Datei: {}",
        "status_unpack_done": "Bulk-Entpackvorgang abgeschlossen.",
        "status_folder_selected": "Ordner erfolgreich ausgewählt.",
        "status_folder_missing": "Fehler: Der Ordner muss einen Unterordner namens 'Stalker2' enthalten.",
        "status_invalid_folder": "Bitte wähle zuerst einen gültigen Ordner aus.",
        "status_pack_success": "Pack erfolgreich ausgeführt: {}",
        "status_pack_error": "Fehler beim Ausführen des Pack-Prozesses: {}",
        "status_modname_missing": "Bitte trage einen Modnamen ein.",
        "status_no_spaces": "Fehler: Keine Leerzeichen im Dateinamen oder Ordnernamen erlaubt.",
        "status_entry_delete_success": "Eintrag entfernt.",
        "status_entry_delete_failed": "Fehler beim Entfernen.",
    },
    "en": {
        "title": "S.T.A.L.K.E.R. 2 Pak GUI - by Schraenki",
        "unpack_section": "Unpack Section",
        "selected_files": "Selected Files:",
        "add_file": "Add Pak",
        "clear_list": "Clear List",
        "unpack_button": "Unpack Archive(s)",
        "pack_section": "Pack Section",
        "folder_label": "Folder for Packing:",
        "choose_folder": "Choose Folder",
        "mod_name": "Mod Name:",
        "use_folder_name": "Use Folder Name",
        "pack_button": "Create Pak",
        "hint": "Hint: Do not use spaces in file or folder names.",
        "status_file_added": "File successfully added.",
        "status_file_exists": "Error: This file is already in the list.",
        "status_list_cleared": "List cleared.",
        "status_no_files": "No .pak files in the list.",
        "status_unpack_success": "Successfully unpacked: {}",
        "status_unpack_error": "Error unpacking {}: {}",
        "status_invalid_file": "Invalid file: {}",
        "status_unpack_done": "Bulk unpack operation completed.",
        "status_folder_selected": "Folder successfully selected.",
        "status_folder_missing": "Error: Folder must contain a subfolder named 'Stalker2'.",
        "status_invalid_folder": "Please select a valid folder first.",
        "status_pack_success": "Pack successfully executed: {}",
        "status_pack_error": "Error executing pack process: {}",
        "status_modname_missing": "Please enter a mod name.",
        "status_no_spaces": "Error: No spaces allowed in filenames or folder names.",
        "status_entry_delete_success": "Entry deleted.",
        "status_entry_delete_failed": "Error deleting entry.",
    },
}

def update_language(language):
    global current_language
    current_language = language

    # Update all UI elements with translations
    root.title(translations[language]["title"])
    title_label.config(text="S.T.A.L.K.E.R. 2 Pak GUI")
    version_label.config(text="v1.3")
    hint_label.config(text=translations[language]["hint"])
    unpack_label.config(text=translations[language]["unpack_section"])
    selected_files_label.config(text=translations[language]["selected_files"])
    add_file_button.config(text=translations[language]["add_file"])
    clear_list_button.config(text=translations[language]["clear_list"])
    bulk_unpack_button.config(text=translations[language]["unpack_button"])
    pack_label.config(text=translations[language]["pack_section"])
    folder_label.config(text=translations[language]["folder_label"])
    browse_folder_button.config(text=translations[language]["choose_folder"])
    mod_name_label.config(text=translations[language]["mod_name"])
    use_folder_name_button.config(text=translations[language]["use_folder_name"])
    pack_button.config(text=translations[language]["pack_button"])

def select_multiple_pak_files():
    file_path = filedialog.askopenfilename(
        title="Select a .pak file",
        filetypes=[("PAK Files", "*.pak")],
        initialdir=os.getcwd()
    )
    if file_path:
        if " " in file_path:
            status_label.config(text=translations[current_language]["status_no_spaces"], fg="red")
        elif file_path in selected_files_listbox.get(0, tk.END):
            status_label.config(text=translations[current_language]["status_file_exists"], fg="red")
        else:
            selected_files_listbox.insert(tk.END, file_path)
            status_label.config(text=translations[current_language]["status_file_added"], fg="green")

def clear_selected_files():
    selected_files_listbox.delete(0, tk.END)
    status_label.config(text=translations[current_language]["status_list_cleared"], fg="blue")

def bulk_unpack_with_list():
    pak_files = selected_files_listbox.get(0, tk.END)
    if not pak_files:
        status_label.config(text=translations[current_language]["status_no_files"], fg="red")
        return

    for pak_file in pak_files:
        if os.path.isfile(pak_file):
            pak_name = os.path.basename(pak_file)
            output_folder = os.path.join(os.getcwd(), os.path.splitext(pak_name)[0])
            try:
                command = [
                    'repak',
                    '--aes-key', '0x33A604DF49A07FFD4A4C919962161F5C35A134D37EFA98DB37A34F6450D7D386',
                    'unpack', pak_file,
                    '-o', output_folder
                ]
                subprocess.run(command, check=True)
                status_label.config(
                    text=translations[current_language]["status_unpack_success"].format(pak_name), fg="green"
                )
            except subprocess.CalledProcessError as e:
                status_label.config(
                    text=translations[current_language]["status_unpack_error"].format(pak_name, e), fg="red"
                )
        else:
            status_label.config(
                text=translations[current_language]["status_invalid_file"].format(pak_file), fg="red"
            )

    status_label.config(text=translations[current_language]["status_unpack_done"], fg="blue")

def select_folder():
    folder_path = filedialog.askdirectory(
        title="Select a folder",
        initialdir=os.getcwd()
    )
    if folder_path:
        if " " in folder_path:
            status_label.config(text=translations[current_language]["status_no_spaces"], fg="red")
        else:
            entry_folder.delete(0, tk.END)
            entry_folder.insert(0, folder_path)
            if not os.path.exists(os.path.join(folder_path, "Stalker2")):
                status_label.config(text=translations[current_language]["status_folder_missing"], fg="red")
            else:
                status_label.config(text=translations[current_language]["status_folder_selected"], fg="green")

def use_folder_name_for_mod_name():
    folder_path = entry_folder.get()
    if folder_path and os.path.isdir(folder_path):
        folder_name = os.path.basename(folder_path)
        if folder_name.endswith("_P") or folder_name.endswith("_p"):
            folder_name = folder_name[:-2]
        entry_mod.delete(0, tk.END)
        entry_mod.insert(0, folder_name)
    else:
        status_label.config(
            text=translations[current_language]["status_invalid_folder"], fg="red"
        )

def create_and_run_pack():
    folder_path = entry_folder.get()
    mod_name = entry_mod.get().strip()

    if " " in folder_path:
        status_label.config(text=translations[current_language]["status_no_spaces"], fg="red")
        return

    if not os.path.exists(os.path.join(folder_path, "Stalker2")):
        status_label.config(text=translations[current_language]["status_folder_missing"], fg="red")
        return

    if not folder_path or not os.path.isdir(folder_path):
        status_label.config(text=translations[current_language]["status_invalid_folder"], fg="red")
        return

    if not mod_name:
        status_label.config(text=translations[current_language]["status_modname_missing"], fg="red")
        return

    mod_name_with_p = f"{mod_name}_P"

    try:
        command = f'repak.exe pack --version V11 {folder_path}/ {mod_name_with_p}.pak'
        subprocess.run(command, check=True, shell=True)
        status_label.config(text=translations[current_language]["status_pack_success"].format(mod_name_with_p), fg="green")
    except subprocess.CalledProcessError as e:
        status_label.config(text=translations[current_language]["status_pack_error"].format(e), fg="red")

# Neue Funktion für das Löschen mit der Delete-Taste
def delete_selected_item(event):
    try:
        selected_index = selected_files_listbox.curselection()
        if selected_index:
            selected_files_listbox.delete(selected_index)
            status_label.config(text=translations[current_language]["status_entry_delete_success"], fg="blue")
    except Exception as e:
        status_label.config(text=translations[current_language]["status_entry_delete_failed"], fg="red")

# GUI erstellen
root = tk.Tk()
root.title(translations["en"]["title"])
root.configure(bg="lightgray")

frame = tk.Frame(root, padx=10, pady=10, bg="lightgray")
frame.pack(padx=10, pady=10, anchor="w")

highlight_color = "#1c3f52"

# Header
header_frame = tk.Frame(frame, bg="lightgray")
header_frame.grid(row=0, column=0, columnspan=2, sticky="w")
title_label = tk.Label(
    header_frame,
    text="S.T.A.L.K.E.R. 2 Pak GUI",
    font=("Helvetica", 14, "bold"),
    bg="lightgray",
    fg=highlight_color
)
title_label.grid(row=0, column=0, sticky="w")
version_label = tk.Label(
    header_frame,
    text="v1.3",
    font=("Helvetica", 10),
    bg="lightgray",
    fg="gray"
)
version_label.grid(row=0, column=1, padx=(5, 0), sticky="w")

# Hinweis
hint_label = tk.Label(frame, text=translations["en"]["hint"], bg="lightgray", fg="red")
hint_label.grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="w")

# Language Switcher
language_switcher = tk.Frame(frame, bg="lightgray")
language_switcher.grid(row=0, column=1, sticky="e")
tk.Button(language_switcher, text="Deutsch", bg="white", command=lambda: update_language("de")).pack(side="left", padx=5)
tk.Button(language_switcher, text="English", bg="white", command=lambda: update_language("en")).pack(side="left")

# Unpack Section
unpack_label = tk.Label(frame, text=translations["en"]["unpack_section"], font=("Arial", 12), bg="lightgray")
unpack_label.grid(row=2, column=0, columnspan=2, pady=(10, 5), sticky="w")
selected_files_label = tk.Label(frame, text=translations["en"]["selected_files"], bg="lightgray")
selected_files_label.grid(row=3, column=0, columnspan=2, sticky="w")
selected_files_listbox = tk.Listbox(frame, width=50, height=5)
selected_files_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
selected_files_listbox.bind("<Delete>", delete_selected_item)  # Bind der Delete-Taste
add_file_button = tk.Button(frame, text=translations["en"]["add_file"], bg="white", command=select_multiple_pak_files)
add_file_button.grid(row=5, column=0, sticky="w", padx=5, pady=5)
clear_list_button = tk.Button(frame, text=translations["en"]["clear_list"], bg="white", command=clear_selected_files)
clear_list_button.grid(row=5, column=1, sticky="w", padx=5, pady=5)
bulk_unpack_button = tk.Button(
    frame,
    text=translations["en"]["unpack_button"],
    bg=highlight_color,
    fg="white",
    font=("Helvetica", 10, "bold"),
    command=bulk_unpack_with_list
)
bulk_unpack_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="w")

# Pack Section
pack_label = tk.Label(frame, text=translations["en"]["pack_section"], font=("Arial", 12), bg="lightgray")
pack_label.grid(row=7, column=0, columnspan=2, pady=(20, 5), sticky="w")
folder_label = tk.Label(frame, text=translations["en"]["folder_label"], bg="lightgray")
folder_label.grid(row=8, column=0, sticky="w")
entry_folder = tk.Entry(frame, width=50)
entry_folder.grid(row=9, column=0, padx=5, pady=5, sticky="w")
browse_folder_button = tk.Button(frame, text=translations["en"]["choose_folder"], bg="white", command=select_folder)
browse_folder_button.grid(row=9, column=1, padx=5, pady=5, sticky="w")
mod_name_label = tk.Label(frame, text=translations["en"]["mod_name"], bg="lightgray")
mod_name_label.grid(row=10, column=0, sticky="w")
mod_name_frame = tk.Frame(frame, bg="lightgray")
mod_name_frame.grid(row=11, column=0, columnspan=2, sticky="w")
entry_mod = tk.Entry(mod_name_frame, width=40)
entry_mod.pack(side="left", padx=(0, 2))
tk.Label(mod_name_frame, text="_P", bg="lightgray", font=("Arial", 10)).pack(side="left")
use_folder_name_button = tk.Button(frame, text=translations["en"]["use_folder_name"], bg="white", command=use_folder_name_for_mod_name)
use_folder_name_button.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky="w")
pack_button = tk.Button(
    frame,
    text=translations["en"]["pack_button"],
    bg=highlight_color,
    fg="white",
    font=("Helvetica", 10, "bold"),
    command=create_and_run_pack
)
pack_button.grid(row=13, column=0, columnspan=2, pady=20, sticky="w")

# Status Label
status_label = tk.Label(frame, text="", fg="blue", bg="lightgray")
status_label.grid(row=14, column=0, columnspan=2, sticky="w")

root.mainloop()
