from tinydb import TinyDB, Query
from datetime import datetime

class UserDB:
    def __init__(self):
        user_db = TinyDB('db/users.json', indent=4)
        baza_db = TinyDB('db/baza.json', indent=4)
        
        self.user_table = user_db.table('User')
        self.task_table = baza_db.table('Task')
        self.query = Query()

    def add_user(self, chat_id: str, first_name:str, username=None, last_name=None):
        user = {
            'chat_id': chat_id,
            'first_name': first_name,
            'username': username,
            'last_name': last_name
        }
        if self.user_table.contains(self.query.chat_id == chat_id):
            self.user_table.update(user, self.query.chat_id == chat_id)
            return False
        self.user_table.insert(user)
        return True
    def check_time(self,date):
        all_time = [8,9,10,11,12,1,2,3,4,5,6,7,8]
        x=datetime.now()
        table=self.task_table.all()
        t=int(x.strftime("%I"))
        if t in all_time:
            n=all_time.index(t)
            time_list=all_time[n+1::]
            for i in table:
                k=i['datetime']
                if k in time_list:
                    time_list.remove(k)
            return time_list
        else:
            return all_time
  
    def add_task(self,vaqti,chat_id:str, first_name:str):
        task={
            "chat_id":chat_id,
            "first_name":first_name,
            "datetime":vaqti
        }
        self.task_table.insert(task)
        return True
    def get_task(self, chat_id,):
        tasks=self.task_table.all()
        for i in tasks:
            if i['chat_id']==chat_id:
                return i
        return False