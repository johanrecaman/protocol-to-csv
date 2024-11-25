import tkinter as tk
from tkinter import filedialog

def remove_html_tags(txt):
    start_key = "= ["
    end_key = "];"

    start_tag_index = (txt.find(start_key) + len(start_key))
    end_tag_index = (txt.find(end_key) - start_tag_index)

    txt = txt[start_tag_index:]
    txt = txt[:end_tag_index]

    return txt

def format(txt):
    txt = txt.replace("|", ",")
    txt = txt.replace("'", "")
    txt = txt.replace(" ", "")
    txt = txt.replace("\n", "")

    return txt

def dash_to_comma(txt):
    result = []
    exceptions = [":", ",", "["]
    for i in range(len(txt)):
        if txt[i] == "-" and txt[i-1] not in exceptions:
            result.append(",")
        elif txt[i] == "-" and txt[i-1] == ":" and not txt[i+1].isdigit():
            result.append("Null")
        else:
            result.append(txt[i]) 
    return ''.join(result)

def join_special_values(txt):
    null =  "Null"
    modified_lines = []

    for line in txt:
        fields = line.split(',')
        if '(' not in line:
            fields[5:5] = [null]
            line = ','.join(fields)
        line = line.replace("),(", ")(")
        modified_lines.append(line)
    return modified_lines

def set_null(txt):
    null = "Null"
    updated_txt = []

    for line in txt:
        fields = line.split(',')
        if "Alt" not in line:
            if '(' in line:
                fields[6:6] = [null] * 25
            else:
                fields[5:5] = [null] * 25
        if len(fields) == 31:
            fields.append(null)
        updated_txt.append(','.join(fields))
    return updated_txt
        
def remove_keys(txt):
    updated_txt = []
    for line in txt:
        fields = line.split(',')
        values = []
        for field in fields:
            if ':' in field:
                if '(' not in field and field.count(':') == 1:
                    values.append(field.split(':', 1)[1])
            else:
                values.append(field)
        updated_txt.append(','.join(values))
    return updated_txt

def separate_by_line(txt):
    return txt.replace("[", "").split("],")

def reileao(txt):
    newTxt = []
    for line in txt:
        line = line.replace(",", ";")
        newTxt.append(line)
    return newTxt

def html_to_csv(file_path):

    with open(file_path, "r") as file:
        txt = file.read()

    txt = remove_html_tags(txt)
    txt = format(txt)
    txt = dash_to_comma(txt)
    txt = separate_by_line(txt)
    txt = join_special_values(txt)
    txt = set_null(txt)
    txt = remove_keys(txt)
    txt = reileao(txt)

    return txt


def generate_csv(file_path):
    headers = ["Lat", "Long", "Valid Pos", "Date", "Time", "event_Tracer", "Alt", "Spd", "Rpm", "Tk", "Tk Friction", "Odo", "FuelAvg", "BoostP", "ExhaustP", "AdmTemp", "Regen Status", "NoxIn", "NoxOut", "DOC In", "DOC out", "DPF out", "SCR out", "DpfMaxTemp", "UrLv", "UrTemp", "UrQlty", "SootLoad", "Acl Pos", "Eng.Temp", "Amb.Temp", "Seq"]

    with open(file_path, mode='w') as csv_file:
        csv_file.write(";".join(headers) + "\n")
        for line in converted_file:
            csv_file.write(line + "\n")

window = tk.Tk()
window.title("HTML to CSV Converter")
window.geometry("450x200")

success_msg = tk.Label(window, text="")
success_msg.pack()

filepath_msg = tk.Label(window, text="")
filepath_msg.pack()

converted_file = None

def convert_html_to_csv():
    global converted_file
    html_file_path = filedialog.askopenfilename(filetypes=[("html files", "*.html")])

    if html_file_path:
        converted_file = html_to_csv(html_file_path)
        success_msg.config(text="File converted successfully!")
        filepath_msg.config(text="File path: " + html_file_path)
        return
    success_msg.config(text="File not converted!")

def download_file():
    csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if csv_file_path:
        generate_csv(csv_file_path)
        success_msg.config(text="File saved successfully!")
        return
    
convert_button = tk.Button(window, text="Upload File", command=convert_html_to_csv)
convert_button.pack(pady=20)

download_button = tk.Button(window, text="Download", command=download_file)
download_button.pack(pady=20)

window.mainloop()