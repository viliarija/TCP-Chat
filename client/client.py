import socket
import pickle

class Client:
    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 55555))

    def receive(self):
        try:
            message = self.client.recv(1024).decode('utf-8')
            return message
        except:
            print("An error occured")

    def recieve_object(self):
        length_bytes = self.client.recv(4)
        length = int.from_bytes(length_bytes, byteorder='big')
        received_data = b''
        while len(received_data) < length:
            chunk = self.client.recv(min(length - len(received_data), 4096))
            if not chunk:
                break
            received_data += chunk

        obj = pickle.loads(received_data)
        return obj

    def send(self, message):
        self.client.send(message.encode('utf-8'))

    def request(self, message):
        self.client.send(message.encode('utf-8'))
        response = self.receive()

        if response == "SUCCESS":
            return True
        else:
            return False

    def send_message(self, room_name, message):
        self.send("MESSAGE,{},{}".format(room_name, message))

    def login(self, username, password):
        response = self.request("LOGIN,{},{}".format(username, password))
        return response
    
    def request_code(self, email):
        self.send("REGISTER,SEND,{}".format(email))

    def check_code(self, code):
        self.send("REGISTER,CHECK,{}".format(code))
    


