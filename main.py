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
    txt = txt.replace("\n", "")

    return txt

def dash_to_comma(txt):
    result = []
    exceptions = [":", ",", "["]
    for i in range(len(txt)):
        if txt[i] == "-" and txt[i-1] not in exceptions:
            result.append(",")
        elif txt[i] == "-" and txt[i-1] == ":" and not txt[i+1].isdigit():
            result.append("")
        else:
            result.append(txt[i]) 
    return ''.join(result)

def join_special_values(txt):
    modified_lines = []

    for line in txt:
        fields = line.split(',')
        if '(' not in line:
            fields[5:5] = [""]
            line = ','.join(fields)
        line = line.replace("),(", ")(")
        modified_lines.append(line)
    return modified_lines

def set_null(txt):
    updated_txt = []

    for line in txt:
        fields = line.split(',')
        if "Alt" not in line:
            if '(' in line:
                fields[6:6] = [""] * 25
            else:
                fields[5:5] = [""] * 25
        if len(fields) == 31:
            fields.append("")
        updated_txt.append(','.join(fields))
    return updated_txt
        
def remove_keys(txt):
    updated_txt = []
    for line in txt:
        fields = line.split(',')
        values = []
        for field in fields:
            if '(' not in field and field.count(':') == 1:
                values.append(field.split(':', 1)[1])
            else:
                values.append(field)
        updated_txt.append(','.join(values))
    return updated_txt

def separate_by_line(txt):
    return txt.replace("[", "").split("],")

def remove_loc(txt):
    updated_txt = []

    for line in txt:
        fields = line.split(',')
        fields = fields[3:]
        updated_txt.append(','.join(fields))
    return updated_txt

def to_excel(txt):
    newTxt = []
    for line in txt:
        line = line.replace(",", ";")
        line = line.replace(".", ",")
        newTxt.append(line)
    return newTxt

def html_to_csv(file_path, skip):

    with open(file_path, "r") as file:
        txt = file.read()

    txt = remove_html_tags(txt)
    txt = format(txt)
    txt = dash_to_comma(txt)
    txt = separate_by_line(txt)
    txt = join_special_values(txt)
    txt = set_null(txt)
    if skip:
        txt = remove_loc(txt)
    txt = remove_keys(txt)
    txt = to_excel(txt)

    return txt


def generate_csv(file_path, skip):
    headers = ["Lat", "Long", "Valid Pos", "Date", "Time", "event_Tracer", "Alt", "Spd", "Rpm", "Tk", "Tk Friction", "Odo", "FuelAvg", "BoostP", "ExhaustP", "AdmTemp", "Regen Status", "NoxIn", "NoxOut", "DOC In", "DOC out", "DPF out", "SCR out", "DpfMaxTemp", "UrLv", "UrTemp", "UrQlty", "SootLoad", "Acl Pos", "Eng.Temp", "Amb.Temp", "Seq"]
    if skip:
        headers = headers[3:]
    with open(file_path, mode='w') as csv_file:
        csv_file.write(";".join(headers) + "\n")
        for line in converted_file:
            csv_file.write(line + "\n")

window = tk.Tk()
window.title("HTML to CSV V0.4")
window.geometry("600x200")

success_msg = tk.Label(window, text="")
success_msg.place(x=0, y=0)

filepath_msg = tk.Label(window, text="")
filepath_msg.place(x=0, y=20)

converted_file = None

def convert_html_to_csv():
    global converted_file, var

    html_file_path = filedialog.askopenfilename(filetypes=[("html files", "*.html")])

    if html_file_path:
        converted_file = html_to_csv(html_file_path, var.get())
        success_msg.config(text="File converted successfully!")
        filepath_msg.config(text="File path: " + html_file_path)
        return
    success_msg.config(text="File not converted!")

def download_file():
    global var
    base_filename = filepath_msg.cget("text").split(": ")[
        1].split("/")[-1].split(".")[0]

    if var.get():
        base_filename += "H"
    csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile=f"{base_filename}.csv")

    if csv_file_path:
        generate_csv(csv_file_path, var.get())
        success_msg.config(text="File saved successfully!")
        return
    
var = tk.IntVar()
checkbox = tk.Checkbutton(window, text="Skip Loc", variable=var)
checkbox.place(x=235, y=50)

convert_button = tk.Button(window, text="Upload File", command=convert_html_to_csv)
convert_button.place(x=315, y=50)

download_button = tk.Button(window, text="Download", command=download_file)
download_button.place(x=530, y=170)

window.mainloop()