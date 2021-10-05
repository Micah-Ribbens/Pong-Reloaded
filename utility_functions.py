def deepcopy(object):
    copied_object = type(object)()
    for key in copied_object.attributes:
        copied_object.__dict__[key] = object.__dict__[key]

    return copied_object
