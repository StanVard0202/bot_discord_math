import json
from interactions import *

class EXP():
    def __init__(self):
        pass

    def add_user(self, user:Member | User):
        with open('exp.json','r') as f:
            exp_list:list = json.load(f)
        for users in exp_list:
            if users["id"] == user.id:
                return False
        else:
            structure = {"id":user.id, "exp":0}
            exp_list.append(structure)
            with open('exp.json','w') as f:
                json.dump(exp_list,f)
    
    def add(self, user:Member | User, amount:int):
        with open('exp.json','r') as f:
            exp_list:list = json.load(f)
        for i in range(len(exp_list)):
            if exp_list[i]["id"] == user.id:
                exp_list[i]["exp"] += int(amount)
            with open('exp.json','w') as f:
                json.dump(exp_list,f)
                    
        else:
            self.add_user(user)
    
    def remove(self,user:Member | User, amount:int):
        with open('exp.json','r') as f:
            exp_list:list = json.load(f)
        for i in range(len(exp_list)):
            if exp_list[i]["id"] == user.id:
                exp_list[i]["exp"] -= amount
                with open('exp.json','w') as f:
                    json.dump(exp_list,f)
                break
        else:
            self.add_user(user)

    def check(self, user:Member | User):
        with open('exp.json','r') as f:
            exp_list:list = json.load(f)
        for users in exp_list:
            if users["id"] == user.id:
                return int(users["exp"])
        else:
            return False
