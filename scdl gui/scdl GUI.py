import tkinter as tk
from tkinter import filedialog
import subprocess
import time
from urllib.request import urlopen
from re import *
from sqlite3 import *

# main window & db
root = tk.Tk()
root.resizable(False, False)
root.title("scdl gui")
root.geometry('600x400')
root.title('scdl gui')
root.configure(bg='#f4f5f0')
connection = connect("scdl.db")
scdl_db = connection.cursor()


def add_to_database():
    #connection.open()
    #scdl_db.open()
    scsource = urlopen(link_entry.get()).read().decode("UTF-8")
    match_artist = findall('<meta name=.*? by (.*?) on desktop', scsource)
    match_title = findall('<title>Stream (.*?) by .*?</title>', scsource)
    sql = 'INSERT INTO downloaded_songs (date, artist, title, link, location) VALUES (?, ?, ?, ?, ?)'
    scdl_db.execute(sql, (time.strftime("%Y-%m-%d"), match_artist[0], match_title[0], link_entry.get(), selected_path.get()))
    connection.commit()
    #scdl_db.close()
    #connection.close()

#main options
def execute_cd_command():
    command = 'cd ' + selected_path.get() + ' && scdl -t -l ' + link_entry.get()
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output_text.insert(tk.END, output.decode())
    output_text.insert(tk.END, error.decode())
    #check if file is outputted before updating db entry maybe
    add_to_database()



def select_folder():
    folder_path = filedialog.askdirectory()
    selected_path.set(folder_path)
    path_label.config(text=folder_path)

selected_path = tk.StringVar()


# CD button
button_execute = tk.Button(root, text="Execute CD Command", command=execute_cd_command)
button_execute.pack(side=tk.BOTTOM, pady=10)

# frame
link_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
link_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# label
link_label = tk.Label(link_frame, text="Enter SoundCloud link here:")
link_label.grid(row=0, column=0, sticky=tk.W)

# entry
link_entry = tk.Entry(link_frame, width=80)
link_entry.grid(row=1, column=0, padx=10, pady=5)

# folder location
path_label = tk.Label(link_frame, text="", width=80)
path_label.grid(row=3, column=0, pady=5)

# folder button
button_select = tk.Button(link_frame, text="Select Folder", command=select_folder)
button_select.grid(row=4, column=0, pady=5)


## terminal output
# frame
output_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
# label
output_label = tk.Label(output_frame, text="Terminal Output")
output_label.pack()
# text
output_text = tk.Text(output_frame, height=10, width=80)
output_text.pack(pady=5)

# Start the event loop to detect user inputs
root.mainloop()
