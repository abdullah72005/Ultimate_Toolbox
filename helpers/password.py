import random

def generate_password(length: int, upper: bool, lower: bool, nums: bool, syms: bool):

    # get values of all possible characters
    uppercase = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    lowercase = uppercase.lower()
    numbers = '1234567890'
    symbols = '!@#$%^&*_+=|;:,.~'
    all_input = ''

    password = ''

    # Ensure at least one character from each selected character set
    if upper:
        password += random.choice(uppercase)
        all_input += uppercase
    if lower:
        password += random.choice(lowercase)
        all_input += lowercase
    if nums:
        password += random.choice(numbers)
        all_input += numbers
    if syms:
        password += random.choice(symbols)
        all_input += symbols

    # Generate the rest of the password
    for _ in range(length - len(password)):
        password += random.choice(all_input)

    # Shuffle the characters to make the password more random
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

