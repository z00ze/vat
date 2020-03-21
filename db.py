# -*- coding: utf-8 -*-
""" VAT validator 9000

DB

Retrieves and saves company information in to MySQL database.

Marko Loponen
marko.juhani.loponen@gmail.com
"""
from datetime import datetime
import mysql.connector
import external as EX
import json

def init_db():
    """ Initialize database connection
    """
    return mysql.connector.connect(user=credentials['cres'][0], database="vat_list", password=credentials['cres'][1])

def get_cursor():
    """ Get cursor
    In case of timeout, initialize.
    """
    
    global connection
    try:
        connection.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:  
        connection = init_db()
    return connection.cursor(buffered=True)

def setCredentials():
    """ Retrieve the credentials from random.random file.
    
    Return:
        (dict) : Credentials data in format:
                "cres": list (in index 0: username, 1:password),
                "error": Boolean,
                "reason": str,
                "info": str
    """
    try:
        f = open("random.random", "r")
        return {"cres":f.readlines()[0].split(","), "error": {"is_error": False, "reason": "", "info": ""}}
    
    except IOError:
        return {"cres":[],"error": {"is_error": True, "reason": "File problem.", "info": "Ask admin for more."}}
    
    finally:
        f.close()

connection = None
""" MySQL connection object
"""

credentials = setCredentials()
""" Set credentials for database connection
"""

if credentials['error']['is_error']:
    """ In case of file read error or something, abort.
    """
    print("ERROR! " + credentials['error']['reason'] + " | " + credentials['error']['info'])
    exit()
    

connection = init_db()
cursor = get_cursor()
""" MySQL connection and cursor
"""

query_ListAll = ("SELECT id, data, date FROM companies")
query_getByVAT = ("SELECT * FROM companies WHERE id = %s")
query_insertCompany = ("INSERT IGNORE INTO companies (id, data, date) VALUES (%s, %s, %s)")
""" Queries we are using in this application.
"""

def listAll():
    """ Get all information.
    Return:
        list of (dict)s : Company data in list format:
                        "city": str,
                        "name": str,
                        "address": str,
                        "postcode": str,
                        "updatedOn": datetime in str when added to DB,
                        "vatNumber": str,
                        "countryCode": str,
                        "requestDate": date in str when requested from external service
    """
    cursor = get_cursor()
    cursor.execute(query_ListAll)
    connection.commit()
    
    companies = []
    
    for idd, data, date in cursor:
        companies.append(json.loads(data))
        
    return companies

def getCompanyByVAT(vat):
    """ Get company information by VAT
    
    Parameters:
        vat (str) : Company VAT number
    
    Return:
        (dict) : Company data in format:
                "city": str,
                "name": str,
                "address": str,
                "postcode": str,
                "updatedOn": datetime in str when added to DB,
                "vatNumber": str,
                "countryCode": str,
                "requestDate": date in str when requested from external service,
                "error": (dict) "is_error": Boolean, 
                                "reason": str, 
                                "info": str,
    """
    cursor = get_cursor()
    cursor.execute(query_getByVAT, (vat,))
    connection.commit()

    for (idd,data,date) in cursor:
        company = json.loads(data)
        company['error'] = {"is_error": False, "reason": "", "info": ""}
        return company
    
    return {"city":"","name":"","address":"","postcode":"","updatedOn":"","vatNumber":"","countryCode":"","requestDate":"","error": {"is_error": True, "reason": "DB problem.", "info": "Ask admin for more."}}

def insertNewCompany(data):
    """ Insert company information to Database
    
    Parameters:
        vat (str) : Company VAT number
    
    TODO: Exception handling
    """
    data['updatedOn'] = str(datetime.now())
    maindata = (data['vatNumber'], json.dumps(data), datetime.now())
    cursor = get_cursor()
    cursor.execute(query_insertCompany, maindata)
    connection.commit()


def is_VAT_in_db(vat):
    """ Is VAT in DB
    
    Parameters:
        vat (str) : Company VAT number
    
    Return:
        Boolean
    """
    
    vats = listAll()

    if vat in [v['vatNumber'] for v in vats]:
        return True
    else:
        return False

def is_VAT_valid(vat):
    """ Checking if the VAT is valid.
    
    We can assume by our logic, that if the VAT is in DB, it is valid.
    
    Parameters:
        vat (str) : Company VAT number
    
    Return:
        Company information based on the given VAT-number.
    """
    if is_VAT_in_db(vat):
        return getCompanyByVAT(vat)
    else:
        return EX.external_check_VAT(vat)