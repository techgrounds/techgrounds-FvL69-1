print("Exercise 1")
# Use a for loop to loop over the list. Print every name individually.
arr = ["Shikha", "Casper", "Bart", "Ruben", "Ulviye"]
for name in arr:
    print(name)


print()
print("Exercise 2")
# print every item added with the next item in the sequence, for the last item add the first item of the list.
numlist = [1, 23, 44, 56, 87, 109]
x = 1
while x != 6:
    print(numlist[x-1] + numlist[x])
    if x == 5:
        print(numlist[5] + numlist[0])
    x += 1

