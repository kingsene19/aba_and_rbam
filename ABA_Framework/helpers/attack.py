class Attack:
    """
    The Attack class represents an attack relation between two arguments in the ABA framework.
    It defines an attack from a source argument to a destination argument.

    Attributes:
        source (int): The index of the argument that initiates the attack.
        destination (int): The index of the argument that is being attacked.

    Methods:
        __init__(self, source: int, destination: int):
            Initializes the attack relationship between a source argument and a destination argument.
        
        __repr__(self) -> str:
            Returns a string representation of the attack in the format "A{source} attacks A{destination}".
    """
    
    def __init__(self, source: int, destination: int):
        """
        Initializes the Attack object with a source argument and a destination argument.

        Args:
            source (int): The index of the source argument initiating the attack.
            destination (int): The index of the destination argument being attacked.
        """
        self.source = source
        self.destination = destination

    def __repr__(self) -> str:
        """
        Returns a string representation of the attack relation in the format "A{source} attacks A{destination}".
        
        Returns:
            str: A string showing the attack relation in the format "A{source} attacks A{destination}".
        """
        return f"A{self.source} attacks A{self.destination}"
