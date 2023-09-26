import sqlite3

conn = sqlite3.connect("LOGG.db")
c = conn.cursor()


# CREATE PRIMARY TABLE
def create_table():
    c.execute(
        """CREATE TABLE mainTable(
             name DATATYPE,
             vehicle DATATYPE,
             plate DATATYPE
    )
    """
    )


# CREATE LOGIN TABLE
def create_table2():
    c.execute(
        """CREATE TABLE logTable(
                     regno DATATYPE,
                     vehicle DATATYPE,
                     timestamp DATATYPIncorrect number of bindings supplied. The current statement uses 1, and there are 10 supplied.E
            )
            """
    )


def create_table3():
    c.execute(
        """CREATE TABLE temporary(
                     nplate DATATYPE
            )
            """
    )


def delete_one(id):
    conn = sqlite3.connect("LOGG.db")
    c = conn.cursor()
    c.execute("DELETE from mainTable WHERE rowid = (?)", id)

    conn.commit()
    conn.close()


# ADD NEW RECORD TO THE TABLE
def add_one(name, vehicle, reg):
    conn = sqlite3.connect("LOGG.db")
    c = conn.cursor()
    c.execute("INSERT INTO mainTable VALUES(?,?,?)", (name, vehicle, reg))

    conn.commit()
    conn.close()


# APPEND NEW LOGIN TABLE
def add_two(regno):
    conn = sqlite3.connect("LOGG.db")
    c = conn.cursor()
    c.execute("INSERT INTO logTable VALUES(?,?,?)", (regno))


# QUERY THE DATABASE FOR INFORMATION
def query_reg(reg):
    conn = sqlite3.connect("LOGG.db")
    c = conn.cursor()
    one = tuple(c.execute("SELECT * FROM mainTable WHERE plate = (?)", reg))
    print(one)
    print((one[0][2]))
    print(f"{one} You are free to enter. ")
    conn.commit()
    conn.close()


# delete_one('1')


def show_all():
    conn = sqlite3.connect("LOGG.db")
    c = conn.cursor()

    # QUERY THE DATABASE
    print(c.execute("SELECT rowid, * FROM mainTable"))
