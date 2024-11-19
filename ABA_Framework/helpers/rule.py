import re

class Rule:
    """
    The Rule class represents a rule in an ABA framework. 
    It consists of a `head` and a `body`, where the head represents the conclusion, 
    and the body represents the premises. The body can either be a tuple of literals, 
    another rule, or a single literal.
    
    Attributes:
        head (str): The head or conclusion of the rule.
        body (tuple or Rule or str): The body or premises of the rule.
    
    Methods:
        __init__(self, tuple: tuple):
            Initializes the rule with a head and body.
        
        __repr__(self) -> str:
            Returns a string representation of the rule in the format "head <- body".
        
        to_paths(self) -> list:
            Collects and returns all the paths from the head to the elements in the body.
        
        _collect_paths(self, current_head, body) -> list:
            Recursively collects paths for the head and body while handling nested rules.
        
        parser(literal: str) -> list:
            Static method that parses a string representation of rules and returns 
            a list of tuples representing head and body pairs.
    """
    
    def __init__(self, tuple: tuple):
        """
        Initializes the Rule object with a head and body.

        Args:
            tuple (tuple): A tuple with two elements. The first element is the head of the rule,
                           and the second element is the body of the rule.
        """
        self.head = tuple[0]
        self.body = tuple[1]

    def __repr__(self) -> str:
        """
        Returns a string representation of the rule in the format "head <- body".
        
        Returns:
            str: A string showing the head and body of the rule.
        """
        return f"{self.head} <- {self.body}"
    
    def to_paths(self) -> list:
        """
        Collects and returns all the paths from the head to each literal in the body.

        A path is a list that starts from the head and traverses through the elements 
        of the body, which could include nested rules.

        Returns:
            list: A list of paths, where each path is a list of literals.
        """
        return self._collect_paths(self.head, self.body)

    def _collect_paths(self, current_head: str, body) -> list:
        """
        Recursively collects paths for the head and body. Handles cases where the body 
        contains nested rules or tuples.

        Args:
            current_head (str): The current head element.
            body (tuple, Rule, or str): The body of the rule, which can be a tuple, 
                                        another Rule object, or a string literal.
        
        Returns:
            list: A list of paths where each path is a list of literals.
        """
        paths = []
        
        # If the body is a tuple, handle each element
        if isinstance(body, tuple):
            for item in body:
                # If the item is another Rule, recursively collect paths
                if isinstance(item, Rule):
                    nested_paths = item._collect_paths(item.head, item.body)
                    for path in nested_paths:
                        paths.append([current_head] + path)
                else:
                    # Append the head and the item (literal) to the path
                    paths.append([current_head, item])
        
        # If the body is another Rule, recursively collect paths
        elif isinstance(body, Rule):
            nested_paths = body._collect_paths(body.head, body.body)
            for path in nested_paths:
                paths.append([current_head] + path)
        
        # If the body is a single literal
        else:
            paths.append([current_head, body])
        
        return paths

    @staticmethod
    def parser(literal: str) -> list:
        """
        Parses a string representation of rules and converts them into a list of head-body tuples.
        The method assumes that each rule is enclosed in parentheses and each head-body 
        pair is separated by commas.

        Example input string: "(head1,body1),(head2,body2)"
        
        Args:
            literal (str): The string representation of the rules to be parsed.
        
        Returns:
            list: A list of tuples, where each tuple represents a rule with the head and body.
        """
        all_rules = []
        
        # Extract content inside parentheses
        R_str = re.findall(r'\((.*?)\)', literal)
        
        # Extract each rule and its components
        res = [tuple(re.findall(r'(\w+)', x)) for x in R_str]
        
        for rule in res:
            if len(rule) == 1:
                # If only the head is present the body is empty eg (q,)
                all_rules.append((rule[0], ''))
            elif len(rule) == 2:
                # If the element constains two elements then we have head, body and can add it directly
                all_rules.append(rule)  
            elif len(rule) > 2:
                # If the element contains more than two element then the body is a tuple so we first convert before adding
                all_rules.append((rule[0], tuple(val for val in rule[1:])))
        
        return all_rules
