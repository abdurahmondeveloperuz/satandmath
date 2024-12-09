import sqlite3
from datetime import datetime, timedelta
import pytz
import random
import json


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id int NOT NULL,
            fullname varchar(255) NOT NULL,
            username varchar(255),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, fullname: str, username="Lomonosov"):
        sql = """
        INSERT INTO Users(id, fullname, username) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, fullname, username), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


class TestManager:
    def __init__(self, path_to_db="test_manager.db"):
        self.connection = sqlite3.connect(path_to_db)
        self.cursor = self.connection.cursor()
        self._setup_database()

    def _setup_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                id TEXT PRIMARY KEY,
                answers TEXT,
                status TEXT DEFAULT 'online'
            )
        """)
        self.connection.commit()

    # def _generate_unique_id(self):
    #     while True:
    #         test_id = ''.join(random.choices('0123456789', k=6))
    #         self.cursor.execute("SELECT id FROM tests WHERE id = ?", (test_id,))
    #         if not self.cursor.fetchone():
    #             return test_id

    def save_test(self, answers, test_id):
        answers = answers.lower()
        count = len(answers)
        if len(answers) != count:
            raise ValueError("Answers length does not match the count.")

        try:
            self.cursor.execute("INSERT INTO tests (id, answers) VALUES (?, ?)", (test_id, answers))
            self.connection.commit()
            return test_id
        except:
            return "error"

    def check_test(self, test_id, user_answers):
        user_answers = user_answers.lower()
        self.cursor.execute("SELECT answers FROM tests WHERE id = ?", (test_id,))
        row = self.cursor.fetchone()

        if not row:
            raise ValueError("Test ID not found.")

        correct_answers = row[0]
        correct = 0
        wrong = 0
        answers = {}

        for i, (correct_answer, user_answer) in enumerate(zip(correct_answers, user_answers), start=1):
            if user_answer == correct_answer:
                correct += 1
            else:
                wrong += 1
            answers[str(i)] = {"correct": correct_answer, "selected": user_answer}

        return {
            "correct": correct,
            "wrong": wrong,
            "answers": answers
        }

    def end_test(self, test_id):
        self.cursor.execute("UPDATE tests SET status = 'offline' WHERE id = ?", (test_id,))
        self.connection.commit()

    def check_status(self, test_id):
        self.cursor.execute("SELECT status FROM tests WHERE id = ?", (test_id,))
        row = self.cursor.fetchone()
        if not row:
            return "notExist"
        return row[0]
    def get_test_count(self, test_id):
        self.cursor.execute("SELECT answers FROM tests WHERE id = ?", (test_id,))
        row = self.cursor.fetchone()
        if not row:
            return "notExist"
        return len(row[0]) 
    

class UserRankings:
    def __init__(self, path_to_db="rankings.db"):
        self.conn = sqlite3.connect(path_to_db)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            score REAL NOT NULL,
            correct INTEGER NOT NULL,
            wrong INTEGER NOT NULL,
            answers TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def saveRating(self, test_id, user_id, correct, wrong, answers):
        total = correct + wrong
        score = round((100 / total) * correct, 1) if total > 0 else 0  # Foiz hisoblash va 1-lar xonasigacha yaxlitlash
        self.cursor.execute("""
        INSERT INTO rankings (test_id, user_id, score, correct, wrong, answers) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (test_id, user_id, score, correct, wrong, answers))
        self.conn.commit()

    def getAllRatings(self, test_id, limit="infinite"):
        self.cursor.execute("""
        SELECT user_id, score FROM rankings WHERE test_id = ? ORDER BY score DESC
        """, (test_id,))
        results = self.cursor.fetchall()

        if limit != "infinite":
            results = results[:int(limit)]

        rankings = [
            {
                "userId": user_id,
                "rank": idx + 1,
                "score": score
            }
            for idx, (user_id, score) in enumerate(results)
        ]
        return rankings

    def check_userId(self, test_id, user_id):
        self.cursor.execute("""
        SELECT 1 FROM rankings WHERE test_id = ? AND user_id = ?
        """, (test_id, user_id))
        result = self.cursor.fetchone()
        return result is None

    def get_user_tests(self, user_id):
        self.cursor.execute("""
        SELECT test_id FROM rankings WHERE user_id = ? ORDER BY id DESC
        """, (user_id,))
        results = self.cursor.fetchall()

        test_ids = [row[0] for row in results]

        grouped_tests = {}
        for i in range(0, len(test_ids), 5):
            group_key = str(i // 5 + 1)
            grouped_tests[group_key] = test_ids[i:i+5]

        return grouped_tests

    def get_user_test(self, user_id, test_id):
        self.cursor.execute("""
        SELECT user_id, score, correct, wrong, answers FROM rankings WHERE test_id = ? ORDER BY score DESC
        """, (test_id,))
        results = self.cursor.fetchall()
        for user in results:
            if int(user[0]) == user_id:
                return {
                    "userId": user[0],
                    "score": user[1],
                    "correct": user[2],
                    "wrong": user[3],
                    "answers": user[4],
                }

        return None