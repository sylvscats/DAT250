import sqlite3

connection = sqlite3.connect('user_database.db')
with open('schema.sql') as f:
    connection.cursor().executescript(f.read())
cur = connection.cursor()

cur.execute("INSERT INTO users (name, personnumber, email, address, password, AvailableBalance) VALUES (?, ?, ?, ?, ?, ?)",
            ('abbas', 11, 'mv@', 'ss', '122', 1000)
            )
print(cur.execute("SELECT * FROM  users;").fetchall())
connection.commit()
connection.close()