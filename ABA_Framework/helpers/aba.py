from helpers.rule import Rule
from helpers.contrary import Contrary
from copy import deepcopy

class ABA:
    """
    The ABA class represents an Argument Based Framework for handling language, arguments, assumptions,
    rules, contraries, and preferences. It provides methods to manage and analyze the structure
    and validity of the framework.

    Attributes:
        language (set[str]): The set of terms that represent the language of the argumentation framework.
        assumptions (set[str]): The set of assumptions used in the argumentation.
        rules (list[Rule]): The list of rules that define the relationships between arguments.
        contraries (list[Contrary]): The list of contrary relations between arguments.
        preferences (list): The list of preferences among arguments or assumptions.
        arguments (optional[list): The arguments generated from the assumptions and rules.
        attacks (optional[list]): The attacks between arguments.
        normal_attacks (optional[list]): Normal attacks using preferences
        reverse_attacks (optional[list]): Reverse attacks using preferences

    Methods:
        __init__(self, language: set[str], assumptions: set[str], rules: list[Rule], 
                 contraries: list[Contrary], preferences: list):
            Initializes the ABA object with language, assumptions, rules, contraries, and preferences.

        _get_literals_in_rules(self) -> set:
            Retrieves all literals found in the defined rules.

        _get_literals_in_contraries(self) -> set:
            Retrieves all literals found in the defined contraries.

        _get_literals_in_preferences(self) -> set:
            Retrieves all literals found in the defined preferences.

        _is_valid(self) -> bool:
            Checks if the argumentation framework is valid based on assumptions, language, rules, and contraries.

        _is_atomic(self) -> bool:
            Determines if all rules in the argumentation framework are atomic.

        _is_atmomic_rule(self, rule) -> bool:
            Checks if a given rule is atomic.

        _derive_rules(self) -> list[Rule]:
            Derives new rules based on the existing rules in the argumentation framework recursively.

        _is_circular(self) -> bool:
            Checks for circular dependencies in the rules of the argumentation framework.

        __repr__(self) -> str:
            Returns a string representation of the ABA object, summarizing its attributes and relationships.
    """

    def __init__(self, language: set[str], assumptions: set[str], rules: list[Rule], 
                 contraries: list[Contrary], preferences: list):
        """
        Initializes the ABA object with language, assumptions, rules, contraries, and preferences.
        We also se arguments, attacks, normal attacks and reverse attacks to none as they are not computed until needed.

        Args:
            language (set[str]): A set of terms representing the language of the argumentation framework.
            assumptions (set[str]): A set of assumptions used in the argumentation.
            rules (list[Rule]): A list of rules defining relationships between arguments.
            contraries (list[Contrary]): A list of contrary relations between arguments.
            preferences (list): A list of preferences among arguments or assumptions.
        """
        self.language = language
        self.assumptions = assumptions
        self.rules = rules
        self.contraries = contraries
        self.preferences = preferences
        self.arguments = None
        self.attacks = None
        self.normal_attacks = None
        self.reverse_attacks = None

    def _get_literals_in_rules(self) -> set:
        """
        Retrieves all literals found in the defined rules.

        Returns:
            set: A set of literals extracted from the rules.
        """
        args_set = set()
        for rule in self.rules:
            args_set.add(rule.head)
            if isinstance(rule.body, tuple):
                args_set.update(rule.body)
            elif rule.body:
                args_set.add(rule.body)
        return args_set
    
    def _get_literals_in_preferences(self) -> set:
        """
        Retrieves all literals found in the defined preferences.

        Returns:
            set: A set of literals extracted from the preferences.
        """
        args_set = set()
        for pref in self.preferences:
            args_set.add(pref.least)
            args_set.add(pref.most)
        return args_set

    def _get_literals_in_contraries(self) -> set:
        """
        Retrieves all literals found in the defined contraries.

        Returns:
            set: A set of literals extracted from the contraries.
        """
        args_set = set()
        for contr in self.contraries:
            args_set.add(contr.contrary)
            args_set.add(contr.arg)
        return args_set
    
    def _is_valid(self) -> bool:
        """
        Checks if the argumentation framework is valid.
        We do so by making sure assumptions is a subset of langauge and is non empty.
        Additionally we also check that all literals specified in rules, contraries
        are part of the language and those in preferences are part of assumptions.

        Returns:
            bool: True if the framework is valid; False otherwise.
        """
        return (len(self.assumptions) > 0 and 
                self.assumptions.issubset(self.language) and 
                self._get_literals_in_contraries().issubset(self.language) and 
                self._get_literals_in_rules().issubset(self.language) and 
                self._get_literals_in_preferences().issubset(self.assumptions) if len(self.preferences) > 0 else True)
    
    def _is_atomic(self) -> bool:
        """
        Determines if all rules in the argumentation framework are atomic, meaning the body contains only assumptions.

        Returns:
            bool: True if all rules are atomic and the framework is valid; False otherwise.
        """
        values = []
        for rule in self.rules:
            values.append(self._is_atmomic_rule(rule))
        return self._is_valid() and all(values)
    
    def _is_atmomic_rule(self, rule) -> bool:
        """
        Checks if a given rule is atomic.
        A rule is atomic if all elements of its body are part of the given set of assumptions.

        Args:
            rule (Rule): The rule to check for atomicity.

        Returns:
            bool: True if the rule is atomic; False otherwise.
        """
        if rule.body != '':
            if isinstance(rule.body, tuple):
                return all(elem in self.assumptions for elem in rule.body)
            else:
                return rule.body in self.assumptions
        else:
            return True

    def _derive_rules(self) -> list[Rule]:
        """
        Derives new rules based on the existing rules in the argumentation framework recursively.
        This method allows us to create new rules that are results of the union between by replacing
        the body with the rule found if possible.

        Returns:
            list[Rule]: A list of derived rules.
        """
        # Create a deep copy of the current ABA object
        myaba = deepcopy(self)
        # Variable to track if any rules were changed
        changed = False
        # Iterate over each rule
        for i, rule1 in enumerate(myaba.rules):
            # If body is a tuple compare each element of its body with other rule heads
            # and if a match is found replace the element with the matching rule and mark the change
            if isinstance(rule1.body, tuple):
                new_body = list(rule1.body)
                for j, value in enumerate(rule1.body):
                    for k, rule2 in enumerate(myaba.rules):
                        if i != k and value == rule2.head:
                            new_body[j] = rule2
                            changed = True
                # Update the rule with new body if changes where made and derive anew
                if changed:
                    myaba.rules[i] = Rule((rule1.head, tuple(new_body)))
                    return myaba._derive_rules()
            # If body is a string then compare with other rules with other rule heads
            # and if a match is found update the rule and derive anew
            elif isinstance(rule1.body, str):
                for j, rule2 in enumerate(myaba.rules):
                    if i != j and rule1.body == rule2.head:
                        myaba.rules[i] = Rule((rule1.head, rule2))
                        return myaba._derive_rules()
        return myaba.rules

    def _is_circular(self) -> bool:
        """
        Checks for circular dependencies in the arguments of the framework.

        Returns:
            bool: True if circular dependencies are found; False otherwise.
        """
        # Derive rule to recursively create new rules by replacing the body if union of rule can be found and convert to paths
        # By converting to paths the aim is to get all paths from the head to the leaves
        derived_rules = [derived_rule.to_paths() for derived_rule in self._derive_rules()]
        # Iterate over each rule
        for rule in self.rules:
            # Check for rules containing assumptions in their body as those are what we will use to create arguments
            if (isinstance(rule.body, tuple) and 
                any(elem in self.assumptions for elem in rule.body)) or \
                (rule.body in self.assumptions):
                # If any derived rules exist
                if derived_rules:
                    # Check that for each of the derived rules there doesn't exist two different paths to the root (rule's head) by
                    # checking how many times it appears in the path and if it doesn't more than once then a circular dependency 
                    # was found
                    for derived_rule in derived_rules:
                        if not all(path.count(element) == 1 for path in derived_rule for element in path):
                            return True
        return False
   
    def __repr__(self):
        """
        Returns a string representation of the ABA object, summarizing its attributes and relationships.

        Returns:
            str: A summary of the ABA framework including language, assumptions, rules, contraries, 
                 preferences, arguments, and attacks.
        """
        return (
            f"Language : {self.language}\n"
            f"\nAssumptions : {self.assumptions}\n"
            f"\nRules:\n" + "\n".join(f"R{i}: {rule}" for i, rule in enumerate(self.rules)) + "\n" +
            f"\nContraries:\n" + "\n".join(f"C{i}: {contr}" for i, contr in enumerate(self.contraries)) + "\n" +
            f"\nPreferences:\n" + "\n".join(f"P{i}:{pref}" for i, pref in enumerate(self.preferences)) + "\n" +
            f"\nArguments:\n" + 
            ( "\n".join(f"A{i}: {arg}" for i, arg in enumerate(self.arguments) if arg is not None) + "\n" if self.arguments else "") +
            f"\nAttacks:\n" +
            ( "\n".join(str(attack) for attack in self.attacks if attack is not None) if self.attacks else "") +
            f"\nNormal Attacks:\n" +
            ( "\n".join(attack for attack in self.normal_attacks if attack is not None) if self.normal_attacks else "") +
            f"\nReverse Attacks:\n" +
            ( "\n".join(attack for attack in self.reverse_attacks if attack is not None) if self.reverse_attacks else "")
        )
