import json
import os
from datetime import date

class UserNode:
    def __init__(self,username):
        self.username = username
        self.games_played =0
        self.total_wins = 0
        self.cur_streak = 0
        self.best_streak = 0
        self.next = None

class UserManager:
    def __init__(self):
        self.head = None
        self.file_path = "data_users/users.bin"
        self.name_size = 10
        self.int_size = 4
        self.record_size = 26

    def save_data(self):
        if self.is_empty():
            return
            
        with open(self.file_path, "wb") as f:
            current = self.head
            while current:
                buffer = bytearray(self.record_size)

                name_bytes = current.username.encode('utf-8')[:self.name_size]
                buffer[0:len(name_bytes)] = name_bytes 
                
                buffer[10:14] = current.games_played.to_bytes(self.int_size, 'little')
                buffer[14:18] = current.total_wins.to_bytes(self.int_size, 'little')
                buffer[18:22] = current.cur_streak.to_bytes(self.int_size, 'little')
                buffer[22:26] = current.best_streak.to_bytes(self.int_size, 'little')
                
                f.write(buffer)
                current = current.next
        print("Data saved successfully (Manual mode).")

    def load_data(self):
        if not os.path.exists(self.file_path):
            return

        self.head = None
        with open(self.file_path, "rb") as f:
            while True:
                data = f.read(self.record_size)
                if len(data) < self.record_size:
                    break
                
                username = data[0:10].decode('utf-8', errors='ignore').rstrip('\x00')
                
                user_node = self.insert_at_beginning(username)
                
                user_node.games_played = int.from_bytes(data[10:14], 'little')
                user_node.total_wins   = int.from_bytes(data[14:18], 'little')
                user_node.cur_streak   = int.from_bytes(data[18:22], 'little')
                user_node.best_streak  = int.from_bytes(data[22:26], 'little')

    # def load_data(self):
    #     with open(self.file_path, "r") as f:
    #         for i in f.readlines():
    #             user = i.strip().split("|")
    #             user_node = self.insert_at_beginning(user[0])
    #             user_node.games_played = int(user[1])
    #             user_node.total_wins = int(user[2])
    #             user_node.cur_streak = int(user[3])
    #             user_node.best_streak = int(user[4])

    # def save_data (self):
    #     if self.is_empty():
    #         print("Nothing to save")
    #         return
    #     with open(self.file_path, "w") as f:
    #         current = self.head
    #         while current:
    #             line =f"{current.username}|{current.games_played}|{current.total_wins}|{current.cur_streak}|{current.best_streak}\n"
    #             f.write(line)
    #             current = current.next
    
    def insert_at_beginning(self, username):
        new_node = UserNode(username)
        new_node.next = self.head
        self.head = new_node
        return new_node

    def is_empty(self):
        return self.head == None
    
    def update_data(self,username, is_win):
        user = self.get_player(username)
        user.games_played +=1
        if is_win == True:
            user.total_wins +=1
            user.cur_streak +=1
            if user.cur_streak > user.best_streak:
                user.best_streak = user.cur_streak
        else:
            user.cur_streak = 0


    def get_player(self,username):
        if self.is_empty():
            user = self.create_new_player(username)
        elif self.player_is_exist(username) == False:
            user = self.create_new_player(username)
        else:
            user = self.player_is_exist(username)
        return user


    def create_new_player(self,username):
        new_user = self.insert_at_beginning(username)
        return new_user


    def player_is_exist(self,username):
        if self.is_empty():
            print("not exist")
            return
        itr = self.head
        while itr:
            if itr.username == username.strip():
                return itr
            itr = itr.next
        return False

    def player_statistics(self,username):
        user = self.get_player(username)
        print(f"{user.games_played}{user.total_wins}{user.cur_streak}{user.best_streak}")


    def ranking_total_games(self):
            if self.is_empty():
                print("No player")
                return
            
            rank_list = []
            itr = self.head
            while itr:
                rank_list.append(itr) 
                itr = itr.next
            

            rank_list.sort(key=lambda x: x.games_played, reverse=True)
            
            top_5 = rank_list[:5]

            for i in top_5:
                print(f"{i.username} {i.games_played}") 


            

    
        
