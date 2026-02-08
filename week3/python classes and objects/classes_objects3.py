class person:
    def __init__(self,name,age) :
        self.name = name
        self.age = age

    def myfunc(self):
        print("Hello me name is " + self.name)

p1 = person("john" , 36)
del p1
print(p1)