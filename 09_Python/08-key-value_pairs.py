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
