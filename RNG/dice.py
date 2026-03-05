import random
## Dice Set
def d(sides):
    if sides == 100:
        d10s = random.randint(0,9)*10
        d10 = random.randint(1,10)
        if d10s == 0:
            if d10 == 10:
                d = 100
            else:
                d = d10
        else:
            d = d10s+d10
    else:
        d = random.randint(1,sides)
    return d