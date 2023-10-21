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
