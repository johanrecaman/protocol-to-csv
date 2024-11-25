
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
            result.append("NULL")
        else:
            result.append(txt[i]) 
    return ''.join(result)

def join_special_values(txt):
    modified_lines = []

    for line in txt:
        if '(' in line:
            start_index = line.index('(')
            end_index = line.rindex(')') + 1

            before = line[:start_index]
            between = line[start_index:end_index]
            after = line[end_index:]

            between = between.replace("),(", ")(")
            line = f"{before}{after.strip(',')},{between}"
        modified_lines.append(line)
    return modified_lines

def set_values(txt):
    null = "Null"
    updated_txt = []

    for line in txt:
        fields = line.split(',')
        if "Alt" in fields:
            print("alt")
            continue
        fields[5:5] = [null] * 25
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

def main():
    file = open("trace.html", "r")
    txt = file.read()
    file.close()

    txt = remove_html_tags(txt)
    txt = format(txt)
    txt = dash_to_comma(txt)
    txt = separate_by_line(txt)
    txt = set_values(txt)
    #txt = remove_keys(txt)
    txt = join_special_values(txt)

    print(txt[1])
    file = open("trace.csv", "w")
    for line in txt:
        file.write(f"{line}\n")
    file.close()
if __name__ == "__main__":
    main()