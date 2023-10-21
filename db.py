import sqlite3
import asyncio

class Database():
    def __init__(self):
        path = 'D:\aiogram-support-bot\database\database.db' 
        self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    def get_users(self):
        response = self.cursor.execute('SELECT user_id FROM users').fetchall()
        return response
    def reg_user(self, user_id):
        self.cursor.execute('INSERT INTO users (user_id) VALUES (?)', [user_id])
        self.conn.commit()
    def user_exist(self, user_id):
        response = self.cursor.execute('SELECT user_id FROM users WHERE user_id = ?', [user_id,]).fetchone()
        return bool(response)
    def count_users(self):
        response = self.cursor.execute('SELECT COUNT (user_id) FROM USERS').fetchall()
        return response[0][0]
    def reg_ticket(self, user_id, text, priority):
        self.cursor.execute('INSERT INTO tickets (user_id, text, priority, state) VALUES (?, ?, ?, 0)', [user_id, text, priority])
        self.conn.commit()
    def get_info(self, user_id):
        response = self.cursor.execute('SELECT id, text, priority, answer FROM tickets WHERE user_id = ? LIMIT 5', [user_id]).fetchall()
        return response
    def get_un_answered_tickets(self):
        response = self.cursor.execute('SELECT id, text, priority FROM tickets WHERE state = 0 LIMIT 10').fetchall()
        return response

