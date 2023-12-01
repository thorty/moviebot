import duckdb
db = "duck.db"

def creattable():

    #query = "CREATE TABLE IF NOT EXISTS messages (  c1 VARCHAR,  c2 VARCHAR);"
    query = "CREATE TABLE IF NOT EXISTS messages(user VARCHAR, bot VARCHAR);"
    with duckdb.connect(db, read_only=False) as con:
        return con.execute(query).df()


def insert_conversation( usermessage, botmessage):
    try:
        usermessage = usermessage.replace("'","")
        botmessage = botmessage.replace("'","")
        query= "INSERT INTO messages VALUES ('"+usermessage+"','"+botmessage+"');"
        with duckdb.connect(db, read_only=False) as con:    
            return con.execute(query).df()
    except:
        return None


def fetchdata():
    query= "SELECT * FROM messages;"
    with duckdb.connect(db, read_only=True) as con:
        return con.execute(query).df()            
