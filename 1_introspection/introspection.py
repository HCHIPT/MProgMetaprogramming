import inspect

class User:
    user_id: int
    username: str
    role: str

    def __init__(self, user_id: int, username: str, role: str = "student"):
        self.user_id = user_id
        self.username = username
        self.role = role

    def promote(self, new_role: str) -> None:
        self.role = new_role


user = User(101, "lukasz")


# print("Type:", type(user))
# print("Is User?:", isinstance(user, User))
# print("Runtime attributes (__dict__):", user.__dict__)
# print("Type hints (__annotations__):", User.__annotations__)

# methods = inspect.getmembers(user, predicate=inspect.ismethod)
# print("Methods:", [name for name, _ in methods])

# sig = inspect.signature(user.promote)
# print("Signature of promote():", sig)
# for param_name, param in sig.parameters.items():
#     print(f"  -> param '{param_name}', type: {param.annotation}")

# print("Source code:\n", inspect.getsource(user.promote))

