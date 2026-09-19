from utils.security import hash_password, verify_password


password = "MyPassword123!"

hashed = hash_password(password)

print("Original:")
print(password)

print("\nHash:")
print(hashed)

print("\nCorrect password:")
print(verify_password(password, hashed))

print("\nWrong password:")
print(verify_password("WrongPassword", hashed))