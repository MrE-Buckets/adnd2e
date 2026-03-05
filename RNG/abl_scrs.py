from .dice import d

def base():
    stat = []
    for i in range(6):
        stat += [sum([d(6),d(6),d(6)])]
    return stat

def racial_adjust(base,race):
    adj = ([0,0,1,0,-1,0],[0,1,-1]+[0]*3,[0]*4+[-1,1],[0]*6,[-1,1]+[0]*4,[0]*6)
    race_adj = adj[race]
    for i in range(0,6):
        base[i] += race_adj[i]
    return base

limits = (
((8,18),(3,17),(12,19),(3,18),(2,17),(3,17)),
((3,18),(7,19),(6,17),(8,18),(3,18),(8,18)),
((6,18),(3,18),(8,18),(6,18),(2,17),(4,19)),
((3,18),(6,18),(6,18),(4,18),(3,18),(3,18)),
((6,17),(8,19),(10,18),(6,18),(3,17),(3,18)),
((3,18),(3,18),(3,18),(3,18),(3,18),(3,18))
)

def stats(race):
    n = 6
    while n != 0:
        new = base()
        block = racial_adjust(new,race)         
        for i in range(0,n):           
            roll = block[i]
            if roll not in range(limits[race][i][0],limits[race][i][1]):
                n = 6
                break
            n -= 1  
    if block[0] == 18 and race != 4:
        block[0] = [roll,d(100)] 
    return block