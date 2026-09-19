from schemas.auth import UserCreate


user = UserCreate(
    email="john@example.com",
    password="MyPassword123!",
)

print(user)
print(user.email)
print(user.password)