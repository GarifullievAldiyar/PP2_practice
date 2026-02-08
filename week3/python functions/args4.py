def myfunction(*numbers):
    total = 0
    for num in numbers:
        total += num 
    return total

print(myfunction(1,2,3))
print(myfunction(10,20,30,40))
print(myfunction(5))