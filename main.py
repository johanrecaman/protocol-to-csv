
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
            if ':' in field and '(' not in field:
                values.append(field.split(':', 1)[1])

            else:
                values.append(field)
        updated_txt.append(','.join(values))
    return updated_txt

def separate_by_line(txt):
    return txt.replace("[", "").split("],")


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

    with open("trace.csv", "w") as file:
        for line in txt:
            file.write(f"{line}\n")

def main():
    html_to_csv("trace.html")

if __name__ == "__main__":
    main()