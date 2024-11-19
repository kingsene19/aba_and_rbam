from helpers.language import Language
from helpers.rule import Rule
from helpers.assumption import Assumption
from helpers.contrary import Contrary
from helpers.aba import ABA
from helpers.argument import Argument
from helpers.attack import Attack
from helpers.preference import Preference
from enum import Enum
import threading

class ConvertTo(Enum):
    """Enumeration for conversion types.

    This enum defines the possible conversion types that can be used
    when performing conversions in the application.

    Attributes:
        ATOMIC (str): Represents atomic conversion.
        NON_CIRCULAR (str): Represents non-circular conversion.
    """
    ATOMIC = 'atomic'
    NON_CIRCULAR = 'non_circular'

class ConversionFailedError(Exception):
    """Exception raised when a conversion fails.

    Attributes:
        message (str): Error message indicating a failure in conversion.
    """

    def __init__(self, message="There was something wrong during conversion"):
        self.message = message
        super().__init__(self.message)


class ConversionNotNeededError(Exception):
    """Exception raised when a conversion is not needed.

    Attributes:
        message (str): Error message indicating that no conversion is needed.
    """

    def __init__(self, message="No conversion needed"):
        self.message = message
        super().__init__(self.message)

class ABA_Generator:
    """
        Class for generating Argument-Based Argumentation (ABA) frameworks.

        The ABA_Generator class provides static methods to create and manipulate ABA frameworks
        based on defined languages, assumptions, rules, contraries, and preferences. It also allows 
        for conversions to atomic and non-circular forms, as well as the generation of arguments 
        and attack relations.

        Methods:
            create_aba_framework(language: str, assumptions: str, rules: str, contraries: str, preferences: Optional[str] = None) -> ABA
                Creates an ABA framework from the provided parameters

            convert_to_atomic(language: str, assumptions: str, rules: str, contraries: str, preferences: Optional[str] = None) -> ABA
                Converts the ABA framework to an atomic form if it isn't already

            convert_to_non_circular(language: str, assumptions: str, rules: str, contraries: str, preferences: Optional[str] = None) -> ABA
                Converts the framework to a non-circular form, modifying rules as necessary

            convert_first(language: str, assumptions: str, rules: str, contraries: str, preferences: Optional[str] = None, convert_to: ConvertTo | None = None) -> ABA
                Converts the framework to atomic or non-circular based on the value provided, if None then just create the normal ABA framework

            create_arguments(language: str, assumptions: str, rules: str, contraries: str, preferences: Optional[str] = None, convert) -> ABA
                Generates arguments based on the assumptions and derived rules within the framework

            create_attacks(language: str, assumptions: str, rules: str, contraries: str, preferences: Optional[str] = None) -> ABA
                Establishes attack relations among the arguments based on contraries

            create_normal_reverse_attacks(language: str, assumptions: str, rules: str, contraries: str, preferences: Optional[str] = None) -> ABA
                Computes normal and reverse attacks based on preferences among subsets of assumptions
    """

    @staticmethod
    def create_aba_framework(language: str, assumptions: str, rules: str, contraries:str, preferences: str|None = None) -> ABA:
        """
            Creates an ABA framework from the provided parameters.

            Args:
                language (str): A string representing the literals of the language in the framework
                assumptions (str) : A string representing the literals of the assumptions in the framework
                rules (str) : A string representing the rules in the framework
                contraries (str) : A string representing the contraries in the framework
                preferences (Optional[str]): An optional string representing preferences in the framework

            Returns:
                ABA: An ABA object representing the framework

            Raises
                ConversionFailedError: If the framework generated is invalid
        """
        # Parse the inputs into structured format using the corresponding parser and create the set of language
        # and assumptions
        language = Language(language).parse()
        assumptions = Assumption(assumptions).parse()
        # Create a list of Rule objects by parsing each rule string using the Rule class
        rules = [Rule(rule) for rule in Rule.parser(rules)]
        # Create a list of Contrary objects by parsing each contrary string using the Contrary class
        contraries = [Contrary(contr) for contr in Contrary.parser(contraries)]
        # Check if preferences are provided if so, parse them into a list of Preference objects and if not return an empty list
        if preferences is not None:
            preferences = [Preference(pref) for pref in Preference.parser(preferences)]
        else:
            preferences = []
        aba = ABA(language, assumptions, rules, contraries, preferences)
        # Check if the framework generated is valid, if not raise a ConversionFailedError
        if not aba._is_valid():
            raise ConversionFailedError("Invalid literals detected in the ABA framework.")
        return aba
        
    @staticmethod
    def convert_to_atomic(language: str, assumptions: str, rules: str, contraries:str, preferences: str|None = None) -> ABA:
        """
            Converts the ABA framework to an atomic form if it isn't already.

            Args:
                language (str): A string representing the literals of the language in the framework
                assumptions (str): A string representing the literals of the assumptions in the framework
                rules (str): A string representing the rules in the framework
                contraries (str): A string representing the contraries in the framework
                preferences (Optional[str]): An optional string representing preferences in the framework

            Returns:
                ABA: The modified ABA object if conversion was necessary

            Raises:
                ConversionNotNeededError: If the ABA framework is already atomic
                ConversionFailedError: If the conversion to atomic failed
        """
        # Create the corresponding ABA framework
        aba = ABA_Generator.create_aba_framework(language, assumptions, rules, contraries, preferences)
        # If the ABA is circular the start by converting it to a non circular framework first
        if aba._is_circular():
            aba = ABA_Generator.convert_to_non_circular(language, assumptions, rules, contraries, preferences)
        # If the ABA is already atomic then raise a ConversionNotNeededError; if not
        if not aba._is_atomic():
            # Initialize a set to store new literals to be added
            to_add = set()
            # Iterate over each literal in the language
            for l in aba.language:
                # If the literal is not assumption, generate new literals with "_d" and "_nd" suffixes to add as well as the contrary relations
                if not l in aba.assumptions:
                    to_add.add(f"{l}_d")
                    to_add.add(f"{l}_nd")
                    aba.contraries.append(Contrary((f"{l}_d",f"{l}_nd")))
                    aba.contraries.append(Contrary((f"{l}_nd",f"{l}")))
            # Update the language and assumptions with the new literals
            aba.language.update(to_add)
            aba.assumptions.update(to_add)
            # Update the body of each rule to include the new literals
            for rule in aba.rules:
                if isinstance(rule.body, tuple):
                    rule.body = tuple(f"{s}_d" if s and not s in aba.assumptions else s for s in rule.body)
                else:
                    s = rule.body
                    rule.body = f"{s}_d" if s and not s in aba.assumptions else s
            # Check again if the ABA framework is atomic after updates and if not raise a ConversionFailedError, if so return it
            if not aba._is_atomic():
                raise ConversionFailedError("There was something wrong during conversion")
            else:
                return aba
        else:
            raise ConversionNotNeededError("ABA Framework is already atomic no conversion needed")

    @staticmethod
    def convert_to_non_circular(language: str, assumptions: str, rules: str, contraries:str, preferences: str|None = None) -> ABA:
        """
            Converts the ABA framework to a non-circular form if it is circular.

            Args:
                language (str): A string representing the literals of the language in the framework
                assumptions (str): A string representing the literals of the assumptions in the framework
                rules (str): A string representing the rules in the framework
                contraries (str): A string representing the contraries in the framework
                preferences (Optional[str]): An optional string representing preferences in the framework

            Returns:
                ABA: The modified ABA object if conversion was necessary.

            Raises:
                ConversionNotNeededError: If the ABA framework is already non circular
                ConversionFailedError: If the conversion to non circular failed
        """
        # Create the corresponding ABA framework
        aba = ABA_Generator.create_aba_framework(language, assumptions, rules, contraries, preferences)
        # If the ABA is already atomic then raise a ConversionNotNeededError; if not
        if aba._is_circular():
            # Determine the number of literals in the language that are not assumptions k =|L\A|
            k = len(aba.language.difference(aba.assumptions))
            new_rules = []
            to_add = set()
            # Iterate over each rule in the existing ABA framework
            for rule in aba.rules:
                # If the current rule is atomic then generate new rules by appending indices to the head of atomic rules
                if aba._is_atmomic_rule(rule):
                    for i in range(1, k+1):
                        if i != k:
                            new_rules.append(Rule((f"{rule.head}{i}", rule.body)))
                            to_add.add(f"{rule.head}{i}")
                        else:
                            new_rules.append(Rule((f"{rule.head}", rule.body)))
                else:
                    # If the rule is not atomic, generate new rules for its body
                    for i in range(2, k+1):
                        new_body = list(rule.body)
                        for j, elem in enumerate(new_body):
                            if not elem in aba.assumptions:
                                new_body[j] = f"{elem}{i-1}"
                                to_add.add(f"{elem}{i-1}")
                        new_body = tuple(new_body) if len(new_body) > 1 else new_body[0]
                        if i != k:
                            new_rules.append(Rule((f"{rule.head}{i}", new_body)))
                            to_add.add(f"{rule.head}{i}")
                        else:
                            new_rules.append(Rule((f"{rule.head}", new_body)))
            # Update the language and rules in the ABA framework
            aba.language.update(to_add)
            aba.rules = new_rules
            # Check again if the ABA framework is circular after updates and if not raise a ConversionFailedError, if so return it
            if aba._is_circular():
                raise ConversionFailedError("There was something wrong during conversion")
            else:
                return aba
        else:
            raise ConversionNotNeededError("ABA Framework is already non circular no conversion needed")
        

    @staticmethod
    def _convert_first(language: str, assumptions: str, rules: str, contraries:str, preferences: str|None = None, convert_to: ConvertTo | None = None) -> ABA:
        """
            Converts the framework to atomic or non-circular based on the value provided, if None then just create the normal ABA framework

            Args:
                language (str): A string representing the literals of the language in the framework
                assumptions (str) : A string representing the literals of the assumptions in the framework
                rules (str) : A string representing the rules in the framework
                contraries (str) : A string representing the contraries in the framework
                preferences (Optional[str]): An optional string representing preferences in the framework
                convert_to (Optional[ConvertTo]) : An optional ConvertTo to specify a conversion to apply

            Returns:
                ABA: An ABA object representing the framework
        """
        # Check if conversion to atomic was asked for and if so convert it first 
        if convert_to == ConvertTo.ATOMIC:
            try:
                aba = ABA_Generator.convert_to_atomic(language, assumptions, rules, contraries, preferences)
            # If the aba is already atomic then just create the normal framework
            except ConversionNotNeededError:
                print("Here")
                aba = ABA_Generator.create_aba_framework(language, assumptions, rules, contraries, preferences)
        else:
            # Check if conversion to non circular was asked and if so convert it first
            if convert_to == ConvertTo.NON_CIRCULAR:
                try:
                    aba = ABA_Generator.convert_to_non_circular(language, assumptions, rules, contraries, preferences)
                # If the aba is already circular then just create the normal framework
                except ConversionNotNeededError:
                    aba = ABA_Generator.create_aba_framework(language, assumptions, rules, contraries, preferences)
            # By default just create the normal framework
            else:
                aba = ABA_Generator.create_aba_framework(language, assumptions, rules, contraries, preferences)
        return aba
    
    @staticmethod
    def create_arguments(language: str, assumptions: str, rules: str, contraries:str, preferences: str|None = None, convert_to: ConvertTo | None = None) -> ABA:
        """
            Creates arguments for the ABA framework based on the derived rules.

            Args:
                language (str): A string representing the literals of the language in the framework
                assumptions (str): A string representing the literals of the assumptions in the framework
                rules (str): A string representing the rules in the framework
                contraries (str): A string representing the contraries in the framework
                preferences (Optional[str]): An optional string representing preferences in the framework
                convert_to (Optional[ConvertTo]) : An optional ConvertTo to specify a conversion to apply

            Returns:
                ABA: The ABA object with generated arguments
        """
        # Convert the framework if neeed
        aba = ABA_Generator._convert_first(language, assumptions, rules, contraries, preferences, convert_to)
        # Derive new rules from the ABA framework and convert them into paths this allows us to get all the claims and leaves
        derived_rules = [derived_rule.to_paths() for derived_rule in aba._derive_rules()]
        pairs = []
        # Iterate over each derived rule and its paths and add for each path create the dictionary with head and leaf
        for derived_rule in derived_rules:
            for path in derived_rule:
                pairs.append({path[0]: path[-1]})
        result = {}
        # Process each pair and for each key in the pair if it appears in multiple dictionaries then create turn the value
        # into a tuple containing all the values of it is a key for
        for d in pairs:
            for key, value in d.items():
                if key in result:
                    if not isinstance(result[key], tuple):
                        result[key] = (result[key],)
                    result[key] += (value,)
                else:
                    result[key] = value
        myargs = []
        # Iterate through the result dictionary to create arguments by only keeping the element in the value that are in assumptions
        # or correspond to the empty string
        for key, value in result.items():
            if isinstance(value, tuple):
                new_leaves = ()
                for l in value:
                    if l in aba.assumptions:
                        new_leaves = new_leaves + (l,)
                myargs.append(Argument(key, new_leaves))
            else:
                if value in aba.assumptions or value == '':
                    myargs.append(Argument(key, (value,)))
        # Add all assumptions as arguments
        for assump in aba.assumptions:
            if not Argument(assump, (assump,)) in myargs:
                myargs.append(Argument(assump, (assump,)))
        # Assign the constructed arguments to the ABA framework and return it
        aba.arguments = myargs
        return aba

    @staticmethod
    def create_attacks(language: str, assumptions: str, rules: str, contraries:str, preferences: str|None = None, convert_to: ConvertTo | None = None) -> ABA:
        """
            Establishes attack relations among the arguments based on contraries.

            Args:
                language (str): A string representing the literals of the language in the framework
                assumptions (str) : A string representing the literals of the assumptions in the framework
                rules (str) : A string representing the rules in the framework
                contraries (str) : A string representing the contraries in the framework
                preferences (Optional[str]): An optional string representing preferences in the framework
                convert_to (Optional[ConvertTo]) : An optional ConvertTo to specify a conversion to apply

            Returns:
                ABA: An ABA object representing the framework with attacks computed
        """
        # Generate the argument for the ABA framework
        aba = ABA_Generator.create_arguments(language, assumptions, rules, contraries, preferences, convert_to)
        attacks = []
        contraries = Contrary.to_dict(aba.contraries)
        # Iterate over each argument in the ABA framework
        for i, arg in enumerate(aba.arguments):
            for j, other_arg in enumerate(aba.arguments):
                # Check if the claim of the current argument has any contraries in the leaves of the other argument and if so add an attack
                if any(arg.claim in contraries[elem] for elem in other_arg.leaves if elem in contraries):
                    attacks.append(Attack(i,j))
        # Assign the constructed attacks to the ABA framework and return it
        aba.attacks = attacks
        return aba
    
    @staticmethod
    def create_normal_reverse_attacks(language: str, assumptions: str, rules: str, contraries: str, preferences: str | None = None, convert_to: ConvertTo | None = None) -> ABA:
        """
        Creates normal and reverse attacks for the ABA framework based on preferences.

        Args:
            language (str): A string representing the literals of the language in the framework
            assumptions (str): A string representing the literals of the assumptions in the framework
            rules (str): A string representing the rules in the framework
            contraries (str): A string representing the contraries in the framework
            preferences (Optional[str]): An optional string representing preferences in the framework
            convert_to (Optional[ConvertTo]) : An optional ConvertTo to specify a conversion to apply

        Returns:
            ABA: The ABA object with generated normal and reverse attacks.

        Raises:
            ValueError: If no preferences are specified.
            TimeoutError: If the attacks are taking too long to compute this can be due to the set of assumptions being very large.
        """

        # Target function to run the computation in order to raise TimeoutError
        def run_computation():
            # Create arguments for the ABA framework using the specified components
            aba = ABA_Generator.create_arguments(language, assumptions, rules, contraries, preferences, convert_to)
            # Check if any preferences are specified and raise a ValueError if not
            if len(aba.preferences) == 0:
                raise ValueError("No preferences specified; cannot compute.")
            # Get all subsets of the assumptions
            subsets = Assumption.get_subsets(aba.assumptions)
            # Convert contraries and preferences into dictionary format for easier lookup
            contraries_dict = Contrary.to_dict(aba.contraries)
            preferences_dict = Preference.to_dict(aba.preferences)
            normal_attacks = []
            reverse_attacks = []
            # Iterate through each subset of assumptions
            for subset in subsets:
                for other_subset in subsets:
                    for arg in aba.arguments:
                        # Check if the argument's leaves are a subset of the current subset
                        if set(arg.leaves).issubset(set(subset)):
                            for y in other_subset:
                                if y in contraries_dict:
                                    # Check if the argument's claim has a contrary in the other subset
                                    if arg.claim in contraries_dict[y]:
                                        # Ensure no preferences exist for y in the leaves of the argument and if so add as a normal attack
                                        if not any(y in preferences_dict[x] for x in arg.leaves if x in preferences_dict):
                                            normal_attacks.append(f"{subset} -> {other_subset}")
                        # Check if the argument's leaves are a subset of the other subset
                        if set(arg.leaves).issubset(set(other_subset)):
                            for x in subset:
                                if x in contraries_dict:
                                    # Check if the argument's claim has a contrary in the current subset
                                    if arg.claim in contraries_dict[x]:
                                        # Ensure preferences exist for x in the leaves of the argument and if so add as reverse attack
                                        if any(x in preferences_dict[y] for y in arg.leaves if y in preferences_dict):
                                            reverse_attacks.append(f"{subset} -> {other_subset}")
            # Assign the constructed attacks to the ABA framework
            aba.normal_attacks = list(set(normal_attacks))
            aba.reverse_attacks = list(set(reverse_attacks))
            return aba
        # Create a thread to run the computation and wait for it complete with a timeout of 1 minute
        computation_thread = threading.Thread(target=run_computation)
        computation_thread.start()
        computation_thread.join(timeout=60)
        if computation_thread.is_alive():
            raise TimeoutError("Attacks are taking too long to compute this can be due to the set of assumptions being very large..")
        # If the thread completed we simply return the result
        return run_computation()
