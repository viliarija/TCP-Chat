from functools import partial
import threading

from room import *
from login import *
from client import Client

import os
import customtkinter
from PIL import Image
from time import sleep
from datetime import datetime

path = None
icons = {}


class RoomFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.buttons = []
        self.update_rooms()

    def update_rooms(self):
        for button in self.buttons:
            button.destroy()

        self.buttons = []

        if self.values:
            for i, value in enumerate(self.values):
                print(i)
                button = customtkinter.CTkButton(self, 
                                                command=partial(self.master.change_room_callback, i),
                                                text=value)
                
                button.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="we")
                self.buttons.append(button)

        add_button = customtkinter.CTkButton(self, 
                                             command=self.master.add_room,
                                             text="Add")
        
        add_button.grid(row=len(self.buttons), column=0, padx=10, pady=(10, 0), sticky="we")
        self.buttons.append(add_button)

class ProfileFrame(customtkinter.CTkFrame):
    def __init__(self, master, username, pfp):
        super().__init__(master)
        image_label = customtkinter.CTkLabel(self, image=icons[pfp], text=username, compound="left", padx=10)
        image_label.grid(row=0, column=0, padx=5, pady=5, sticky="we")


class MessageFrameTop(customtkinter.CTkFrame):
    def __init__(self, master, date, username, pfp, message):
        super().__init__(master)
        image_label = customtkinter.CTkLabel(self, image=icons[pfp], text=username, compound="left", padx=10)
        image_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        message_label = customtkinter.CTkLabel(self, text=message, padx=30)
        message_label.grid(row=1, column=0, padx=5, sticky="w")

        self.grid_columnconfigure(1, weight=1)
        date_label = customtkinter.CTkLabel(self, text=date, text_color="gray")
        date_label.grid(row=0, column=1, padx=5, sticky="e")


class MessageLogFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, label_text="Chat")
        self. master = master

        self.profile = master.profile
        self.log = master.log
        self.rooms = master.rooms
        self.cur_row = 0
        self.messages = []

        self.grid_columnconfigure(0, weight=1)

        if self.log:
            self.update_messages()

    def update_messages(self):
        cur_room = self.master.cur_room
        log = self.log[cur_room]

        self.configure(label_text=self.master.rooms[cur_room])

        for message_widget in self.messages:
            message_widget.destroy()

        self.messages = []

        last_user = None

        if log == None:
            return

        for i, (mid, date, username, uid, pfp, message) in enumerate(log):
            if i != 0 and username == last_user:
                message_label = customtkinter.CTkLabel(self, text=message, padx=30)
                message_label.grid(row=i, column=0, padx=15, sticky="w")
                self.messages.append(message_label)
            else:
                message_frame = MessageFrameTop(self, date, username, pfp, message)
                message_frame.grid(row=i, column=0, padx=10, sticky="we")
                self.messages.append(message_frame)
            last_user = username
            self.cur_row = i

    def insert_local_message(self, message):
        cur_room = self.master.cur_room
        username = self.profile[0]

        if self.log[cur_room]:
            print(self.log[cur_room])
            last_user = self.log[cur_room][-1][2]
        else:
            last_user = None

        self.cur_row += 1
        if last_user != username:
            now = datetime.now()
            date = now.strftime("%d/%m/%Y %H:%M:%S")

            pfp = self.profile[1]
            message_frame = MessageFrameTop(self, date, username, pfp, message)
            message_frame.grid(row=self.cur_row, column=0, padx=10, sticky="we")
            self.messages.append(message_frame)

            self.log[cur_room].append((None, date, username, None, pfp, message))
        else:
            message_label = customtkinter.CTkLabel(self, text=message, padx=30)
            message_label.grid(row=self.cur_row, column=0, padx=15, sticky="w")
            self.messages.append(message_label)
            self.log[cur_room].append((None, None, username, None, None, message))

    def insert_external_message(self, room, username, pfp, message):
        cur_room = self.master.cur_room
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")

        if room != self.rooms[cur_room]:
            self.log[self.rooms.index(room)].append((None, date, username, None, pfp, message))
            return

        if self.log[0]:
            last_user = self.log[cur_room][-1][2]
        else:
            last_user = None

        self.cur_row += 1
        if last_user != username:
            now = datetime.now()
            date = now.strftime("%d/%m/%Y %H:%M:%S")

            message_frame = MessageFrameTop(self, date, username, pfp, message)
            message_frame.grid(row=self.cur_row, column=0, padx=10, sticky="we")
            self.messages.append(message_frame)
            self.log[cur_room].append((True, date, username, None, pfp, message))
        else:
            message_label = customtkinter.CTkLabel(self, text=message, padx=30)
            message_label.grid(row=self.cur_row, column=0, padx=15, sticky="w")
            self.messages.append(message_label)
            self.log[cur_room].append((False, None, username, None, None, message))


class MessageEntryFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.master = master

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.message_entry = customtkinter.CTkEntry(self, placeholder_text="Message")
        self.message_entry.grid(row=0, column=0, padx=(0, 10), sticky="nswe")

        self.send_button = customtkinter.CTkButton(self, command=self.send, text="Send", width=100)
        self.send_button.grid(row=0, column=1, sticky="ns")

    def send(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, "end")
        self.master.send_message_callback(message)


class MembersFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, members):
        super().__init__(master, label_text="Members")
        self.master = master
        self.members = members
        self.user_labels = []

        if self.members:
            self.update_members()

    def update_members(self):
        cur_room = self.master.cur_room
        for user_label in self.user_labels:
            user_label.destroy()

        self.user_labels = []

        for i, (username, pfp) in enumerate(self.members[cur_room]):
            user_label = customtkinter.CTkLabel(self, image=icons[pfp], text=username, compound="left", padx=10)
            user_label.grid(row=i, column=0, padx=10, sticky="we")
            self.user_labels.append(user_label)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.client = Client()

        self.profile = None
        self.rooms = ["Chat"]
        self.log = None
        self.members = None

        login = Login(self.client)
        login.mainloop()

        if login.result == True:
            print("Logged in")
            self.retrieve_data()
        elif login.result == False:
            self.client.send("REGISTER")
            register = Register(self.client)
            register.mainloop()
            self.retrieve_data()

        global path
        path = os.path.dirname(os.path.realpath(__file__))

        self.update = False

        self.cur_room = 0

        self.room_frame = None
        self.profile_frame = None
        self.log_frame = None
        self.message_entry_frame = None
        self.members_frame = None

        self.load_icons()
        self.init_window()

        self.run_threads()

    def run_threads(self):
        self.handle_thread = threading.Thread(target=self.handle)
        self.handle_thread.start()

        self.gui_thread = threading.Thread(target=self.gui)
        self.gui_thread.start()

    def gui(self):
        self.init_1st()
        self.init_2nd()
        self.init_3rd()

    def retrieve_data(self):
        self.profile = self.client.recieve_object()
        self.rooms = self.client.recieve_object()
        self.log = self.client.recieve_object()
        self.members = self.client.recieve_object()
        print(self.members)

        print("retrieved data")

    def load_icons(self):
        icon_path = "{}/icon/".format(path)
        icon_files = os.listdir(icon_path)
        for icon in icon_files:
            image = Image.open("{}/{}".format(icon_path, icon))
            image_object = customtkinter.CTkImage(light_image=image, size=(30, 30))

            icons[icon.split('.')[0]] = image_object

    def init_window(self):
        # Create window
        self.geometry("1000x600")
        self.title("Discuss thing - Client")
        self.minsize(300, 200)

        # Configure columns and rows
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=2)

    def init_1st(self):
        self.room_frame = RoomFrame(self, "Rooms", self.rooms)
        self.room_frame.grid(row=0, column=0, padx=15, pady=(20, 0), rowspan=2, sticky="ns")

        self.profile_frame = ProfileFrame(self, self.profile[0], self.profile[1])
        self.profile_frame.grid(row=3, column=0, padx=15, pady=10, sticky="we")

    def init_2nd(self):
        self.log_frame = MessageLogFrame(self)
        self.log_frame.grid(row=0, column=1, rowspan=2, pady=(20, 0), sticky="nsew")

        self.message_entry_frame = MessageEntryFrame(self)
        self.message_entry_frame.grid(row=3, column=1, pady=10, sticky="nswe")

    def init_3rd(self):
        self.members_frame = MembersFrame(self, self.members)
        self.members_frame.grid(row=0, column=2, rowspan=3, sticky="nswe", pady=(20, 0), padx=10)

    def handle(self):
        while True:
            try:
                if not self.update:
                    text = self.client.receive()
                    query = text.split(',')
                    if query[0] == "MESSAGE":
                        content = text[len(f"MESSAGE,{query[1]},{query[2]},{query[3]},"):]
                        self.log_frame.insert_external_message(query[1], query[2], query[3], content)
                else:
                    sleep(4)
            
            except Exception as e:
                print(e)

    # def handle_update(self):
    #     while True:
    #         if self.update == True:
    #             self.retrieve_data()
    #             self.room_frame.update_rooms()

    #         sleep(1)


    def add_room(self):
        add = Add(self, self.client)
        add.mainloop()
        
    def send_message_callback(self, message):
        room_name = self.rooms[self.cur_room]
        self.client.send_message(room_name, message)
        self.log_frame.insert_local_message(message)
    
    def change_room_callback(self, index):
        self.cur_room = index

        self.log_frame.update_messages()
        self.members_frame.update_members()


if __name__ == "__main__":
    app = App()
    app.mainloop()
