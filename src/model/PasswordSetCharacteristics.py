import json

from charclass import count_classes, count_words, count_lowers, count_uppers, count_digits, count_symbols

class PasswordSetCharacteristics:
    """ Represents the characteristics of a set of passwords.
    """

    def __init__ (self):
        """ Constructs a new instance of a representation of the characteristics of a set of passwords.
        """
        self.lengths = {}
        self.lower_counts = {}
        self.upper_counts = {}
        self.digit_counts = {}
        self.symbol_counts = {}
        self.class_counts = {}
        self.word_counts = {}

    @staticmethod
    def max_key (dict):
        """ Gets the maximum key from a dictionary.

        Args:
            dict (dict): The input dictionary.
        Returns:
            int: The maximum key.
        """
        output = -1
        for key, value in dict.items():
            output = max(output, key)
        return output

    @classmethod
    def accumulate (cls, dict, inverse=False):
        """ Turns a discrete count dictionary into a cumulative one.

        Args:
            dict (dict): The count dictionary.
        Returns:
            dict: The cumulative dictionary.
        """
        total = 0
        output = {}
        keys = range(0, cls.max_key(dict) + 1)
        if inverse:
            keys = range(cls.max_key(dict), -1, -1) # Invert range if needed.
        for i in keys:
            if i in dict:
                total += dict[i] # Accumulate frequencies.
            output[i] = total
        return output

    @staticmethod
    def to_num_dict (dict):
        """ Converts a string-indexed dictionary to a numerically-indexed one.

        Args:
            dict (dict): The dictionary to convert.
        Returns:
            dict: The converted dictionary.
        """
        output = {}
        for key, value in dict.items():
            output[int(key)] = value
        return output

    @classmethod
    def load (cls, file):
        """ Loads a password set characteristics object from a file.

        Args:
            file (str): The filepath from which to load the object.
        Returns:
            PasswordSetCharacteristics: The loaded object.
        """
        with open(file) as f:
            raw = json.load(f)
            obj = PasswordSetCharacteristics()
            obj.lengths = cls.to_num_dict(raw['lengths'])
            obj.lower_counts = cls.to_num_dict(raw['lowerCounts'])
            obj.upper_counts = cls.to_num_dict(raw['upperCounts'])
            obj.digit_counts = cls.to_num_dict(raw['digitCounts'])
            obj.symbol_counts = cls.to_num_dict(raw['symbolCounts'])
            obj.class_counts = cls.to_num_dict(raw['classCounts'])
            obj.word_counts = cls.to_num_dict(raw['wordCounts'])
            return obj

    def to_dict (self):
        """ Transforms this object into a dictionary for JSON serialization.

        Returns:
            dict: The transformed object.
        """
        return {
            'lengths': self.lengths,
            'lowerCounts': self.lower_counts,
            'upperCounts': self.upper_counts,
            'digitCounts': self.digit_counts,
            'symbolCounts': self.symbol_counts,
            'classCounts': self.class_counts,
            'wordCounts': self.word_counts
        }

    def get (self, key, accum=False, inverse=False):
        """ Gets a frequency dictionary by its key.

        Args:
            key (str): The key of the frequency dictionary to get.
            accum (bool): Whether or not to convert the frequency dictonary to cumulative frequency before returning.
            inverse (bool): Whether to use inverse cumulative frequency.
        Returns:
            dict: The frequency dictionary.
        """
        lookup = self.to_dict()
        if accum:
            out = self.accumulate(lookup[key], inverse)
            return out
        else:
            return lookup[key]

    def add (self, pwd, freq):
        """ Adds a password into this password characteristics object, recording its properties.

        Args:
            pwd (str): The password to add.
            freq (int): The frequency of the password to add.
        """
        # Record password lengths.
        pwd_len = len(pwd)
        if not pwd_len in self.lengths:
            self.lengths[pwd_len] = 0
        self.lengths[pwd_len] += freq

        # Record password lowercase letter counts.
        pwd_lowers = count_lowers(pwd)
        if not pwd_lowers in self.lower_counts:
            self.lower_counts[pwd_lowers] = 0
        self.lower_counts[pwd_lowers] += freq

        # Record password uppercase letter counts.
        pwd_uppers = count_uppers(pwd)
        if not pwd_uppers in self.upper_counts:
            self.upper_counts[pwd_uppers] = 0
        self.upper_counts[pwd_uppers] += freq

        # Record password digit counts.
        pwd_digits = count_digits(pwd)
        if not pwd_digits in self.digit_counts:
            self.digit_counts[pwd_digits] = 0
        self.digit_counts[pwd_digits] += freq

        # Record password symbol counts.
        pwd_symbols = count_symbols(pwd)
        if not pwd_symbols in self.symbol_counts:
            self.symbol_counts[pwd_symbols] = 0
        self.symbol_counts[pwd_symbols] += freq

        # Record password chaacter class counts.
        pwd_classes = count_classes(pwd)
        if not pwd_classes in self.class_counts:
            self.class_counts[pwd_classes] = 0
        self.class_counts[pwd_classes] += freq

        # Record password word counts.
        pwd_words = count_words(pwd)
        if not pwd_words in self.word_counts:
            self.word_counts[pwd_words] = 0
        self.word_counts[pwd_words] += freq
