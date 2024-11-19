class Argument:
    """
    The Argument class represents an argument in an argumentation framework.
    It consists of a claim and supporting elements (leaves).

    Attributes:
        claim (str): The main assertion or claim of the argument.
        leaves (optional(list)): The supporting elements or sub-arguments for the claim. 
                                  Defaults to None if not provided.

    Methods:
        __init__(self, claim: str, leaves=None):
            Initializes the Argument object with a claim and optional supporting elements.
        
        __repr__(self) -> str:
            Returns a string representation of the argument in the format "leaves |- claim".
    """

    def __init__(self, claim: str, leaves=None):
        """
        Initializes the Argument object with a claim and optional supporting elements.

        Args:
            claim (str): The main assertion or claim of the argument.
            leaves (list, optional): The supporting elements or sub-arguments for the claim. 
                                     Defaults to None if not provided.
        """
        self.claim = claim
        self.leaves = leaves

    def __repr__(self) -> str:
        """
        Returns a string representation of the argument in the format "leaves |- claim".
        
        Returns:
            str: A string showing the structure of the argument, indicating how the claim is supported.
        """
        return f"{self.leaves} |- {self.claim}"
