from base_pong.colors import *


class TestCase:
    inputs = []
    output = None

    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output


class Parameter:
    """Stores the type, name, and color of each parameter in a function"""
    type = None
    name = None
    color = None

    def __init__(self, type: str, name: str):
        """ summary: initializes the object

            params:
                type: String; the type of the parameter like int, String, etc.
                name: String; the name of the parameter

            returns: None
        """
        self.type = type
        self.name = name

        type = type.lower()
        type_to_color = {
            type.__contains__("list"): red,
            type.__contains__("map"): blue,
            type.__contains__("string"): green,
            type.__contains__("int"): purple,
            type.__contains__("boolean"): orange
        }
        # The first things that is True is the color of the type
        self.color = type_to_color.get(True) if not type_to_color.get(True) is None else black


class Function:
    """Stores the values for every function in the file"""

    parameters = []
    name = ""
    number_of_outputs = 0
    test_cases = []
    output_type = ""

    def __init__(self, parameters, name):
        """ summary: initializes the object

            params:
                parameters: List of Parameter; the parameters that the function has
                name: String; the name of the function

            returns: None
        """

        self.parameters = parameters
        self.name = name


