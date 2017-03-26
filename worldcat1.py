import urllib
import json
import sqlite3

# Create a database
conn = sqlite3.connect('worldcat.sqlite')
cur = conn.cursor()

# Make some fresh tables in the database using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Library;

CREATE TABLE Library (   
    library    TEXT UNIQUE,
    fullname   TEXT,
    count   INTEGER
);
''')

link1 = "http://www.worldcat.org/webservices/catalog/content/libraries/"
wskey = "" # Enter your WSKey: https://www.oclc.org/developer/develop/authentication/how-to-request-a-wskey.en.html"
link2 = "?maximumLibraries=100&wskey=" + wskey + "&format=json&frbrGrouping=off"

fhand = open('OCLC.txt')
for oclc in fhand:
    oclc = oclc.rstrip() 
    url = link1 + oclc + link2
    input = urllib.urlopen(url)

    for line in input:
        root = line.strip()
        info = json.loads(root)
        print '\n' 'OCLC#: ',oclc
        libcount = 0
               
        try:                                        
            lib = info["library"]
            for item in lib:
                libcode = item["oclcSymbol"]
                print libcode
                libfullname = item["institutionName"]
                libcount = libcount + 1

                cur.execute('SELECT count FROM Library WHERE library = ? ', (libcode, )) 
                row = cur.fetchone()
                if row is None:
                    cur.execute('''INSERT INTO Library (library, fullname, count) VALUES ( ?, ?, 1 )''', (libcode, libfullname,) )
                else: 
                    cur.execute('UPDATE Library SET count=count+1 WHERE library = ?', (libcode, ))
 
            print 'Total Lib Count: ', libcount	
        except:
		    print 'Total Lib Count: ', libcount


    conn.commit()

sqlstr = 'SELECT library, fullname, count FROM Library ORDER BY count DESC LIMIT 5'

toplibraries = open('top5libraries.txt','w')
print
print "Top 5 Libraries:"
for row in cur.execute(sqlstr):
	toplibraries.write(str(row[0]))
	toplibraries.write("\n")
	print (row[0]), row[1], row[2]

toplibraries.close()
cur.close()            