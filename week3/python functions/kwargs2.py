def myfunction(**myvar):
    print("Type :", type(myvar))
    print("Name :", myvar["name"])
    print("Age :",myvar["age"])
    print("All data :", myvar)

myfunction(name = "Tobias", age = 40 , city = "Bergen")
