from sys import argv
from json import load

from generator import Generator

if __name__ == "__main__":
    if len(argv) > 1:
        user_input = argv[1]
    else:
        user_input = "geas"
    
    # Import data
    json_file = open("assets/%s.json"%user_input,"r")
    data = load(json_file)
    
    # Create generator
    generator = Generator(data)

    # Print a result
    print(generator.generate("geas"))