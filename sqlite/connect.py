from sqlite3 import connect

con = connect('sqlite/chart_db.db')
cur = con.cursor()
