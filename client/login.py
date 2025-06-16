import os
import customtkinter

class Login(customtkinter.CTk):
    def __init__(self, client):
        super().__init__()
        global path
        path = os.path.dirname(os.path.realpath(__file__))

        self.client = client
        self.result = None

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

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(column=0, row=0, columnspan=2, pady=(50,5))

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Password", show='*')
        self.password_entry.grid(column=0, row=1, columnspan=2)

        login_button = customtkinter.CTkButton(self, text="Login", command=self.login_callback)
        login_button.grid(column=0, row=2, columnspan=2, pady=10)

        register_button = customtkinter.CTkButton(self, text="Register", fg_color="transparent", hover=False, text_color="black", command=self.register_callback)
        register_button.grid(column=0, row=3, pady=10, sticky="s")
        
        resset_button = customtkinter.CTkButton(self, text="Resset",fg_color="transparent", hover=False, text_color="black", command=self.resset_callback)
        resset_button.grid(column=1, row=3, pady=10, sticky="s")

    def login_callback(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.client.login(username, password):
            self.result = True
            self.close()

    def register_callback(self):
        self.result = False
        self.close()

    def close(self):
        super().destroy()
        super().quit()

    def resset_callback(self):
        pass
    


class Register(customtkinter.CTk):
    def __init__(self, client):
        super().__init__()

        self.client = client
        self.result = None

        self.init_window()
        self.init_widgets()
    
    def init_window(self):
        # Create window
        self.geometry("300x300")
        self.title("Discuss thing - Register")
        self.minsize(300, 200)

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(3, weight=1)

    def init_widgets(self):
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Email address")
        self.entry.grid(column=0, row=2, columnspan=2, pady=5)

        self.button = customtkinter.CTkButton(self, text="Send code", command=self.send_code_callback)
        self.button.grid(column=0, row=3, columnspan=2, pady=10)

    def send_code_callback(self):
        email = self.entry.get()
        response = self.client.request(email)

        if not response:
            return

        self.entry.delete(0, "end")
        self.entry.configure(placeholder_text="Code")
        self.button.configure(command=self.check_code_callback, text="Check code")

    def check_code_callback(self):
        code = self.entry.get()
        response = self.client.request(code)

        if not response:
            return

        self.entry.delete(0, "end")
        self.entry.configure(placeholder_text="Confirm password")

        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.entry2.grid(column=0, row=0, columnspan=2, pady=5)

        self.entry3 = customtkinter.CTkEntry(self, placeholder_text="Enter password")
        self.entry3.grid(column=0, row=1, columnspan=2, pady=5)

        self.button.configure(command=self.register_callback, text="Log in")

    def register_callback(self):
        username = self.entry2.get()
        password = self.entry3.get()
        password2 = self.entry.get()

        if password != password2:
            return

        response = self.client.request(username + ' ' + password)

        if not response:
            return

        self.close()

    def close(self):
        super().destroy()
        super().quit()


if __name__ == "__main__":
    login = Login()
    login.mainloop()
