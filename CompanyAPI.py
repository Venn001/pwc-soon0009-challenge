#!/usr/bin/python3

#------------------------------------------------------
# CompanyAPI.py

# Python class defining API access to the Companies database.

# The class provides the functions for the Web API to access the database and
# build the HTML (including CSS) representation of the data, which is returned
# back to the caller.
#------------------------------------------------------

import os

from CompanyDB import CompanyDB

from bs4 import BeautifulSoup


class CompanyAPI:

    def __init__(self, companyDB, cssFile = "company.css"):
        # Initialise the class with an instance of the CompanyDB class.

        self.companyDB = companyDB
        self.cssFile = cssFile
        self.cssText = ""
        self.LoadCSSFile() 


    def AddNewCompany(self, row):
        # Write the company to the database.

        # Row is a dictionary of key / value pairs in any order:
        #     id, companyName, description, tagline, companyEmail, businessNumber, restricted

        # Convert string for 'restricted' back to an integer boolean.
        row["restricted"] = "0" if row["restricted"].lower() == "no" else "1"

        self.companyDB.AddNewCompany(row)


    def GetCompanyById(self, id):
        # Get a specific company by id and return its details.
        # print("CompanyAPI.GetCompanyById: id [%s]" % id)

        companyHTML = self.PresetHTML()
        companyHTML += "<body><H1>Company Database Search</h1>\n"

        row = self.companyDB.GetCompanyById(id)

        # Check for no result.
        if len(row) == 0:
            companyHTML += "<p><strong>No company with ID [%s]</strong></p>" % id

        else:
            # Must have a result.
            restricted = "No" if row[6] == "0" else "Yes"

            companyHTML += "<div style=\"overflow-x:auto;\">\n"
            companyHTML += "<table id=\"company\">\n"
            companyHTML += "<tr><th>Company</th><th>%s</th></tr>\n" % row[1]
            companyHTML += "<tr><td>ID</td><td>%s</td></tr>\n" % row[0]
            companyHTML += "<tr><td>Description</td><td>%s</td></tr>\n" % row[2]
            companyHTML += "<tr><td>Tagline</td><td>%s</td></tr>\n" % row[3]
            companyHTML += "<tr><td>Email</td><td>%s</td></tr>\n" % row[4]
            companyHTML += "<tr><td>Business number</td><td>%s</td></tr>\n" % row[5]
            companyHTML += "<tr><td>Restricted</td><td>%s</td></tr>\n" % restricted

            companyHTML += "</table></div>\n"

        companyHTML += "</body></html>\n"

        # Format the HTML aspect - easier to read and debug.
        return BeautifulSoup(companyHTML, 'html.parser').prettify()
        # return companyHTML


    def GetCompanyList(self, id, count = 100):
        # Get a list of companies after the supplied id, to a maximum of count companies.
        # print("CompanyAPI.GetCompanyList: id [%s] count [%d]" % (id, count) )
        pass


    def LoadCSSFile(self):
        # Preload the CSS file contentss to a string for easier usage.

        if os.path.isfile(self.cssFile):
            # Read whole file to a string.
            text_file = open(self.cssFile, "r")
            self.cssText = text_file.read()
            text_file.close()


    def PresetHTML(self):
        # Preset the HTML to be returned.
        companyHTML = "<!DOCTYPE html><html><head><title>Company DB search</title>\n"
        if self.cssText:
            companyHTML += "<style>\n" + self.cssText + "</style>\n"
        companyHTML += "</head>\n"

        return companyHTML
