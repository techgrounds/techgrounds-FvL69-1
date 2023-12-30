print("Exercise 1")
# Create a dictionary of the two lists.
k = ['First Name', 'Last Name', 'Job Title', 'Company']
v = ['Francois', 'van Lieshout', 'student', 'TechGrounds']

# Using a dict comprehension with the zip() function.
dict = {k: v for k, v in zip(k, v)}
print(dict)


print()
print("Exercise 2")
# Create a dictionary with user input.
# Syntax dict[x] = i, will bind key 'x' to new value 'i'.
for x in dict.keys():
    i = input(f"Pls enter your {x}: ")
    dict[x] = i

print(dict)


print()
import csv 
# Write the dict content to a csv file. 
# Create a csv file.
fp = open("dict.csv", "w")
fp.close() 

# Using the key list 'k' for the header.
csv_header = k 
# Store a copy of the dict in an empty list.
dict_list = []
dict_list.append(dict.copy())

file_csv = "dict.csv"
try:
    # Opening the csv file this time with 'a' instead of 'w' to prevent overwriting the content.
    with open(file_csv, 'a') as csv_file:
        linker = csv.DictWriter(csv_file, fieldnames = csv_header)
        linker.writeheader()
        for item in dict_list:
            linker.writerow(item)

except IOError:
    print("Error encountered...")

with open("dict.csv") as f:
    buffer = f.read()

print(buffer)

