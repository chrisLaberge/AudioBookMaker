import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pyttsx3
import PyPDF2
from tqdm import tqdm

def select_file():
    file_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_label.config(text=file_path)

def save_file():
    save_path = asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if save_path:
        save_label.config(text=save_path)

def convert_to_audio():
    file_path = file_label.cget("text")
    save_path = save_label.cget("text")

    if not file_path or not save_path:
        return

    with open(file_path, 'rb') as file:
        pdfreader = PyPDF2.PdfReader(file)
        pages = len(pdfreader.pages)
        
        player = pyttsx3.init()
        full_text = ""

        progress_bar['maximum'] = pages

        for num in tqdm(range(pages), desc="Processing Pages"):
            page = pdfreader.pages[num]
            text = page.extract_text()
            full_text += text
            progress_bar['value'] = num + 1
            root.update_idletasks()

        player.save_to_file(full_text, save_path)
        player.runAndWait()

    progress_bar['value'] = 0
    tk.messagebox.showinfo("Success", "Audio file saved successfully!")

root = tk.Tk()
root.title("Chris' PDF to Audio Converter")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# File selection
ttk.Label(frame, text="Select PDF:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
file_label = ttk.Label(frame, text="No file selected")
file_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
ttk.Button(frame, text="Browse", command=select_file).grid(row=0, column=2, padx=5, pady=5)

# Save location
ttk.Label(frame, text="Save As:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
save_label = ttk.Label(frame, text="No save location selected")
save_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
ttk.Button(frame, text="Browse", command=save_file).grid(row=1, column=2, padx=5, pady=5)

# Progress bar
ttk.Label(frame, text="Progress:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

# Convert button
ttk.Button(frame, text="Convert", command=convert_to_audio).grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
