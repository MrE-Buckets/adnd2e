import random as rand
## Dice Set
def d(sides):
    if sides == 100:
        res = rand.randint(0,9)*10+rand.randint(1,10)
    else:
        res = rand.randint(1,sides)
    return res