import os
import shutil
import tkinter.messagebox as messagebox
from tkinter import Tk, simpledialog

def progress_percentage(perc, width=None):
    #credit: https://stackoverflow.com/questions/29967487/get-progress-back-from-shutil-file-copy-thread/48450305#48450305
    # This will only work for python 3.3+ due to use of
    # os.get_terminal_size the print function etc.

    FULL_BLOCK = '█'
    # this is a gradient of incompleteness
    INCOMPLETE_BLOCK_GRAD = ['░', '▒', '▓']

    assert(isinstance(perc, float))
    assert(0. <= perc <= 100.)
    # if width unset use full terminal
    if width is None:
        width = os.get_terminal_size().columns
    # progress bar is block_widget separator perc_widget : ####### 30%
    max_perc_widget = '[100.00%]' # 100% is max
    separator = ' '
    blocks_widget_width = width - len(separator) - len(max_perc_widget)
    assert(blocks_widget_width >= 10) # not very meaningful if not
    perc_per_block = 100.0/blocks_widget_width
    # epsilon is the sensitivity of rendering a gradient block
    epsilon = 1e-6
    # number of blocks that should be represented as complete
    full_blocks = int((perc + epsilon)/perc_per_block)
    # the rest are "incomplete"
    empty_blocks = blocks_widget_width - full_blocks

    # build blocks widget
    blocks_widget = ([FULL_BLOCK] * full_blocks)
    blocks_widget.extend([INCOMPLETE_BLOCK_GRAD[0]] * empty_blocks)
    # marginal case - remainder due to how granular our blocks are
    remainder = perc - full_blocks*perc_per_block
    # epsilon needed for rounding errors (check would be != 0.)
    # based on reminder modify first empty block shading
    # depending on remainder
    if remainder > epsilon:
        grad_index = int((len(INCOMPLETE_BLOCK_GRAD) * remainder)/perc_per_block)
        blocks_widget[full_blocks] = INCOMPLETE_BLOCK_GRAD[grad_index]

    # build perc widget
    str_perc = '%.2f' % perc
    # -1 because the percentage sign is not included
    perc_widget = '[%s%%]' % str_perc.ljust(len(max_perc_widget) - 3)

    # form progressbar
    progress_bar = '%s%s%s' % (''.join(blocks_widget), separator, perc_widget)
    # return progressbar as string
    return ''.join(progress_bar)


def copy_progress(copied, total):
    print('\r' + progress_percentage(100*copied/total, width=30), end='')


def copyfile(src, dst, *, follow_symlinks=True):
    """Copy data from src to dst.

    If follow_symlinks is not set and src is a symbolic link, a new
    symlink will be created instead of copying the file it points to.

    """
    if shutil._samefile(src, dst):
        raise shutil.SameFileError("{!r} and {!r} are the same file".format(src, dst))

    for fn in [src, dst]:
        try:
            st = os.stat(fn)
        except OSError:
            # File most likely does not exist
            pass
        else:
            # XXX What about other special files? (sockets, devices...)
            if shutil.stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError("`%s` is a named pipe" % fn)

    if not follow_symlinks and os.path.islink(src):
        os.symlink(os.readlink(src), dst)
    else:
        size = os.stat(src).st_size
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                copyfileobj(fsrc, fdst, callback=copy_progress, total=size)
    return dst


def copyfileobj(fsrc, fdst, callback, total, length=16*1024):
    copied = 0
    while True:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
        copied += len(buf)
        callback(copied, total=total)


def copy_with_progress(src, dst, *, follow_symlinks=True):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    copyfile(src, dst, follow_symlinks=follow_symlinks)
    shutil.copymode(src, dst)
    return dst

def ingest_folder():
    # Move the destination folder to finalDst_path
    dst_path_ingest = os.path.join(finalDst_path, dst_name)
    shutil.move(dst_path, dst_path_ingest)
    print("/n")
    messagebox.showinfo(title="Ingest Complete", message="The folder has been moved to "+dst_path_ingest)
    root.destroy()
    exit()

# Set the fixed source and destination paths
src_path = "F:\\Clip"
dst_path = "N:\\VANTAGE\\File_Ingest"
finalDst_path = "N:\\VANTAGE\\File_Ingest\\FILE"

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

# Copy all .MXF files from the source folder to the destination folder
file_count = 1
for file_name in os.listdir(src_path):
    if file_name.endswith(".MXF"):
        src_file = os.path.join(src_path, file_name)
        dst_file = os.path.join(dst_path, file_name)
        print(str(file_name) + " | " + str(file_count) + "/" + str(len([file for file in os.listdir(src_path) if file.endswith('.MXF')])))
        copy_with_progress(src_file, dst_file)
        print(f" {file_name} Copied!")
        file_count += 1

ingest_folder()
# root.deiconify()
# answer = messagebox.askyesno(title="Copy Complete", message="Copy Complete. Ingest?")
# if answer:
#     ingest_folder()