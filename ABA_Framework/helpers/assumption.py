from helpers.language import Language
import itertools

class Assumption(Language):
    """
    The Assumption class extends the Language class to handle assumptions in the ABA framework.
    It inherits the methods needed to parse the string into individual literals and display the set.
    It also provides a method to generate all subsets of assumptions.

    Methods:
        get_subsets(assumptions: set) -> list:
            Static method that generates all possible subsets of the given set of assumptions.
    """
    
    @staticmethod
    def get_subsets(assumptions: set) -> list:
        """
        Generates all possible subsets of the provided set of assumptions.

        Args:
            assumptions (set): A set of assumptions from which to generate subsets.
        
        Returns:
            list: A list of tuples representing all possible subsets of the input assumptions, 
                   including the empty set.
        """
        subsets = []
        for i in range(len(assumptions) + 1):
            subsets.extend(itertools.combinations(assumptions, i))
        return subsets
