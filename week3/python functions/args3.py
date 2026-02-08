def myfunction(greeting, *names):
    for name in names:
        print(greeting, name)

myfunction("Hello", "Emil", "Tobias", "Linus")