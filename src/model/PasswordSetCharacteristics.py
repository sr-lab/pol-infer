import json

from charclass import count_classes, count_words, count_lowers, count_uppers, count_digits, count_symbols

class PasswordSetCharacteristics:
    """ Represents the characteristics of a set of passwords.
    """

    def __init__(self):
        """ Constructs a new instance of a representation of the characteristics of a set of passwords.
        """
        self.lengths = {}
        self.lower_counts = {}
        self.lower_counts_cumulative = {}
        self.upper_counts = {}
        self.upper_counts_cumulative = {}
        self.digit_counts = {}
        self.digit_counts_cumulative = {}
        self.symbol_counts = {}
        self.symbol_counts_cumulative = {}
        self.class_counts = {}
        self.word_counts = {}
        self.num_with_lowers = 0
        self.num_with_uppers = 0
        self.num_with_digits = 0
        self.num_with_symbols = 0

    def max_key(self, dict):
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

    def accumulate(self, dict):
        """ Turns a discrete count dictionary into a cumulative one.

        Args:
            dict (dict): The count dictionary.
        Returns:
            dict: The cumulative dictionary.
        """
        total = 0
        output = {}
        for i in range(0, self.max_key(dict) + 1):
            if i in dict:
                total += dict[i]
            output[i] = total
        return output

    def dict(self):
        """ Transforms this object into a dictionary for JSON serialization.

        Returns:
            dict: The transformed object.
        """
        return {
            'lengths': self.lengths,
            'lengthsAccum': self.accumulate(self.lengths),
            'lowerCounts': self.lower_counts,
            'lowerCountsAccum': self.accumulate(self.lower_counts),
            'upperCounts': self.upper_counts,
            'upperCountsAccum': self.accumulate(self.upper_counts),
            'digitCounts': self.digit_counts,
            'digitCountsAccum': self.accumulate(self.digit_counts),
            'symbolCounts': self.symbol_counts,
            'symbolCountsAccum': self.accumulate(self.symbol_counts),
            'classCounts': self.class_counts,
            'wordCounts': self.word_counts,
            'containing': {
                'lowers': self.num_with_lowers,
                'uppers': self.num_with_uppers,
                'digits': self.num_with_digits,
                'symbols': self.num_with_symbols,
            },
        }

    def load(self, pwd, freq):
        """ Loads a password into this password characteristics object, recording its properties.

        Args:
            pwd (str): The password to load.
            freq (int): The frequency of the password to load.
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

        # Update contains-class counts.
        if pwd_lowers > 0:
            self.num_with_lowers += freq
        if pwd_uppers > 0:
            self.num_with_uppers += freq
        if pwd_digits > 0:
            self.num_with_digits += freq
        if pwd_symbols > 0:
            self.num_with_symbols += freq
