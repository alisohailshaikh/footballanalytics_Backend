import pyodbc
import pandas as pd


class Database:

    def __init__(self):
        cxnstring = ("Driver={ODBC Driver 17 for SQL Server};"
             "Server=DESKTOP-PSGPR9D\SQLEXPRESS;"
             "Database=FootballAnalytics;"
             "Trusted_Connection=yes;")

        cxn = pyodbc.connect(cxnstring)
        self.cursor = cxn.cursor()
        




