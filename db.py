import mysql.connector
import json
from datetime import datetime
import external as EX

connection = None

def init_db():
    return mysql.connector.connect(user=credentials['cres'][0], database="vat_list", password=credentials['cres'][1])

def get_cursor():
    global connection
    try:
        connection.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:  
        connection = init_db()
    return connection.cursor(buffered=True)

def setCredentials():
    """ Retrieve the credentials from random.random file.
    """
    try:
        f = open("random.random", "r")
        return {"cres":f.readlines()[0].split(","), "error": False}
    
    except IOError:
        return {"error": True, "reason": "File problem.", "info":"Won't tell you."}
    
    finally:
        f.close()

        

credentials = setCredentials()
""" Set credentials for database
"""

if credentials['error']:
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
    """
    cursor.execute(query_ListAll)
    connection.commit()
    companies = []
    
    for idd, data, date in cursor:
        companies.append(json.loads(data))
        
        # For more detailed info, ie. dump whole database, use this :
        #companies.append({"id": idd, "data": json.loads(data), "date": str(date)})
        
    return companies

def getCompanyByVAT(vat):
    """ Get company information by VAT
    """
    cursor.execute(query_getByVAT, (vat,))
    connection.commit()

    for (idd,data,date) in cursor:
        return json.loads(data)
    
    return {"error": True, "reason": "db", "info": "Empty request."}

def insertNewCompany(data):
    data['updatedOn'] = str(datetime.now())
    maindata = (data['vatNumber'], json.dumps(data), datetime.now())
    cursor.execute(query_insertCompany, maindata)
    connection.commit()


def is_VAT_in_db(vat):
    """
    """
    
    vats = listAll()

    if vat in [v['vatNumber'] for v in vats]:
        return True
    else:
        return False

def is_VAT_valid(vat):
    """ Checking if the VAT is valid.
        We can assume by our logic, that if the VAT is in DB, it is valid.
    """
    if is_VAT_in_db(vat):
        return getCompanyByVAT(vat)
    else:
        return EX.external_check_VAT(vat)