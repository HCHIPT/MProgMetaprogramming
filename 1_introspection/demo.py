class User:
    role = "student"


user = User()
print("Adress of the class User:", hex(id(User)))
print("Adress of the instance: ", hex(id(user)))
input("")