print("Exercise 1") 
# Ask user to enter a name, print a personalized message depending the input.
x = input("What is your name?: ")
if x == "Francois":
    print(f"Welcome {x}, good to see you!")
else:
    print(f"Only Francois is authorized {x}, goodbye!")


print()
print("Exercise 2")
# Ask the user to enter a number, when the number equals 100 stop the loop.
while x != 100:
    x = int(input("Enter a number: "))
    if x < 100:
        print("You're input is lower than 100.")
        continue
    elif x > 100:
        print("You're input is higher than 100.")
        continue
    else:
        print("You're input is equal to 100.")
        break



