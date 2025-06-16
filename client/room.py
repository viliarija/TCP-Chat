import customtkinter
from time import sleep

class Add(customtkinter.CTk):
    def __init__(self, master, client):
        super().__init__()

        self.master = master
        self.client = client
        self.result = False

        self.init_window()
        self.init_widgets()

    def init_window(self):
        # Create window
        self.geometry("300x300")
        self.title("Discuss thing - Login")
        self.minsize(300, 200)

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(3, weight=1)

    def init_widgets(self):

        self.code_entry = customtkinter.CTkEntry(self, placeholder_text="Code")
        self.code_entry.grid(column=0, row=0, columnspan=2, pady=(50,5))
        
        create_button = customtkinter.CTkButton(self, text="Create", command=self.create_callback)
        create_button.grid(column=0, row=3, pady=10, sticky="s")
        
        add_button = customtkinter.CTkButton(self, text="Add", command=self.add_callback)
        add_button.grid(column=1, row=3, pady=10, sticky="s")

    def create_callback(self):
        pass

    def add_callback(self):
        self.master.update = True
        code = self.code_entry.get()
        self.client.send("ADD,{}".format(code))
        self.master.retrieve_data()
        self.master.room_frame.update_rooms()
        self.master.update = False

        self.close()


    def close(self):
        print("close called")
        super().destroy()
        super().quit()