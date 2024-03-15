from DBConfig import conn


def build():
    sqlFile = open("./databaseDDL.sql", 'r', encoding='utf8')
    sql = sqlFile.read()
    cursor = conn.cursor()
    cursor.executescript(sql)
    cursor.close()
    conn.commit()
    print("Done. Go running DBBuild.py to import more data.")


if __name__ == "__main__":
    build()
