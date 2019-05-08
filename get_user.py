import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

cursor = c.execute("SELECT * from recommend_myuser")
for row in cursor:
    print(row)

with open('data/user.txt', 'r', encoding='UTF-8') as f:
    all_user = f.readlines()
print(all_user[0])
print(all_user.__len__())

for user in all_user:
    user_info = user.split(';')
    c.execute("INSERT INTO recommend_myuser (user_name, L, S, password)"
              "VALUES (?, ?, ?, ?)", (user_info[0], user_info[2], user_info[3], user_info[1]))

conn.commit()

cursor = c.execute("SELECT * from recommend_myuser")
for row in cursor:
    print(row)

conn.close()
