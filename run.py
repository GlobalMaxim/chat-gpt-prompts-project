import os
import tkinter as tk
from tkinter import filedialog
from time import sleep

from pandas import read_csv

from main import TextCreator

def show_popup(text: str):
    popup = tk.Toplevel(root)
    popup.title("Info")
    link_label = tk.Label(popup, text=text)
    link_label.pack(padx=60)
    continue_button = tk.Button(popup, text="Continue", command=popup.destroy)
    continue_button.pack()

def browse_parametres_file():
    file_path = filedialog.askopenfilename()
    parametres_label_entry.delete(0, tk.END)
    parametres_label_entry.insert(0, file_path)

def browse_prompts_file():
    file_path = filedialog.askopenfilename()
    prompts_label_entry.delete(0, tk.END)
    prompts_label_entry.insert(0, file_path)

def browse_result_path():
    file_path = filedialog.askdirectory()
    result_folder_entry.delete(0, tk.END)
    result_folder_entry.insert(0, file_path)

def run():
    api_key = api_key_entry.get()
    parametres_file = parametres_label_entry.get()
    prompts_file = prompts_label_entry.get()
    result_folder = result_folder_entry.get()
    gpt_version = gpt_version_var.get()
    sync_data = bool(sync_data_entry.get())
    parametres_list = get_parametres_from_file(parametres_file)
    prompts = get_prompts_from_file(prompts_file)
    for (keyword, country) in parametres_list:
         generator = TextCreator(
                                    api_key=api_key, 
                                    keyword=keyword,
                                    country=country, 
                                    prompts=prompts,
                                    result_folder_path=result_folder,
                                    gpt_version=gpt_version,
                                    sync_data=sync_data
                                )
         generator.create_full_text()
    text = 'Finished'
    show_popup(text)

def get_prompts_from_file(path) -> list:
    data = read_csv(path, names=['prompts'], delimiter=";")
    result = []
    for _, row in data.iterrows():
        a = str(row['prompts'])
        if a != 'nan':
            result.append(a)
    return result

def get_parametres_from_file(path) -> list:
    data = read_csv(path, names=['keyword', 'country'], delimiter=";")
    result = []
    for _, row in data.iterrows():
        a = str(row['keyword'])
        b = str(row['country'])
        result.append((a, b))
    return result

root = tk.Tk()
root.title("Chat GPT Text Creator")


api_key = tk.Label(root, text="Api Key:")
api_key.pack()
api_key_entry = tk.Entry(root)
api_key_entry.pack(padx=60)

delimeter = tk.Label(root, text="________________")
delimeter.pack()

parametres_label = tk.Label(root, text="Parametres path:")
parametres_label.pack()
parametres_label_entry = tk.Entry(root)
parametres_label_entry.pack()
browse_button = tk.Button(root, text="Browse parametres file", command=browse_parametres_file)
browse_button.pack()

delimeter = tk.Label(root, text="________________")
delimeter.pack()

prompts_label = tk.Label(root, text="Prompts path:")
prompts_label.pack()
prompts_label_entry = tk.Entry(root)
prompts_label_entry.pack()
browse_button = tk.Button(root, text="Browse prompts file", command=browse_prompts_file)
browse_button.pack()

delimeter = tk.Label(root, text="________________")
delimeter.pack()

result_folder_label = tk.Label(root, text="Result path:")
result_folder_label.pack()
result_folder_entry = tk.Entry(root)
result_folder_entry.pack()
browse_button = tk.Button(root, text="Browse result path", command=browse_result_path)
browse_button.pack()

delimeter = tk.Label(root, text="________________")
delimeter.pack()

gpt_version_link = tk.Label(root, text="Select GPT Version:")
gpt_version_link.pack()
gpt_version_var = tk.StringVar(root)
gpt_version_var.set("GPT-4 Turbo") # default value
gpt_version_opt = tk.OptionMenu(root, gpt_version_var,"GPT-4", "GPT-4 Turbo", "GPT-3.5")
gpt_version_opt.pack()

delimeter = tk.Label(root, text="________________")
delimeter.pack()

sync_data = tk.Label(root, text="Synchronize data")
sync_data.pack()
sync_data_entry = tk.IntVar()
c1 = tk.Radiobutton(root, variable=sync_data_entry, value=1, text="True")
c1.pack()
c2 = tk.Radiobutton(root, variable=sync_data_entry, value=0, text="False")
c2.pack()

delimeter = tk.Label(root, text="________________")
delimeter.pack()

login_button = tk.Button(root, text="Run", command=run)
login_button.pack()

root.mainloop()