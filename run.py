import rng.vitals as c

keys = ['Race:','Gender:','Alignment:','Age:','Height:','Weight:','Stats:\tMethod I']
values = []
for i in range(0,7):
    values += [c.char[i]]
new_char = dict(zip(keys,values))
for key, value in new_char.items():
    print(f"{key}\n {value}")

import tables.abl_tbl as tbl

# str_tbl = tbl.str_tbl(stats[0])
# dex_tbl = tbl.dex_tbl(stats[1])
# con_tbl = tbl.con_tbl(stats[2])
# int_tbl = tbl.int_tbl(stats[3])
# wis_tbl = tbl.wis_tbl(stats[4])
# cha_tbl = tbl.cha_tbl(stats[5])
# tables = [str_tbl,dex_tbl,con_tbl,int_tbl,wis_tbl,cha_tbl]