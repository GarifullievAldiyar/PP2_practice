def myfunction(title, *args, **kwargs):
    print("title:", title)
    print("positional arguments:", args)
    print("keyword arguments:" , kwargs)

myfunction("user info","Emil","Tobias", age = 35, city = "Oslo") 