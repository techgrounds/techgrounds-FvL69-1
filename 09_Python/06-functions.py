from random import randint

print("Exercise 1")
# Print 5 random number between 1 and 100.
for n in range(6):
    print(randint(1, 100))


print()
print("Exercise 2")
# Write a custom function myfunction() that prints “Hello, world!” to the terminal. Call myfunction.
# Customize the fuction with an input function to enter a name and print the output.
def myfunction():
    x = input("Enter your name: ")
    print(f"Hello {x}!")

myfunction() 

print()
print("Exercise 3")
# Return the average of the parameter input.
def avg(x,y):
    return (x + y) / 2

x = 128
y = 255
z = avg(x,y)

print("The average of",x,"and",y,"is",z)