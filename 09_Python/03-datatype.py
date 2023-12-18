# Exercise 1
# Print the data type 
a = 'int'
b = 7
c = False
d = "18.5"

print(type(a))
print(type(b))
print(type(c))
print(type(d))

print()

# type cast string d to a float
x = b + float(d) 
print('b + d =', x)


# Exercise 2
# Use the input() function to get input from the user
x = input("Enter a number between 0 and 10: ")
print(f"The number you've entered is: {x}")
print(type(x))
print(type(int(x)))
