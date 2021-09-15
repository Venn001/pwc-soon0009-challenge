#!/usr/bin/python3

#------------------------------------------------------
# CompanyDB.py

# Python class defining access interface to the Restricted companies database.
# The database is held in SQLite.

# Companies database / tables:

# Companies
# ---------
# pkID (Integer Primary Key)
# id (Integer)
# companyName (Text)
# description (TEXT)
# tagline (Text)
# companyEmail (Text)
# businessNumber (Text)
# restricted (Text)
#------------------------------------------------------

import apsw
import string

from builtins import int


class CompanyDB:

    def __init__(self, database = "company.db3", table = "Company"):
        # Initialise the class with the database / table names.
        global connection
        global cursor

        self.database = database
        self.table = table
        self.totalcount = 0
        self.minkey = 0
        self.maxkey = 0

        connection=apsw.Connection(self.database)
        cursor=connection.cursor()


    def AddNewCompany(self, row):
        # Write the company to the database.

        # Row is a dictionary of key / value pairs in any order:
        #     id, companyName, description, tagline, companyEmail, businessNumber, restricted

        sql = "INSERT INTO %s (id, companyName, description, tagline, companyEmail, businessNumber, restricted) " % self.table
        sql += "VALUES (?, ?, ?, ?, ?, ?, ?)"
        # print("Executing SQL statement [%s]" % sql)
        cursor.execute(sql, (row["id"], row["companyName"], row["description"], row["tagline"],
                             row["companyEmail"], row["businessNumber"], row["restricted"]) )


    def Close(self):
        # Close the database cleanly.
        connection.close(True)


    def CountRows(self):
        # Some basic statistics about the companies in the table.
        # Clear in case NULL values result.
        self.totalcount = 0
        self.minkey = 0
        self.maxkey = 0

        sql = 'SELECT count(*), min(id), max(id) FROM %s' % self.table
        # print("Executing SQL statement [%s]" % sql)
        for x in cursor.execute(sql):
            self.totalcount = int(x[0])
            if (self.totalcount):
                self.minkey = int(x[1])
                self.maxkey = int(x[2])

        # print('Rows: total [%d] keys: min [%d] max [%d]' % (self.totalcount, self.minkey, self.maxkey) )


    def GetCompanyById(self, id):
        # Get a specific company by id and return its details.
        # print("CompanyDB.GetCompanyById: id [%s]" % id)

        sql = "SELECT id, companyName, description, tagline, companyEmail, businessNumber, restricted "
        sql += "FROM %s WHERE id = %s" % (self.table, str(id) )
        # print("Executing SQL statement [%s]" % sql)

        row = []

        for x in cursor.execute(sql):
            if x[0] != "":
                row = x

        # Return the result.
        return row


    def GetCompanyList(self, id, count = 100):
        # Get a list of companies after the supplied id, to a maximum of count companies.
        # print("CompanyDB.GetCompanyList: id [%s] count [%s]" % (id, count) )
        pass


    def RecreateTable(self):
        # Drop the table if it already exists.
        sql = 'DROP TABLE IF EXISTS %s' % self.table
        cursor.execute(sql)
    
        # Create the table is not already existing.
        sql = 'CREATE TABLE IF NOT EXISTS %s ' % self.table
        sql += '(pkID INTEGER PRIMARY KEY'
        sql += ', id INTEGER UNIQUE NOT NULL'
        sql += ', companyName TEXT NOT NULL'
        sql += ', description TEXT'
        sql += ', tagline TEXT'
        sql += ', companyEmail TEXT'
        sql += ', businessNumber TEXT'
        sql += ', restricted INTEGER DEFAULT 0'
        sql += ')'
        # print("Executing SQL statement [%s]" % sql)
        cursor.execute(sql)
