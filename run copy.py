import RNG.vitals as c

stats = c.char[6]
library = ['Race\t','Gender\t','Align\t','Age\t','Height\t','Weight\t']
print("Name\t")

for i in range(0,6):
    print(library[i],c.char[i])

print('Stats\t','-Method I-\n',stats)
import tables.abl_tbl as tbl

str_tbl = tbl.str_tbl(stats[0])
dex_tbl = tbl.dex_tbl(stats[1])
# con_tbl = tbl.con_tbl(stats[2])
# int_tbl = tbl.int_tbl(stats[3])
# wis_tbl = tbl.wis_tbl(stats[4])
# cha_tbl = tbl.cha_tbl(stats[5])
tables = [str_tbl,dex_tbl]#,con_tbl,int_tbl,wis_tbl,cha_tbl