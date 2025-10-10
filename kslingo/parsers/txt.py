import os
from kslingo.utils.text import split_pair
from kslingo.utils.text import normalize_separator

from kslingo.utils.fs import validate_file

def ReadFromTxtFile(input_file):    
    print("start ReadFromTxtFile")
    
    phrases = []
    
    # sanity
    validate_file(input_file, ".txt")

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = normalize_separator(line)
            left, right = split_pair(line)
            if left and right:
                phrases.append((left, right))

    # only debug
    print(phrases)
    return phrases
