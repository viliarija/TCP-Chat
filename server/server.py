import socket
import pickle
import threading
import hashlib as hash
from datetime import datetime
from random import choice

from database import *
from mail import send_code

userData = userDB()
logData = logDB()

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

roomIDs = dict()

rooms = dict()
connections = dict()
members = dict()

pfps = ['bee', 'bullfinch', 'camel', 'cat', 'chicken', 'clown-fish', 'crab', 'deer', 'dog',
        'elephant', 'fox', 'frog', 'hippo', 'lion', 'mouse', 'crab', 'panda', 'parrot', 'pig', 'rhino', 'sheep']

def broadcast(room, message, username, userID, pfp, origin):
    for client in rooms[room]:
        if client == origin:
            continue
        client.send(f"MESSAGE,{room},{username},{pfp},{message}".encode("utf-8"))

    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    logData.insert_message(roomIDs[room], message, date, username, userID, pfp)

def handle(client, username, pfp, uid):
    while True:
        try:
            text = client.recv(1024).decode('utf-8')
            query = text.split(',')
            if query[0] == "MESSAGE":
                room = query[1]
                content = text[len(f"MESSAGE {room} "):]
                broadcast(room, content, username, uid, pfp, client)

            elif query[0] == "ADD":
                userData.join_room(uid, int(query[1]))
                client.send("SUCCESS".encode("utf-8"))
                set_up(client, uid)
                
        except Exception as e:
            print(e)
            for connection in connections[uid]:
                rooms[connection].remove(client)
            connections.pop(uid)
            client.close()
            break


def send_object(client, obj):
    obj_raw = pickle.dumps(obj)
    length = len(obj_raw)
    client.sendall(length.to_bytes(4, byteorder='big'))
    client.sendall(obj_raw)

def set_up(client, uid):
    user_connections = userData.get_connections(uid)
    user_rooms = list()
    log = list()
    connections[uid] = list()
    members = list()

    for id, banned, userID, roomID in user_connections:
        if banned:
            continue
        name = userData.get_roomInfo(roomID)[0]
        user_rooms.append(name)

        log.append(logData.get_log(roomID))

        if name in rooms:
            rooms[name].append(client)
        else:
            rooms[name] = [client, ]

        connections[uid].append(name)
        members.append(userData.get_room_members(roomID))

    profile = userData.get_profile(uid)
    send_object(client, profile)
    send_object(client, user_rooms)
    send_object(client, log)
    send_object(client, members)

    return profile[1]


def auth(client):
    userData.connect()
    logData.connect()
    message = client.recv(1024).decode('utf-8').split(',')
    if message[0] == "LOGIN":
        username = message[1]
        password = hash.sha256("{}{}{}".format(message[1][:2], message[2], message[1][-2:]).encode("utf-8")).hexdigest()

        if userData.check_login(username, password):
            client.send("SUCCESS".encode("utf-8"))
            uid = userData.get_UID(username)
            pfp = set_up(client, uid)
            handle(client, username, pfp, uid)

        else:
            client.send("FAIL".encode("utf-8"))

    if message[0] == "REGISTER":
        email = client.recv(1024).decode('utf-8')
        if not userData.check_email(email):
            sent_code = send_code(email)
            client.send("SUCCESS".encode("utf-8"))
        else:
            client.send("FAIL".encode("utf-8"))
            return

        received_code = client.recv(1024).decode('utf-8')
        if received_code == sent_code:
            client.send("SUCCESS".encode("utf-8"))
        else:
            client.send("FAIL".encode("utf-8"))
            return

        username, password = client.recv(1024).decode('utf-8').split(' ')
        if not userData.check_username(username):
            password_hash = hash.sha256("{}{}{}".format(username[:2], password, username[-2:]).encode("utf-8")).hexdigest()
            userData.add_user(email, username, password_hash, choice(pfps))
            client.send("SUCCESS".encode("utf-8"))
        else:
            client.send("FAIL".encode("utf-8"))
            return

        uid = userData.get_UID(username)
        pfp = set_up(client, uid)
        handle(client, username, pfp, uid)

    userData.close()
    logData.close()


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        thread = threading.Thread(target=auth, args=(client,))
        thread.start()


def init():
    userData.connect()
    unorganized_roomIDs = userData.get_RoomIDs()
    for (roomID, room_name) in unorganized_roomIDs:
        roomIDs[room_name] = roomID

    userData.close()

    receive()


init()
