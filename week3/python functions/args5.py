def myfunction(*numbers):
    if len(numbers) == 0:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num>max_num:
            max_num = num
    return max_num

print(myfunction(4 , 5 , 2 , 8 , 9 ))