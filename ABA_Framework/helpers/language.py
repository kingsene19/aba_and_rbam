import re

class Language:
    """
    The Language class represents a set containing the language structure of the ABA framework, 
    and provides methods to parse the string into individual literals to create the set of literals.

    Attributes:
        _literal (str): The input string representing the language.
    
    Methods:
        __init__(self, literal: str):
            Initializes the Language object with the input string.
        
        parse(self) -> set:
            Parses the input string and returns a set of literals found in the string.
        
        __repr__(self) -> str:
            Returns the original input string as the string representation of the object.
    """
    
    def __init__(self, literal: str):
        """
        Initializes the Language object with the input string.

        Args:
            literal (str): The input string representing the language structure to be parsed.
        """
        self._literal = literal

    def parse(self) -> set:
        """
        Parses the input string and extracts all literals.
        The words are extracted based on word boundaries (alphanumeric characters).
        
        Returns:
            set: A set of unique literals found in the input string.
        """
        return set(re.findall(r'\w+', self._literal))
