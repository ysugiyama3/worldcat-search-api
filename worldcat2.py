import urllib
import json
import sqlite3

conn = sqlite3.connect('worldcat.sqlite')
cur = conn.cursor()

liblist = list()
libraries = open('top5libraries.txt')
for library in libraries:
    liblist.append(library)

lib1 = liblist[0].strip()
lib2 = liblist[1].strip()
lib3 = liblist[2].strip()
lib4 = liblist[3].strip()
lib5 = liblist[4].strip()		
						
# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS OCLC;

CREATE TABLE OCLC (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    oclcid  INTEGER,
    libcount   INTEGER,
    library1     TEXT,
    library2     TEXT,
    library3     TEXT,
    library4     TEXT,
    library5     TEXT
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
        lib1count = "N"
        lib2count = "N"
        lib3count = "N"
        lib4count = "N"
        lib5count = "N"
               
        try:                                        
            lib = info["library"]
            for item in lib:
                libcode = item["oclcSymbol"]
                libcode = str(libcode)
                libfullname = item["institutionName"]
                libcount = libcount + 1
                if libcode == str(lib1):
                    lib1count = "Y"
                if libcode == str(lib2):
                    lib2count = "Y"					
                if libcode == str(lib3):
                    lib3count = "Y"					
                if libcode == str(lib4):
                    lib4count = "Y"					
                if libcode == str(lib5):
                    lib5count = "Y"					
            print 'Total Lib Count: ', libcount	
        except:
            print 'Total Lib Count: ', libcount
                   
        print lib1, lib1count
        print lib2, lib2count
        print lib3, lib3count
        print lib4, lib4count
        print lib5, lib5count
               
        cur.execute('''INSERT OR IGNORE INTO OCLC (oclcid, libcount, library1, library2, library3, library4, library5 ) VALUES ( ?, ?, ?, ?, ?, ?, ? )''', ( oclc, libcount, lib1count, lib2count, lib3count, lib4count, lib5count) )
        cur.execute('SELECT id FROM OCLC WHERE oclcid = ? ', (oclc, ))
        petnameid = cur.fetchone()[0]
        conn.commit()
cur.close()         
