import re
import sys

filename1 = sys.argv[1]
filename2 = sys.argv[2]
output_counter = 0

words_list = []

print(filename1, filename2)

with open(filename1, 'r') as words_file:
    for line in words_file:
        words_list.append(line.strip())

with open(filename2, 'r') as key_file:
    for line in key_file:
        for word in words_list:
            if re.search(word,line,re.IGNORECASE):
                print("Found: " + word + " in " + line.strip())