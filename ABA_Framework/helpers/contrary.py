import re

class Contrary:
    """
    The Contrary class represents a contrary relation in the ABA framework.
    It defines a contrary relationship between two elements, where one element is contrary to the other.

    Attributes:
        contrary (str): The contrary element.
        arg (str): The argument or proposition that is contrary to the contrary element.

    Methods:
        __init__(self, tuple: tuple):
            Initializes the contrary relationship with a contrary element and an argument.
        
        __repr__(self) -> str:
            Returns a string representation of the contrary in the format "Contrary de contrary = arg".
        
        parser(literal: str) -> list:
            Static method that parses a string representation of contrary relations and returns 
            a list of tuples representing the contrary and its argument.
        
        to_dict(contrary_list: list) -> dict:
            Static method that converts a list of Contrary objects into a dictionary where 
            the contrary element is the key, and the argument(s) are stored in tuples as values.
    """
    
    def __init__(self, tuple: tuple):
        """
        Initializes the Contrary object with a contrary element and an argument.

        Args:
            tuple (tuple): A tuple with two elements. The first element is the contrary, 
                           and the second element is the argument.
        """
        self.contrary = tuple[0]
        self.arg = tuple[1]

    def __repr__(self) -> str:
        """
        Returns a string representation of the contrary relation in the format "Contrary de contrary = arg".
        
        Returns:
            str: A string showing the contrary and the argument in the format "Contrary de contrary = arg".
        """
        return f"Contrary de {self.contrary} = {self.arg}"

    @staticmethod
    def parser(literal: str) -> list:
        """
        Parses a string representation of contrary relations and converts them into a list of tuples.
        Each tuple represents a contrary relationship between a contrary element and its argument.

        The input string should contain contrary relations enclosed in parentheses.

        Example input string: "(a b), (c d)"
        
        Args:
            literal (str): The string representation of the contrary relations to be parsed.
        
        Returns:
            list: A list of tuples, where each tuple represents a contrary relationship.
        """
        R_str = re.findall(r'\((.*?)\)', literal)
        return [tuple(re.findall(r'(\w+)', x)) for x in R_str]

    @staticmethod
    def to_dict(contrary_list: list) -> dict:
        """
        Converts a list of Contrary objects into a dictionary. The contrary element becomes the key, 
        and the arguments that are contrary to the element are stored in tuples as values.

        If a contrary element has multiple arguments, all of them are combined as values for the same key.

        Args:
            contrary_list (list): A list of Contrary objects to be converted into a dictionary.
        
        Returns:
            dict: A dictionary where each key is a contrary element, and the value is a tuple containing 
                  all the arguments that are contrary to that element.
        """
        contrary_dict = {}
        
        for contrary_obj in contrary_list:
            key = contrary_obj.contrary
            # Store the argument as a tuple
            value = (contrary_obj.arg,)  
            
            # If the contrary key exists, append the argument to the existing tuple
            if key in contrary_dict:
                current_val = contrary_dict[key]
                contrary_dict[key] = current_val + value
            else:
                contrary_dict[key] = value
        
        return contrary_dict
