from random import randint
def get_random_item(list):
    index = randint(0, len(list) - 1)

    return list[index]