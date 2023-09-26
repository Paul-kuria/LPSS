import sqlite3

conn = sqlite3.connect("license.db")
c = conn.cursor()

# CREATE A TABLE
# c.execute("""CREATE TABLE storeLicense(
#             name DATATYPE,
#             plate DATATYPE,
#             vehicle DATATYPE,
#             registration DATATYPE
#         ) """)


# def show_all():
#     conn = sqlite3.connect('license_db.db')
#     c = conn.cursor()
#
#     #QUERY THE DATABASE
#     c.execute("SELECT rowid, * FROM ")


# ADD NEW RECORD TO THE TABLE
def add_one(name, plate, vehicle, registration):
    conn = sqlite3.connect("license.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO storeLicense VALUES(?,?,?,?)", (name, plate, vehicle, registration)
    )

    conn.commit()
    conn.close()


# DELETE RECORD FROM TABLE
def delete_one(id):
    conn = sqlite3.connect("license.db")
    c = conn.cursor()
    c.execute("DELETE from storeLicense WHERE rowid = (?)", id)

    conn.commit()
    conn.close()


# UPDATE RECORD IN TABLE
def update(name, id):
    conn = sqlite3.connect("license.db")
    c = conn.cursor()
    c.execute("UPDATE storeLicense SET name = (?) " "WHERE rowid = (?)", (name, id))
    conn.commit()
    conn.close()
