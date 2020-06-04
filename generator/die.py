from random import randint

class Die:

    def __init__(self, sides=6):
        sides = int(sides)
        if "d" in str(sides):
            dice = sides.split("d")
        else:
            if sides > 0:
                self.sides = int(sides)
            else:
                raise Exception("Can only create a die with positive number of sides")
    

    def roll(self, amount=1):
        """ Rolls amount of dice and adds them together
            Rolls 1 die if no argument is given """
        amount = int(amount)
        if amount == 1:
            return randint(1, self.sides)
        elif amount < 1:
            raise Exception("Cannot roll a negative number of dice")
        else:
            result = 0
            for _ in range(amount):
                result += randint(1, self.sides)
            return result


if __name__ == "__main__":
    d4 = Die(4)
    d6 = Die(6)
    d8 = Die(8)
    d10 = Die(10)
    d12 = Die(12)
    d20 = Die(20)
    for i in range(100):
        stat = d6.roll(3)
        if stat > 16:
            print(stat)