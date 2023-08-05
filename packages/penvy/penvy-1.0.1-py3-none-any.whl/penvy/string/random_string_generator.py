import random
import string


def generate_random_string(string_length: int):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))
