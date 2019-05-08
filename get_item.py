import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
cursor = c.execute("DELETE from recommend_myitem")
cursor = c.execute("SELECT * from recommend_myitem")
for row in cursor:
    print(row)

with open('data/item.txt', 'r', encoding='UTF-8') as f:
    all_item = f.readlines()
print(all_item[0])
print(all_item.__len__())

for item in all_item:
    item_info = item.split(';')
    c.execute("INSERT INTO recommend_myitem(item_name, latitude, longitude, item_id)"
              "VALUES (?, ?, ?, ?)", (item_info[1], item_info[2], item_info[3], item_info[0]))

conn.commit()

cursor = c.execute("SELECT * from recommend_myitem")
for row in cursor:
    print(row)

conn.close()
