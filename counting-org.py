import sqlite3

# create a connection object that represents the database, the data will be stored in the emaildb.sqlite file.
conn = sqlite3.connect('emaildb.sqlite')

# create a cursor object and call execute() method to perform SQL commands
cur = conn.cursor()

# every time run this program, drop the table and then create it again
cur.execute('''
DROP TABLE IF EXISTS Counts''')
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

# prompt for file name
fname = raw_input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.split()
    email = pieces[1]
    parts = email.split('@')
    org = parts[1]
    print org
    # question maker is a place holder to be filled in
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, )) 
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) 
                VALUES ( ?, 1 )''', ( org, ) )
    else : 
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', 
            (org, ))
    # This statement commits outstanding changes to disk each 
    # time through the loop - the program can be made faster 
    # by moving the commit so it runs only after the loop completes
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

print
print "Counts:"
for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]

cur.close()


# https://docs.python.org/2/library/sqlite3.html
