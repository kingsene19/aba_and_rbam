import re

class Preference:
    """
    The Preference class represents a preference relation between two elements 
    in the form of a tuple `(least, most)`, where the least preferred element is 
    compared to the most preferred element.
    
    Attributes:
        least (str): The less preferred element.
        most (str): The more preferred element.
    
    Methods:
        __init__(self, tuple: tuple):
            Initializes the preference with a least and most preferred element.
        
        __repr__(self) -> str:
            Returns a string representation of the preference in the format "least < most".
        
        parser(literal: str) -> list:
            Static method that parses a string representation of preferences and returns 
            a list of tuples representing least and most preferences.
        
        to_dict(preference_list: list) -> dict:
            Converts a list of Preference objects into a dictionary where the least preferred 
            element is the key, and the values are tuples of the corresponding most preferred elements.
    """
    
    def __init__(self, tuple: tuple):
        """
        Initializes the Preference object with a least and most preferred element.

        Args:
            tuple (tuple): A tuple with two elements. The first element is the less preferred element,
                           and the second element is the more preferred element.
        """
        self.least = tuple[0]
        self.most = tuple[1]

    def __repr__(self) -> str:
        """
        Returns a string representation of the preference in the format "least < most".
        
        Returns:
            str: A string showing the least and most preferred elements in the format "least < most".
        """
        return f"{self.least} < {self.most}"

    @staticmethod
    def parser(literal: str) -> list:
        """
        Parses a string representation of preferences and converts them into a list of tuples.
        Each tuple represents a preference relationship between a least and most preferred element.

        The input string should contain preferences enclosed in parentheses.
        If a preference has multiple most preferred elements, they are split into separate tuples.

        Example input string: "(a,b),(c,(d,e))"
        
        Args:
            literal (str): The string representation of the preferences to be parsed.
        
        Returns:
            list: A list of tuples, where each tuple represents a preference with least and most elements.
        """
        all_prefs = []
        
        # Extract content inside parentheses
        R_str = re.findall(r'\((.*?)\)', literal)
        
        # Extract each preference and its components
        res = [tuple(re.findall(r'(\w+)', x)) for x in R_str]
        
        for pref in res:
            # If there are more than two elements, create multiple (least, most) pairs
            if len(pref) > 2:
                for x in pref[1:]:
                    all_prefs.append((pref[0], x))
            elif len(pref) == 2:
                # If only two element create a pair
                all_prefs.append(pref)
        
        return all_prefs

    @staticmethod
    def to_dict(preference_list: list) -> dict:
        """
        Converts a list of Preference objects into a dictionary. The least preferred 
        element becomes the key, and the most preferred elements are stored in tuples as values.

        Args:
            preference_list (list): A list of Preference objects to be converted into a dictionary.
        
        Returns:
            dict: A dictionary where each key is a least preferred element, and the value is a tuple 
                  containing all the most preferred elements for that key.
        """
        preference_dict = {}
        
        for preference_obj in preference_list:
            key = preference_obj.least
            # Store the value as a tuple
            value = (preference_obj.most,)
            
            # Append the value if the key exists, otherwise create a new entry
            if key in preference_dict:
                current_val = preference_dict[key]
                preference_dict[key] = current_val + value
            else:
                preference_dict[key] = value
        
        return preference_dict
