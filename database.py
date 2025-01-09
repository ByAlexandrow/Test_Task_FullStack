import sqlite3


DB_NAME = 'monitoring.db'


class Database:
    def __init__(self, db_name = DB_NAME):
        self.connection = sqlite3.connect(db_name)
        self.create_table()
    

    def create_table(self):
        """Функия создания базы данных."""
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sys_monitoring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL
            )
        """)
        self.connection.commit()
    

    def insert_data(self, cpu_usage, memory_usage, disk_usage):
        """Функция внедряет полученные значения в базу данных."""
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO sys_monitoring (cpu_usage, memory_usage, disk_usage) VALUES (?, ?, ?)",
            (cpu_usage, memory_usage, disk_usage)
        )
        self.connection.commit()
    

    def close_db(self):
        """Функция закрывает соединение с базой данных."""
        self.connection.close()
