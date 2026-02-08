class person:
    def __init__(self, fname , lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self):
        print(self.firstname,self.lastname)

x = person("John", "Doe")
x.printname()