
def save_file(file_name,file):
    with open(file_name,"w",encoding="utf-8") as f:
        f.write(file)

def open_file(file_name):
    with open(file_name,"r",encoding="utf-8") as f:
        return f.read()