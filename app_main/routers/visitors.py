# def add_one(name, plate, vehicle, registration):
#     conn = sqlite3.connect('license.db')
#     c = conn.cursor()
#     c.execute("INSERT INTO storeLicense VALUES(?,?,?,?)", (name,plate,vehicle,registration))

#     conn.commit()
#     conn.close()


# #DELETE RECORD FROM TABLE
# def delete_one(id):
#     conn = sqlite3.connect('license.db')
#     c = conn.cursor()
#     c.execute("DELETE from storeLicense WHERE rowid = (?)",id)

#     conn.commit()
#     conn.close()

# #UPDATE RECORD IN TABLE
# def update(name,id):
#     conn = sqlite3.connect('license.db')
#     c = conn.cursor()
#     c.execute("UPDATE storeLicense SET name = (?) "
#               "WHERE rowid = (?)", (name,id))
#     conn.commit()
#     conn.close()
