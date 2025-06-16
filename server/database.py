import sqlite3
import threading

class userDB:
    def __init__(self):
        # Connect to database
        self.conn = None
        self.cur = None
        self.local = threading.local()
        
        conn = sqlite3.connect("user.db")
        cur = conn.cursor()
        # Create tables if missing
        try:
            cur.execute("""CREATE TABLE "user" (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT,
                            username TEXT,
                            password TEXT,
                            pfp TEXT,
                            isAdmin INT
                        )""")
            conn.commit()
            print("Creating 'user' table")
        except sqlite3.OperationalError as e:
            if "table \"user\" already exists" in str(e):
                print("Using existing 'user' table")
            else:
                raise e

        try:
            cur.execute("""CREATE TABLE room (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            description TEXT,
                            code INT
                        )""")
            conn.commit()
            print("Creating 'room' table")
        except sqlite3.OperationalError as e:
            if "table room already exists" in str(e):
                print("Using existing 'room' table")
            else:
                raise e

        try:
            cur.execute("""CREATE TABLE connection (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            banned INT,
                            userID INT,
                            roomID INT,
                            FOREIGN KEY (userID) REFERENCES "user" (id),
                            FOREIGN KEY (roomID) REFERENCES room (id)
                        )""")
            conn.commit()
            print("Creating 'connection' table")
        except sqlite3.OperationalError as e:
            if "table connection already exists" in str(e):
                print("Using existing 'connection' table")
            else:
                raise e
        conn.close()

    def connect(self):
        self.local.conn = sqlite3.connect("user.db")
        self.local.cur = self.local.conn.cursor()

    def close(self):
        if hasattr(self.local, 'conn'):
            self.local.conn.close()

    def add_user(self, email, username, password, pfp, is_admin=False):
        cur = self.local.conn.cursor()
        conn = self.local.conn

        cur.execute("INSERT INTO user (email, username, password, pfp, isAdmin) VALUES (?, ?, ?, ?, ?)",
                    (email, username, password, pfp, is_admin))
        conn.commit()

    def add_connection(self, userID, roomID):
        cur = self.local.cur
        conn = self.local.conn
        cur.execute("INSERT INTO connection (banned, userID, roomID) VALUES (?, ?, ?)",
            (0, userID, roomID))
        conn.commit()

    def check_email(self, email):
        cur = self.local.cur

        cur.execute("SELECT id FROM \"user\" WHERE email = ?", (email,))
        result = cur.fetchone()

        if result:
            return True
        else:
            return False

    def check_username(self, username):
        cur = self.local.cur

        cur.execute("SELECT id FROM \"user\" WHERE username = ?", (username,))
        result = cur.fetchone()

        if result:
            return True
        else:
            return False

    def check_login(self, username, hash1):
        cur = self.local.cur
        # conn = self.local.conn

        cur.execute("SELECT password FROM \"user\" WHERE username = ?", (username,))
        result = cur.fetchone()
        print(result[0], hash1)
        if not result:
            return False
        elif hash1 == result[0]:
            return True
        else:
            return False

    def get_profile(self, uid):
        cur = self.local.cur
        print(uid)
        cur.execute("SELECT * FROM \"user\" WHERE id = ?", (uid,))
        data = cur.fetchone()
        print(data)
        return (data[2], data[4])

    def get_UID(self, username):
        cur = self.local.cur
        cur.execute("SELECT id FROM \"user\" WHERE username = ?", (username,))
        result = cur.fetchone()
        uid = result[0]
        
        return int(uid)
    
    def get_connections(self, uid):
        cur = self.local.cur
        cur.execute("SELECT * FROM \"connection\" WHERE userID = ?", (uid,))
        connections = cur.fetchall()
        
        return connections

    def get_RoomIDs(self):
        cur = self.local.cur
        cur.execute("SELECT id, name FROM \"room\"")
        ids = cur.fetchall()

        return ids

    def get_roomInfo(self, roomID):
        cur = self.local.cur
        cur.execute("SELECT name, description FROM \"room\" WHERE id = ?", (roomID,))
        info = cur.fetchone()

        return info

    def get_room_members(self, roomID):
        cur = self.local.cur
        cur.execute("SELECT userID FROM \"connection\" WHERE roomID = ?", (roomID,))
        result = cur.fetchall()
        members = list()
        for item in result:
            members.append(self.get_profile(item[0]))

        return members

    def join_room(self, uid, code):
        cur = self.local.cur
        cur.execute("SELECT id FROM \"room\" WHERE code = ?", (code,))
        result = cur.fetchone()

        if not result:
            return False

        self.add_connection(uid, result[0])

        return True

class logDB:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.local = threading.local()


    def connect(self):
        self.local.conn = sqlite3.connect("log.db")
        self.local.cur = self.local.conn.cursor()

    def close(self):
        if hasattr(self.local, 'conn'):
            self.local.conn.close()

    def insert_message(self, roomID, message, date, username, userID, pfp):
        cur = self.local.cur
        conn = self.local.conn

        cur.execute("INSERT INTO room_{} (date, username, userID, pfp, message) VALUES (?, ?, ?, ?, ?)".format(roomID),
                    (date, username, userID, pfp, message))
        conn.commit()
    def get_log(self, roomID):
        cur = self.local.cur
        conn = self.local.conn
    # no such table: room_2
        
        # conn.commit()

        try:
            cur.execute("SELECT * FROM room_{}".format(roomID))
            log = cur.fetchall()
        except sqlite3.OperationalError as e:
            if "no such table: room_{}".format(roomID) in str(e):
                print("Creating 'room_{}' table".format(roomID))
                cur.execute("""CREATE TABLE "room_{}" (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT,
                                username TEXT,
                                userID INT,
                                pfp TEXT,
                                message TEXT
                  )""".format(roomID))
                log = [()]            
            else:
                raise e

        return log