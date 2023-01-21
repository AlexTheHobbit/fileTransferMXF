import os
import shutil
import tkinter.messagebox as messagebox
from tkinter import Tk, simpledialog

# Set the fixed source and destination paths
src_path = "F:\\Clip"
dst_path = "N:\\VANTAGE\\File_Ingest"

# Get the destination folder name from the user
root = Tk()
root.withdraw()
dst_name = simpledialog.askstring(title="Destination Folder", prompt="Enter the name of the destination folder:")

# Create the destination folder path
dst_path = os.path.join(dst_path, dst_name)

# Check if the destination folder already exists
if os.path.exists(dst_path):
    # Ask the user if they want to overwrite the files
    answer = messagebox.askyesno(title="Destination Folder Exists", message="The destination folder already exists. Do you want to overwrite the files in it?")
    if not answer:
        messagebox.showinfo(title="Copy Aborted", message="The copy operation has been cancelled.")
        root.deiconify()
        root.destroy()
        exit()
else:
    # Create the destination folder
    os.mkdir(dst_path)

# Copy all .mxf files from the source folder to the destination folder
for file_name in os.listdir(src_path):
    if file_name.endswith(".MXF"):
        src_file = os.path.join(src_path, file_name)
        dst_file = os.path.join(dst_path, file_name)
        shutil.copy(src_file, dst_file)

def ingest_folder():
    # Move the destination folder to "N:\VANTAGE\File_Ingest\FILE"
    dst_path_ingest = os.path.join("N:\\VANTAGE\\File_Ingest\\FILE", dst_name)
    shutil.move(dst_path, dst_path_ingest)
    messagebox.showinfo(title="Ingest Complete", message="The folder has been moved to "+dst_path_ingest)
    root.destroy()
    exit()

ingest_folder()
# root.deiconify()
# answer = messagebox.askyesno(title="Copy Complete", message="Copy Complete. Ingest?")
# if answer:
#     ingest_folder()