
from re import findall
from parser import expr, compilest
from random import choice, random

from die import Die


class Generator():
    def __init__(self, data):
        self.data = data

    def generate(self, key):
        # Generates a result from the gen data dictionary at key
        if self.is_randomtable(key):
            random_table = self.data[key]
            if isinstance(random_table, list):
                text = choice(random_table)
            elif isinstance(random_table, dict):
                text = self.select_from_dict(random_table)
            return self.replace_keys(text)
        elif self.is_dieroll(key):
            return self.dieroll(key)
        else:
            return key

    # RANDOM TABLE FUNCTIONS

    def is_randomtable(self, key):
        # Checks if a data definition exists for the given key
        if key in self.data.keys():
            return True
        return False
    
    def replace_keys(self, text):
        # Replaces {key} in text
        keys = findall(r"{([\w\s()+\-*\/]+)}", text)
        for key in keys:
            text = text.replace('{'+key+'}',self.generate(key))
        return text

    def select_from_dict(self, entry_dict):
        # Pick a random entry from dictionary weighted in keys
        length = max([list(self.rangeify(k)) for k in entry_dict])[1]
        if length:
            idx = int(random() * length) + 1
            for key in entry_dict:
                key_range = self.rangeify(key)
                if (idx >= key_range[0] and idx <= key_range[1]):
                    return entry_dict[key]
        return ''

    def rangeify(self, key):
        # Turns range substrings like 1-10 into an equivalent tuple: (1,10)
        match = findall(r"(\d+)-(\d+)",key)
        if match:
            return (int(match[0][0]), int(match[0][1]))
        return (int(key), int(key))

    # DIE FUNCTIONS

    def is_dieroll(self, key):
        # Checks if key is a string with die notation
        matches = findall(r"(\d+)(d)(\d+)",key)
        # At least one match and only die notation
        if len(matches) > 0 and all([c in "d0123456789()+-*/" for c in key]):
            # Each match is exactly 3 groups
            if all([len(m) == 3 for m in matches]):
                # Each match matches properties for a die (sides amount etc.)
                if all([m[0].isdigit() and m[1]=="d" and m[2].isdigit()] for m in matches):
                    return True
        return False

    def dieroll(self, key):
        # Gives the result of the roll for a given dice string (such as "5d6")
        matches = findall(r"(\d+)(d)(\d+)",key)
        for match in matches:
            n_of, _, sides = list(match)
            roll_result = str(Die(sides).roll(n_of))
            key = key.replace("".join(match), roll_result)
        result = self.math_parse(key)
        return result
    
    def math_parse(self, expression):
        return str(eval(expr(expression).compile()))
    

if __name__ == "__main__":
    # Import data
    from json import load
    json_file = open("assets/geas.json","r")
    data = load(json_file)
    
    # Create generator
    generator = Generator(data)

    # Print a result
    print(generator.generate("test"))
