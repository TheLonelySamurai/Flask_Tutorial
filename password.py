import bcrypt;

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    :param password: The password to hash.
    :return: The hashed password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Return as string for easier storage and comparison
def decrypt_password(hashed_password: str, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    :param hashed_password: The hashed password to check against.
    :param password: The plain text password to check.
    :return: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
#test the functions
if __name__ == "__main__":
    password = "eexample"
    hashed = hash_password(password)
    print(f"Password: {password}")
    print(f"Hashed: {hashed}")
    # Check if the password matches the hashed password
    is_correct = decrypt_password(hashed, password)
    print(f"Password matches: {is_correct}")