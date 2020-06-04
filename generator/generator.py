
import json
from re import findall
from random import choice, random

from die import Die

class Generator():
    def __init__(self, data):
        self.data = data


    def generate(self, key):
        # Generates a result from the gen data dictionary at key
        if self.is_dataentry(key):
            string = self.select(self.data[key])
            if string:
                return self.expand_tokens(string)
        elif self.is_dieroll(key):
            return self.dieroll(key)
        else:
            return ''
    
    def expand_tokens(self, phrase):
        # Replaces {token} in phrase
        tokens = findall(r"{([\w\s]+)}", phrase)
        for token in tokens:
            replacement = self.generate(token)
            if replacement:
                phrase = phrase.replace('{'+token+'}',replacement)
            else:
                phrase = phrase.replace('{'+token+'}',token)
        return phrase
    

    # DIE FUNCTIONS

    def is_dieroll(self, key):
        # Checks if key is a string with exactly 2 numbers separated by a "d"
        matches = findall(r"(\d+)(d)(\d+)",key)
        if len(matches) == 1:
            if len(matches[0]) == 3 and len("".join(matches[0])) == len(key):
                n_of, separator, sides = matches[0]
                if n_of.isdigit() and separator == "d" and sides.isdigit():
                    return True
        return False

    def dieroll(self, key):
        # Gives the result of the roll for a given dice string (such as "5d6")
        matches = findall(r"(\d+)(d)(\d+)",key)
        n_of, _, sides = matches[0]
        return str(Die(sides).roll(n_of))
    

    # JSON FUNCTIONS

    def is_dataentry(self, key):
        # Checks if a data definition exists for the given key
        if key in self.data.keys():
            return True
        return False

    def select(self, data):
        if isinstance(data, list):
            return self.select_from_list(data)
        elif isinstance(data, dict):
            return self.select_from_dict(data)
        return False

    def select_from_list(self, list_data):
        # Pick a random entry from list
        return choice(list_data)
    
    def select_from_dict(self, entry_dict):
        # 
        length = self.entry_dict_range(entry_dict)
        if length:
            idx = int(random() * length) + 1
            for key in entry_dict:
                key_range = self.rangeify(key)
                if (idx >= key_range[0] and idx <= key_range[1]):
                    return entry_dict[key]
        return ''

    def entry_dict_range(self, entry_dict):
        # Finds the largest number among the ranges of an entry table
        key_ranges = [list(self.rangeify(key)) for key in entry_dict]
        return max(key_ranges)[1]

    def rangeify(self, key):
        # Turns range substrings like 1-10 into an equivalent tuple: (1,10)
        match = findall(r"(\d+)-(\d+)",key)
        if match:
            return (int(match[0][0]), int(match[0][1]))
        return (int(key), int(key))


if __name__ == "__main__":
    # Import data
    json_file = open("assets/geas.json","r")
    data = json.load(json_file)
    
    # Create generator
    generator = Generator(data)

    # Print a result
    print(generator.generate("geas_test"))
