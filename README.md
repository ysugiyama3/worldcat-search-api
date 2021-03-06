# worldcat-search-api
Python scripts that access WorldCat and get holdings data using the WorldCat Search API. https://www.oclc.org/developer/develop/web-services/worldcat-search-api/library-locations.en.html

# What you need
1. Python 2.7
2. SQLite browser
3. Your own WSKey https://www.oclc.org/developer/develop/authentication/how-to-request-a-wskey.en.html

# Steps
1. Create a list of OCLC numbers and save it as OCLC.txt. (sample list in the examples folder contains 890 OCLC numbers for Japanese LGBTQ materials)
2. Run worldcat1.py. It will count how many OCLC records each library holds and determine top 5 libraries that hold the most OCLC records. top5libraries.txt will be generated (sample in the examples folder). It will create a table called Library in a sqlite database called worldcat.
3. Run worldcat2.py. It will check the holdings status of those 5 libraries. It will create a table called OCLC in the sqlite database.

# For more info about my project
Data-Driven Collection Analysis Using the WorldCat Search API: Japanese LGBTQ Collections https://drive.google.com/file/d/0B9mw-tbO3jRdRkozNGdpbXg0N1E/view?usp=sharing
