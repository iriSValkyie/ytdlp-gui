import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import ttk
import threading
import sys
import os

def ytdlp_execute(url,format):
    print("downloading...")
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    yt_dlp_path = os.path.join(base_path, "yt-dlp.exe")
    outputOption = "--output"
    outputOptionValue = "./downloads/%(title)s.%(ext)s"
    convertOption = get_format(format)

    
    command = [yt_dlp_path]
    if outputOption:
        command.extend(outputOption.split())
        command.extend(outputOptionValue.split())
    if convertOption:
        command.extend(convertOption.split())
    command.append(url)
    print(command)
    execute_button["state"] = tk.DISABLED
    progress_bar.pack(pady=10)
    progress_bar.start()
    res = subprocess.run(command, capture_output=True, text=True, encoding=None, shell=True)
    print(res.stderr)
    print(res.stdout)
    progress_bar.stop()
    progress_bar.pack_forget()
    execute_button["state"] = tk.NORMAL

def execute_command():
    url = url_entry.get()
    format = format_state.get()
    format_str = format_to_string(format)

    print(f"url:{url} format:{format_str} ")
    if(url == ""):
        messagebox.showerror("URLエラー","URLを入力してください")
        return
    
   
    thread = threading.Thread(target=ytdlp_execute,args=(url,format))
    thread.start()   

def get_format(format):
    if(format == 1):
        return "-f mp4"
    elif(format == 2):
        return "-x --audio-format mp3"
    return ""

def format_to_string(format):
    if format == 1:
        return "mp4"
    elif format == 2:
        return "mp3"
    else:
        return "Unknown Format"

window = tk.Tk()

window.title("ytdlp-gui")
window.geometry("300x200")

url_frm = tk.Frame(window)
url_frm.pack(pady=10)


url_label = tk.Label(url_frm,text="URL:")
url_label.pack(side=tk.LEFT)


url_entry = tk.Entry(url_frm, width=30)
url_entry.pack(side=tk.LEFT)


otherFrame = tk.Frame(window,width=window.winfo_width())
otherFrame.pack(pady=10)

formatLabelFrm = tk.LabelFrame(otherFrame,text="format")
formatLabelFrm.pack(side=tk.LEFT, padx=10)
format_state = tk.IntVar(value=2)

formatRadio01 = tk.Radiobutton(formatLabelFrm,text="mp4",value=1, variable=format_state)
formatRadio01.pack()
formatRadio02 = tk.Radiobutton(formatLabelFrm,text="mp3",value=2, variable=format_state)
formatRadio02.pack()


execute_button = tk.Button(otherFrame,text="変換開始",command=execute_command)
execute_button.pack(side=tk.RIGHT, padx=10)
progress_bar = ttk.Progressbar(window, mode='indeterminate', length=200, value=0, maximum=100)
progress_bar.pack_forget()

window.mainloop()

