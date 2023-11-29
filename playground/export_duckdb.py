import duckdb
db = "duck.db"

query= "COPY (SELECT * FROM messages) TO 'output.csv' (HEADER, DELIMITER ',');"
with duckdb.connect(db, read_only=True) as con:
    con.execute(query).df()   