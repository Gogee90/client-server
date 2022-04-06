import uuid


def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def flip_letters(word):
    new_word = []
    for i, n in enumerate(word):
        if i % 2 != 0:
            new_word.insert(i - 1, n)
        else:
            new_word.insert(i, n)
    return "".join(new_word)


def multiply_letters(word):
    return "".join([letter * index for index, letter in enumerate(word, 1)])


def flip_letters_backwards(word):
    return word[::-1]
