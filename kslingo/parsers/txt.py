import os


def ReadFromTxtFile(input_file):
    print("start ReadFromTxtFile")
    
    # sanity
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"File '{input_file}' doesn't exist!")
    if not input_file.lower().endswith(".txt"):
        raise ValueError(f"File '{input_file}' isn't .txt! Please enter after arg --txt <file>.txt")
    
    phrases = []
    with open(input_file, "r", encoding="utf-8") as f:
        for  line in f:
            line = line.replace("–", "-")
            if "-" in  line:
                left, right =  line.strip().split("-", maxsplit=1)
                phrases.append((left.strip(), right.strip()))
                
    # only debug
    print(phrases)
    return phrases
