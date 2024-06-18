import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

sql = """ select * from table_team_games"""
c.execute(sql)
my_table = c.fetchall()
conn.commit()
conn.close()



def duplicate_or_already_exist_in_sql(my_table):
    i = 0
    temp_table =[]
    while i < len(my_table) - 1:
        j = i + 1
        while j < len(my_table):
            if my_table[i][1] == my_table[j][1]:
                # print(my_table[i][0], "    ", my_table[j][0])
                temp_table.append(my_table[j])
                my_table.remove(my_table[j])
            else:
                j = j + 1
        i = i + 1
    print("remove duplicates")
    print(temp_table)

    return my_table


my_table=duplicate_or_already_exist_in_sql(my_table)
# print(my_table)