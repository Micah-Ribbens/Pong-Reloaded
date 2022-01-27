from random import randint

def get_random_item(list):
    """ summary: gets a random index then returns list[index]

        params:
            list: List; the list that will have a random item returned from it

        returns: Object; a random item from the list
    """
    index = randint(0, len(list) - 1)

    return list[index]
