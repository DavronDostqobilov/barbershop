from tinydb import TinyDB, Query
baza_db = TinyDB('test.json', indent=4)
task_table = baza_db.table('Task')
query = Query()
all_time = [8,9,10,11,12,1,2,3,4,5,6,7,8]
x=task_table.all()
print(task_table.all())
for i in x:
    k=i['datetime']
    if k in all_time:
        all_time.remove(k)
print(all_time)