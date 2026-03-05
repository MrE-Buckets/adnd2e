from .dice import d

## Race
def race(n):
    option = ('Dwarf','Elf','Gnome','Half-Elf','Halfling','Human')
    return option[n]
## Gender
def gender(n):
    option = ["Male","Female"]
    return option[n]
## Alignment
def alignment(o,m):
    order = ["Lawful","Neutral","Chaotic"]
    morality = ["Good","Neutral","Evil"]
    if o == 1 and m == 1:
        return "True Neutral"
    else:
        return order[o]+" "+morality[m]
## Age
def age(race):
    base = [40,100,60,15,20,15]
    mod = [d(6)*5,d(6)*5,d(12)*3,d(6),d(4)*3,d(4)]
    return f'{base[race]+mod[race]} Years Old'
## Height
def height(race,gender):
    base = [[43,41],[55,50],[38,36],[60,58],[32,30],[60,59]]
    base = base[race][gender]
    mod = [d(10),d(10),d(6),(d(6)*2),(d(8)*2),(d(10)*2)]
    mod = mod[race]
    feet = (base+mod)//12
    inch = (base+mod)%12
    # Quote marks ' and " mixed and matched for feet and inches
    if inch == 0:
        return f"{feet}'"
    else:
        return f"{feet}'"f'{inch}"'           
## Weight
def weight(race,gender):
    base = [[130,105],[90,70],[72,68],[110,85],[52,48],[140,100]]
    base = base[race][gender]
    mod = [d(10)*4,d(10)*3,d(4)*5,d(12)*3,d(4)*5,d(10)*6]
    mod = mod[race]
    return f'{base+mod} lbs'