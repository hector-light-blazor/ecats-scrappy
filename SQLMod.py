import psycopg2

# MOD: establish connection and cursor
def getConAndCursor():
    con = psycopg2.connect("dbname=webapp user=postgres host=spartandb.lrgvdc911.org")
    cursor = con.cursor()
    return con, cursor


def clearTable(cur, phone):
    cur.execute("DELETE FROM ali.spill where transfer_number like %s", ("%" + phone + "%",))


def insertData(data, PHONE):
    con, cur = getConAndCursor()
    clearTable(cur, PHONE)
    con.commit()
    values = b','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tup) for tup in data)
    values = values.decode("utf-8")
    cur.execute("INSERT INTO ali.spill VALUES " + values)
    con.commit()
    cur.close()
    con.close()