import os
import zipfile
import tkinter as tk
from tkinter import simpledialog, messagebox, Button, Label

appdata_path = os.getenv('APPDATA')
sekiro_path = os.path.join(appdata_path, 'SEKIRO') if appdata_path else None
first_folder = next((f for f in os.listdir(sekiro_path) if os.path.isdir(os.path.join(sekiro_path, f))), None)
first_folder_path = os.path.join(sekiro_path, first_folder)

def create_gui():
    def run_backup():
        if sekiro_path and os.path.exists(sekiro_path):
            if first_folder:
                sl2_or_bak_files = [f for f in os.listdir(first_folder_path) if f.endswith(('.sl2', '.bak'))]
                if sl2_or_bak_files:
                    root = tk.Tk()
                    root.withdraw()  # Hide the root window
                    while True:
                        zip_name = simpledialog.askstring("Input", "Enter the name for the backup zip file (without extension):")
                        if not zip_name:
                            break
                        zip_path = os.path.join(first_folder_path, f"{zip_name}.zip")
                        if os.path.exists(zip_path):
                            messagebox.showwarning("Warning", f"A zip file with the name '{zip_name}.zip' already exists. Please choose a different name.")
                        else:
                            break
                    if zip_name:
                        zip_path = os.path.join(first_folder_path, f"{zip_name}.zip")
                        with zipfile.ZipFile(zip_path, 'w') as zipf:
                            for file in sl2_or_bak_files:
                                file_path = os.path.join(first_folder_path, file)
                                zipf.write(file_path, arcname=file)
                        messagebox.showinfo("Success", f"Files zipped into: {zip_path}")
                    else:
                        messagebox.showwarning("Cancelled", "Backup operation cancelled.")
                else:
                    messagebox.showinfo("Info", "No .sl2 or .bak files found in the folder.")
            else:
                messagebox.showinfo("Info", "No folders found in the SEKIRO directory.")
        else:
            messagebox.showerror("Error", "SEKIRO folder not found or APPDATA environment variable not set.")

    def open_folder():
        appdata_path = os.getenv('APPDATA')
        sekiro_path = os.path.join(appdata_path, 'SEKIRO') if appdata_path else None
        if sekiro_path and os.path.exists(sekiro_path):
            first_folder = next((f for f in os.listdir(sekiro_path) if os.path.isdir(os.path.join(sekiro_path, f))), None)
            if first_folder:
                first_folder_path = os.path.join(sekiro_path, first_folder)
                os.startfile(first_folder_path)
            else:
                messagebox.showinfo("Info", "No folders found in the SEKIRO directory.")
        else:
            messagebox.showerror("Error", "SEKIRO folder not found or APPDATA environment variable not set.")

    def unzip_backup():
        if first_folder_path and os.path.exists(first_folder_path):
            zip_files = [f for f in os.listdir(first_folder_path) if f.endswith('.zip')]
            if zip_files:
                def on_select(event):
                    selected_zip = listbox.get(listbox.curselection())
                    if selected_zip:
                        zip_file_path = os.path.join(first_folder_path, selected_zip)
                        try:
                            with zipfile.ZipFile(zip_file_path, 'r') as zipf:
                                zipf.extractall(first_folder_path)
                            messagebox.showinfo("Success", f"Files extracted to: {first_folder_path}")
                        except zipfile.BadZipFile:
                            messagebox.showerror("Error", f"The file '{selected_zip}' is not a valid zip file.")
                        unzip_window.destroy()

                unzip_window = tk.Toplevel()
                unzip_window.title("Select Zip File to restore")
                unzip_window.geometry("300x200")

                label = Label(unzip_window, text="Select a zip file to unzip:")
                label.pack(pady=10)

                listbox = tk.Listbox(unzip_window)
                for zip_file in zip_files:
                    listbox.insert(tk.END, zip_file)
                listbox.pack(pady=10, fill=tk.BOTH, expand=True)

                listbox.bind("<<ListboxSelect>>", on_select)

                close_button = Button(unzip_window, text="Close", command=unzip_window.destroy)
                close_button.pack(pady=10)
            else:
                messagebox.showinfo("Info", "No zip files found in the folder.")
        else:
            messagebox.showerror("Error", "Save folder not found or invalid.")

    root = tk.Tk()
    root.title("Sekiro Save Backup")
    root.geometry("400x250")

    description = Label(root, text="This GUI will create a backup of Sekiro save filesand allow one to restore these backups as well.", wraplength=350, justify="center")
    description.pack(pady=20)

    backup_button = Button(root, text="Create Backup", command=run_backup)
    backup_button.pack(pady=10)

    open_folder_button = Button(root, text="Open Save Folder", command=open_folder)
    open_folder_button.pack(pady=10)

    unzip_button = Button(root, text="Restore Backup", command=unzip_backup)
    unzip_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()